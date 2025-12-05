"""
Google Business Profile Data Mappers
Handles mapping between Google My Business data and our Business Directory models
"""

import re
import logging
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime, time
from dataclasses import dataclass

import phonenumbers
from phonenumbers import NumberParseException

from ..models.business import BusinessListing, BusinessCategory
from ..models.google_integration import GoogleBusinessLocation

logger = logging.getLogger(__name__)


@dataclass
class MappingResult:
    """Result of a mapping operation"""
    success: bool
    data: Optional[Dict[str, Any]] = None
    warnings: List[str] = None
    errors: List[str] = None
    
    def __post_init__(self):
        if self.warnings is None:
            self.warnings = []
        if self.errors is None:
            self.errors = []


class GoogleDataMapper:
    """
    Maps data between Google My Business API responses and our business models
    """
    
    # Google category to our category mapping
    CATEGORY_MAPPING = {
        "Restaurant": "restaurants",
        "Grocery store": "grocery",
        "Gas station": "automotive",
        "Hospital": "healthcare",
        "Doctor": "healthcare",
        "Dentist": "healthcare",
        "Pharmacy": "healthcare",
        "School": "education",
        "University": "education",
        "Bank": "financial",
        "ATM": "financial",
        "Hotel": "hospitality",
        "Shopping mall": "shopping",
        "Clothing store": "retail",
        "Electronics store": "retail",
        "Beauty salon": "beauty",
        "Hair salon": "beauty",
        "Gym": "fitness",
        "Lawyer": "legal",
        "Real estate agency": "real-estate",
        "Car dealership": "automotive",
        "Auto repair shop": "automotive",
        "Veterinarian": "pet-services",
        "Pet store": "pet-services",
    }
    
    # Days of week mapping
    DAY_MAPPING = {
        "MONDAY": "monday",
        "TUESDAY": "tuesday", 
        "WEDNESDAY": "wednesday",
        "THURSDAY": "thursday",
        "FRIDAY": "friday",
        "SATURDAY": "saturday",
        "SUNDAY": "sunday"
    }
    
    def map_google_location_to_business(
        self, 
        google_location: Dict[str, Any], 
        tenant_id: str
    ) -> MappingResult:
        """
        Map Google location data to BusinessListing format
        
        Args:
            google_location: Raw Google location data
            tenant_id: Tenant ID for the business
            
        Returns:
            MappingResult with mapped business data
        """
        try:
            warnings = []
            errors = []
            
            # Extract basic information
            business_data = {
                "tenant_id": tenant_id,
                "name": google_location.get("title", ""),
                "description": google_location.get("description", ""),
                "short_description": self._truncate_description(
                    google_location.get("description", ""), 
                    max_length=500
                )
            }
            
            # Map address
            address_result = self._map_address(google_location.get("storefrontAddress", {}))
            business_data.update(address_result.data or {})
            warnings.extend(address_result.warnings)
            errors.extend(address_result.errors)
            
            # Map contact information
            contact_result = self._map_contact_info(google_location)
            business_data.update(contact_result.data or {})
            warnings.extend(contact_result.warnings)
            errors.extend(contact_result.errors)
            
            # Map business hours
            hours_result = self._map_business_hours(google_location.get("regularHours", {}))
            if hours_result.success and hours_result.data:
                business_data["business_hours"] = hours_result.data
            warnings.extend(hours_result.warnings)
            
            # Map category
            category_result = self._map_category(google_location.get("categories", []))
            if category_result.success and category_result.data:
                business_data.update(category_result.data)
            warnings.extend(category_result.warnings)
            
            # Map additional fields
            business_data.update({
                "website": self._clean_website_url(google_location.get("websiteUri", "")),
                "is_claimed": True,  # Google locations are by definition claimed
                "claimed_at": datetime.utcnow(),
                "is_verified": google_location.get("metadata", {}).get("placeId") is not None,
                "status": "active"
            })
            
            # Map metadata and additional info
            metadata_result = self._map_metadata(google_location)
            if metadata_result.success and metadata_result.data:
                business_data.update(metadata_result.data)
            warnings.extend(metadata_result.warnings)
            
            return MappingResult(
                success=True,
                data=business_data,
                warnings=warnings,
                errors=errors
            )
            
        except Exception as e:
            logger.error(f"Error mapping Google location to business: {str(e)}")
            return MappingResult(
                success=False,
                errors=[f"Mapping failed: {str(e)}"]
            )
    
    def map_business_to_google_location(
        self, 
        business: BusinessListing
    ) -> MappingResult:
        """
        Map BusinessListing to Google location update format
        
        Args:
            business: BusinessListing instance
            
        Returns:
            MappingResult with Google-formatted data
        """
        try:
            warnings = []
            
            google_data = {
                "title": business.name,
                "description": business.description or "",
                "websiteUri": business.website or ""
            }
            
            # Map address
            if any([business.address_line_1, business.city, business.state]):
                address_data = {
                    "addressLines": [line for line in [
                        business.address_line_1, 
                        business.address_line_2
                    ] if line],
                    "locality": business.city or "",
                    "administrativeArea": business.state or "",
                    "postalCode": business.postal_code or "",
                    "regionCode": self._get_country_code(business.country or "US")
                }
                google_data["storefrontAddress"] = address_data
            
            # Map phone number
            if business.phone:
                phone_result = self._format_phone_for_google(business.phone)
                if phone_result.success:
                    google_data["phoneNumbers"] = {
                        "primaryPhone": phone_result.data["formatted_phone"]
                    }
                else:
                    warnings.extend(phone_result.warnings)
            
            # Map business hours
            if business.business_hours:
                hours_result = self._map_hours_to_google_format(business.business_hours)
                if hours_result.success:
                    google_data["regularHours"] = hours_result.data
                else:
                    warnings.extend(hours_result.warnings)
            
            # Map category
            if business.category:
                category_result = self._map_category_to_google(business.category)
                if category_result.success:
                    google_data["categories"] = category_result.data
                else:
                    warnings.extend(category_result.warnings)
            
            return MappingResult(
                success=True,
                data=google_data,
                warnings=warnings
            )
            
        except Exception as e:
            logger.error(f"Error mapping business to Google location: {str(e)}")
            return MappingResult(
                success=False,
                errors=[f"Mapping failed: {str(e)}"]
            )
    
    def _map_address(self, google_address: Dict[str, Any]) -> MappingResult:
        """Map Google address to our address format"""
        try:
            address_lines = google_address.get("addressLines", [])
            
            data = {
                "address_line_1": address_lines[0] if len(address_lines) > 0 else "",
                "address_line_2": address_lines[1] if len(address_lines) > 1 else "",
                "city": google_address.get("locality", ""),
                "state": google_address.get("administrativeArea", ""),
                "postal_code": google_address.get("postalCode", ""),
                "country": self._get_country_name(google_address.get("regionCode", "US"))
            }
            
            return MappingResult(success=True, data=data)
            
        except Exception as e:
            return MappingResult(
                success=False,
                errors=[f"Address mapping failed: {str(e)}"]
            )
    
    def _map_contact_info(self, google_location: Dict[str, Any]) -> MappingResult:
        """Map Google contact information"""
        try:
            warnings = []
            data = {}
            
            # Phone number
            phone_numbers = google_location.get("phoneNumbers", {})
            primary_phone = phone_numbers.get("primaryPhone", "")
            
            if primary_phone:
                phone_result = self._normalize_phone_number(primary_phone)
                if phone_result.success:
                    data["phone"] = phone_result.data["normalized_phone"]
                else:
                    warnings.append(f"Invalid phone number: {primary_phone}")
            
            # Additional phone numbers could be stored in metadata
            additional_phones = phone_numbers.get("additionalPhones", [])
            if additional_phones:
                data["additional_phones"] = additional_phones
            
            return MappingResult(success=True, data=data, warnings=warnings)
            
        except Exception as e:
            return MappingResult(
                success=False,
                errors=[f"Contact info mapping failed: {str(e)}"]
            )
    
    def _map_business_hours(self, google_hours: Dict[str, Any]) -> MappingResult:
        """Map Google business hours to our format"""
        try:
            if not google_hours or not google_hours.get("periods"):
                return MappingResult(success=True, data={})
            
            mapped_hours = {}
            warnings = []
            
            for period in google_hours.get("periods", []):
                # Google uses different day format
                open_day = period.get("openDay")
                close_day = period.get("closeDay", open_day)
                
                if open_day in self.DAY_MAPPING:
                    day_name = self.DAY_MAPPING[open_day]
                    
                    open_time = period.get("openTime", {})
                    close_time = period.get("closeTime", {})
                    
                    if open_time and close_time:
                        hours_str = f"{self._format_time(open_time)}-{self._format_time(close_time)}"
                        mapped_hours[day_name] = {
                            "open": self._format_time(open_time),
                            "close": self._format_time(close_time),
                            "is_open": True
                        }
                    else:
                        mapped_hours[day_name] = {"is_open": False}
                else:
                    warnings.append(f"Unknown day format: {open_day}")
            
            return MappingResult(
                success=True,
                data=mapped_hours,
                warnings=warnings
            )
            
        except Exception as e:
            return MappingResult(
                success=False,
                errors=[f"Business hours mapping failed: {str(e)}"]
            )
    
    def _map_category(self, google_categories: List[Dict[str, Any]]) -> MappingResult:
        """Map Google categories to our category system"""
        try:
            if not google_categories:
                return MappingResult(success=True, data={})
            
            warnings = []
            primary_category = google_categories[0] if google_categories else {}
            primary_category_name = primary_category.get("displayName", "")
            
            # Try to find matching category in our system
            mapped_category = self.CATEGORY_MAPPING.get(primary_category_name)
            
            if not mapped_category:
                # Try partial matching
                for google_cat, our_cat in self.CATEGORY_MAPPING.items():
                    if google_cat.lower() in primary_category_name.lower():
                        mapped_category = our_cat
                        break
            
            data = {}
            if mapped_category:
                data["category_slug"] = mapped_category
            else:
                warnings.append(f"No mapping found for category: {primary_category_name}")
            
            # Store all Google categories as tags
            category_tags = [cat.get("displayName", "") for cat in google_categories]
            data["google_categories"] = category_tags
            
            return MappingResult(
                success=True,
                data=data,
                warnings=warnings
            )
            
        except Exception as e:
            return MappingResult(
                success=False,
                errors=[f"Category mapping failed: {str(e)}"]
            )
    
    def _map_metadata(self, google_location: Dict[str, Any]) -> MappingResult:
        """Map additional Google metadata"""
        try:
            metadata = google_location.get("metadata", {})
            profile = google_location.get("profile", {})
            
            data = {
                "google_place_id": metadata.get("placeId", ""),
                "google_metadata": {
                    "google_updated": metadata.get("updateTime"),
                    "google_created": metadata.get("createTime"),
                    "duplicate_location": metadata.get("duplicateLocation"),
                    "can_modify_service_list": metadata.get("canModifyServiceList", False),
                    "can_have_business_calls": metadata.get("canHaveBusinessCalls", False),
                    "has_pending_edits": metadata.get("hasPendingEdits", False)
                }
            }
            
            # Add profile information if available
            if profile:
                data["google_metadata"]["profile"] = profile
            
            # Map special attributes
            attributes = google_location.get("attributes", [])
            if attributes:
                amenities = []
                for attr in attributes:
                    attr_name = attr.get("attributeId", "")
                    if attr.get("valueType") == "BOOL" and attr.get("booleanValue"):
                        amenities.append(self._humanize_attribute_name(attr_name))
                
                if amenities:
                    data["amenities"] = amenities
            
            return MappingResult(success=True, data=data)
            
        except Exception as e:
            return MappingResult(
                success=False,
                errors=[f"Metadata mapping failed: {str(e)}"]
            )
    
    def _normalize_phone_number(self, phone: str) -> MappingResult:
        """Normalize phone number to standard format"""
        try:
            # Remove common formatting
            cleaned = re.sub(r'[^\d+]', '', phone)
            
            # Parse with phonenumbers library
            try:
                parsed = phonenumbers.parse(cleaned, "US")  # Default to US
                if phonenumbers.is_valid_number(parsed):
                    formatted = phonenumbers.format_number(
                        parsed, 
                        phonenumbers.PhoneNumberFormat.E164
                    )
                    display_format = phonenumbers.format_number(
                        parsed,
                        phonenumbers.PhoneNumberFormat.NATIONAL
                    )
                    
                    return MappingResult(
                        success=True,
                        data={
                            "normalized_phone": formatted,
                            "display_phone": display_format
                        }
                    )
            except NumberParseException:
                pass
            
            # Fallback: basic cleaning
            if len(cleaned) >= 10:
                return MappingResult(
                    success=True,
                    data={"normalized_phone": cleaned},
                    warnings=["Phone number validation failed, using cleaned version"]
                )
            
            return MappingResult(
                success=False,
                errors=["Invalid phone number format"]
            )
            
        except Exception as e:
            return MappingResult(
                success=False,
                errors=[f"Phone normalization failed: {str(e)}"]
            )
    
    def _format_phone_for_google(self, phone: str) -> MappingResult:
        """Format phone number for Google API"""
        try:
            # Google expects E.164 format
            normalized_result = self._normalize_phone_number(phone)
            if normalized_result.success:
                return MappingResult(
                    success=True,
                    data={"formatted_phone": normalized_result.data["normalized_phone"]}
                )
            
            return normalized_result
            
        except Exception as e:
            return MappingResult(
                success=False,
                errors=[f"Phone formatting failed: {str(e)}"]
            )
    
    def _format_time(self, time_obj: Dict[str, Any]) -> str:
        """Format Google time object to HH:MM string"""
        try:
            hours = time_obj.get("hours", 0)
            minutes = time_obj.get("minutes", 0)
            return f"{hours:02d}:{minutes:02d}"
        except:
            return "00:00"
    
    def _map_hours_to_google_format(self, business_hours: Dict[str, Any]) -> MappingResult:
        """Map our business hours format to Google format"""
        try:
            periods = []
            
            # Reverse day mapping
            reverse_day_mapping = {v: k for k, v in self.DAY_MAPPING.items()}
            
            for day_name, hours_info in business_hours.items():
                if day_name in reverse_day_mapping and hours_info.get("is_open"):
                    google_day = reverse_day_mapping[day_name]
                    
                    open_time = hours_info.get("open", "09:00")
                    close_time = hours_info.get("close", "17:00")
                    
                    # Parse time strings
                    open_parts = open_time.split(":")
                    close_parts = close_time.split(":")
                    
                    period = {
                        "openDay": google_day,
                        "openTime": {
                            "hours": int(open_parts[0]),
                            "minutes": int(open_parts[1]) if len(open_parts) > 1 else 0
                        },
                        "closeDay": google_day,
                        "closeTime": {
                            "hours": int(close_parts[0]),
                            "minutes": int(close_parts[1]) if len(close_parts) > 1 else 0
                        }
                    }
                    periods.append(period)
            
            return MappingResult(
                success=True,
                data={"periods": periods}
            )
            
        except Exception as e:
            return MappingResult(
                success=False,
                errors=[f"Hours mapping to Google format failed: {str(e)}"]
            )
    
    def _map_category_to_google(self, category: BusinessCategory) -> MappingResult:
        """Map our category to Google category format"""
        try:
            # Reverse lookup in category mapping
            google_category = None
            for google_cat, our_cat in self.CATEGORY_MAPPING.items():
                if our_cat == category.slug:
                    google_category = google_cat
                    break
            
            if not google_category:
                # Fallback to category name
                google_category = category.name
            
            return MappingResult(
                success=True,
                data={
                    "primary": {
                        "categoryId": google_category,
                        "displayName": google_category
                    }
                }
            )
            
        except Exception as e:
            return MappingResult(
                success=False,
                errors=[f"Category mapping to Google failed: {str(e)}"]
            )
    
    def _clean_website_url(self, url: str) -> str:
        """Clean and validate website URL"""
        if not url:
            return ""
        
        url = url.strip()
        if not url.startswith(("http://", "https://")):
            url = f"https://{url}"
        
        return url
    
    def _truncate_description(self, description: str, max_length: int = 500) -> str:
        """Truncate description to specified length"""
        if not description or len(description) <= max_length:
            return description
        
        # Truncate at word boundary
        truncated = description[:max_length]
        last_space = truncated.rfind(" ")
        if last_space > max_length * 0.8:  # Don't truncate too much
            truncated = truncated[:last_space]
        
        return truncated + "..."
    
    def _get_country_code(self, country_name: str) -> str:
        """Get country code from country name"""
        country_codes = {
            "United States": "US",
            "Canada": "CA",
            "United Kingdom": "GB",
            "Australia": "AU",
            # Add more as needed
        }
        return country_codes.get(country_name, "US")
    
    def _get_country_name(self, country_code: str) -> str:
        """Get country name from country code"""
        country_names = {
            "US": "United States",
            "CA": "Canada", 
            "GB": "United Kingdom",
            "AU": "Australia",
            # Add more as needed
        }
        return country_names.get(country_code, "United States")
    
    def _humanize_attribute_name(self, attr_name: str) -> str:
        """Convert Google attribute name to human-readable format"""
        # Remove common prefixes/suffixes
        attr_name = attr_name.replace("has_", "").replace("_available", "")
        
        # Convert snake_case to Title Case
        return attr_name.replace("_", " ").title()
    
    def detect_conflicts(
        self, 
        business_data: Dict[str, Any], 
        google_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Detect conflicts between business data and Google data
        
        Returns:
            List of conflict dictionaries
        """
        conflicts = []
        
        # Define fields to compare
        comparison_fields = [
            ("name", "title"),
            ("description", "description"),
            ("phone", "phoneNumbers.primaryPhone"),
            ("website", "websiteUri"),
            ("address_line_1", "storefrontAddress.addressLines[0]"),
            ("city", "storefrontAddress.locality"),
            ("state", "storefrontAddress.administrativeArea"),
            ("postal_code", "storefrontAddress.postalCode")
        ]
        
        for business_field, google_field_path in comparison_fields:
            business_value = business_data.get(business_field)
            google_value = self._get_nested_value(google_data, google_field_path)
            
            if business_value and google_value and business_value != google_value:
                conflicts.append({
                    "field": business_field,
                    "local_value": business_value,
                    "google_value": google_value,
                    "severity": self._get_conflict_severity(business_field),
                    "recommendation": self._get_conflict_recommendation(business_field)
                })
        
        return conflicts
    
    def _get_nested_value(self, data: Dict[str, Any], path: str) -> Any:
        """Get nested value from dictionary using dot notation"""
        try:
            current = data
            for key in path.split("."):
                if "[" in key and "]" in key:
                    # Handle array access like "addressLines[0]"
                    array_key, index_str = key.split("[")
                    index = int(index_str.rstrip("]"))
                    current = current[array_key][index]
                else:
                    current = current[key]
            return current
        except (KeyError, IndexError, TypeError):
            return None
    
    def _get_conflict_severity(self, field: str) -> str:
        """Get conflict severity level"""
        high_priority = ["name", "phone", "address_line_1"]
        medium_priority = ["description", "website", "city", "state"]
        
        if field in high_priority:
            return "high"
        elif field in medium_priority:
            return "medium"
        else:
            return "low"
    
    def _get_conflict_recommendation(self, field: str) -> str:
        """Get recommendation for resolving conflict"""
        recommendations = {
            "name": "Business name conflicts require careful review",
            "phone": "Phone number should match primary business contact", 
            "address_line_1": "Address conflicts may affect local search results",
            "description": "Consider combining information from both sources",
            "website": "Verify which URL is current and active"
        }
        return recommendations.get(field, "Review both values and choose the most accurate")


# Service instance
google_data_mapper = GoogleDataMapper()