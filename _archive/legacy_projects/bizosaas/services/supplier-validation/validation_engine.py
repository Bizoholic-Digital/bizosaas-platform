#!/usr/bin/env python3
"""
Enhanced Validation Engine for Supplier Validation Workflow [P9]
Provides advanced document verification and business validation capabilities
"""

import asyncio
import json
import logging
import re
import aiohttp
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import phonenumbers
from email_validator import validate_email, EmailNotValidError

logger = logging.getLogger(__name__)

@dataclass
class ValidationResult:
    """Validation result structure"""
    is_valid: bool
    confidence_score: float
    details: Dict[str, Any]
    issues: List[str]
    recommendations: List[str]

class IndianBusinessValidator:
    """Indian business validation engine"""
    
    def __init__(self):
        self.gst_states = {
            "01": "Jammu and Kashmir", "02": "Himachal Pradesh", "03": "Punjab",
            "04": "Chandigarh", "05": "Uttarakhand", "06": "Haryana",
            "07": "Delhi", "08": "Rajasthan", "09": "Uttar Pradesh",
            "10": "Bihar", "11": "Sikkim", "12": "Arunachal Pradesh",
            "13": "Nagaland", "14": "Manipur", "15": "Mizoram",
            "16": "Tripura", "17": "Meghalaya", "18": "Assam",
            "19": "West Bengal", "20": "Jharkhand", "21": "Odisha",
            "22": "Chhattisgarh", "23": "Madhya Pradesh", "24": "Gujarat",
            "25": "Daman and Diu", "26": "Dadra and Nagar Haveli",
            "27": "Maharashtra", "28": "Andhra Pradesh", "29": "Karnataka",
            "30": "Goa", "31": "Lakshadweep", "32": "Kerala",
            "33": "Tamil Nadu", "34": "Puducherry", "35": "Andaman and Nicobar Islands",
            "36": "Telangana", "37": "Andhra Pradesh", "38": "Ladakh"
        }
    
    async def validate_gst_number(self, gst_number: str, state: str = None) -> ValidationResult:
        """Validate GST number format and optionally verify against API"""
        issues = []
        details = {}
        
        # Basic format validation
        gst_pattern = r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$'
        
        if not re.match(gst_pattern, gst_number):
            return ValidationResult(
                is_valid=False,
                confidence_score=0.0,
                details={"format": "invalid"},
                issues=["Invalid GST number format"],
                recommendations=["Provide valid 15-character GST number"]
            )
        
        # Extract state code
        state_code = gst_number[:2]
        gst_state = self.gst_states.get(state_code)
        
        if gst_state:
            details["state_code"] = state_code
            details["gst_state"] = gst_state
            
            # Cross-check with provided state
            if state and gst_state.lower() != state.lower():
                issues.append(f"GST state ({gst_state}) doesn't match provided state ({state})")
        else:
            issues.append(f"Invalid state code in GST: {state_code}")
        
        # Check digit validation (simplified)
        pan_part = gst_number[2:12]
        details["pan_from_gst"] = pan_part
        
        # Calculate confidence
        confidence = 0.8 if not issues else 0.4
        
        return ValidationResult(
            is_valid=len(issues) == 0,
            confidence_score=confidence,
            details=details,
            issues=issues,
            recommendations=["Verify GST registration with government portal"] if not issues else [
                "Correct GST number format",
                "Ensure state matches business location"
            ]
        )
    
    async def validate_pan_number(self, pan_number: str) -> ValidationResult:
        """Validate PAN number format"""
        issues = []
        details = {}
        
        pan_pattern = r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$'
        
        if not re.match(pan_pattern, pan_number):
            return ValidationResult(
                is_valid=False,
                confidence_score=0.0,
                details={"format": "invalid"},
                issues=["Invalid PAN number format"],
                recommendations=["Provide valid 10-character PAN number"]
            )
        
        # Extract information from PAN
        details["entity_type"] = self._get_pan_entity_type(pan_number[3])
        details["area_code"] = pan_number[4]
        details["serial_number"] = pan_number[5:9]
        details["check_digit"] = pan_number[9]
        
        return ValidationResult(
            is_valid=True,
            confidence_score=0.9,
            details=details,
            issues=[],
            recommendations=["Verify PAN with Income Tax Department"]
        )
    
    def _get_pan_entity_type(self, fourth_char: str) -> str:
        """Get entity type from PAN fourth character"""
        entity_types = {
            'P': 'Individual',
            'C': 'Company',
            'H': 'HUF',
            'F': 'Firm',
            'A': 'Association of Persons',
            'T': 'Trust',
            'B': 'Body of Individuals',
            'L': 'Local Authority',
            'J': 'Artificial Juridical Person',
            'G': 'Government'
        }
        return entity_types.get(fourth_char, 'Unknown')

class EmailPhoneValidator:
    """Email and phone validation"""
    
    async def validate_email(self, email: str) -> ValidationResult:
        """Validate email address"""
        issues = []
        details = {}
        
        try:
            validation = validate_email(email)
            normalized_email = validation.email
            
            details["normalized"] = normalized_email
            details["domain"] = validation.domain
            details["local"] = validation.local
            
            # Check for common business email domains
            business_domains = [
                'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com'
            ]
            
            if validation.domain.lower() in business_domains:
                issues.append("Using personal email domain instead of business domain")
                confidence = 0.6
            else:
                confidence = 0.9
            
            return ValidationResult(
                is_valid=True,
                confidence_score=confidence,
                details=details,
                issues=issues,
                recommendations=["Consider using business domain email"] if issues else []
            )
            
        except EmailNotValidError as e:
            return ValidationResult(
                is_valid=False,
                confidence_score=0.0,
                details={"error": str(e)},
                issues=["Invalid email format"],
                recommendations=["Provide valid email address"]
            )
    
    async def validate_phone(self, phone: str, country_code: str = "IN") -> ValidationResult:
        """Validate phone number"""
        issues = []
        details = {}
        
        try:
            parsed = phonenumbers.parse(phone, country_code)
            
            if not phonenumbers.is_valid_number(parsed):
                return ValidationResult(
                    is_valid=False,
                    confidence_score=0.0,
                    details={},
                    issues=["Invalid phone number"],
                    recommendations=["Provide valid phone number with country code"]
                )
            
            # Format phone number
            details["formatted"] = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
            details["national"] = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL)
            details["international"] = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
            details["country_code"] = parsed.country_code
            details["number_type"] = phonenumbers.number_type(parsed)
            
            # Check if it's a mobile number (preferred for business contact)
            if phonenumbers.number_type(parsed) != phonenumbers.PhoneNumberType.MOBILE:
                issues.append("Phone number is not a mobile number")
                confidence = 0.7
            else:
                confidence = 0.95
            
            return ValidationResult(
                is_valid=True,
                confidence_score=confidence,
                details=details,
                issues=issues,
                recommendations=["Consider providing mobile number for better communication"] if issues else []
            )
            
        except phonenumbers.NumberParseException as e:
            return ValidationResult(
                is_valid=False,
                confidence_score=0.0,
                details={"error": str(e)},
                issues=["Phone number parsing error"],
                recommendations=["Provide phone number in correct format"]
            )

class WebsiteValidator:
    """Website validation and analysis"""
    
    async def validate_website(self, url: str) -> ValidationResult:
        """Validate website URL and check accessibility"""
        issues = []
        details = {}
        
        # Basic URL format validation
        url_pattern = r'^https?:\/\/(www\.)?[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*\/?.*$'
        
        if not re.match(url_pattern, url):
            return ValidationResult(
                is_valid=False,
                confidence_score=0.0,
                details={},
                issues=["Invalid URL format"],
                recommendations=["Provide valid website URL starting with http:// or https://"]
            )
        
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
                async with session.get(url) as response:
                    details["status_code"] = response.status
                    details["content_type"] = response.headers.get('content-type', '')
                    details["server"] = response.headers.get('server', '')
                    
                    if response.status == 200:
                        # Read first 1KB of content to analyze
                        content = await response.text()
                        details["has_title"] = '<title>' in content.lower()
                        details["has_meta"] = '<meta' in content.lower()
                        details["content_length"] = len(content)
                        
                        # Check for business indicators
                        business_keywords = ['about', 'contact', 'services', 'products', 'company']
                        found_keywords = [kw for kw in business_keywords if kw in content.lower()]
                        details["business_keywords"] = found_keywords
                        
                        if len(found_keywords) >= 2:
                            confidence = 0.9
                        elif len(found_keywords) >= 1:
                            confidence = 0.7
                        else:
                            confidence = 0.5
                            issues.append("Website lacks clear business information")
                    
                    elif response.status == 404:
                        issues.append("Website not found (404)")
                        confidence = 0.0
                    else:
                        issues.append(f"Website returned status code {response.status}")
                        confidence = 0.3
        
        except asyncio.TimeoutError:
            issues.append("Website timeout - slow or unresponsive")
            confidence = 0.2
        except Exception as e:
            issues.append(f"Website accessibility error: {str(e)}")
            confidence = 0.1
        
        return ValidationResult(
            is_valid=len(issues) == 0,
            confidence_score=confidence,
            details=details,
            issues=issues,
            recommendations=[
                "Ensure website is accessible and loads quickly",
                "Include clear business information and contact details"
            ] if issues else ["Website appears professional and accessible"]
        )

class BusinessProfileValidator:
    """Business profile validation using AI and heuristics"""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
    
    async def validate_business_profile(self, profile_data: Dict[str, Any]) -> ValidationResult:
        """Validate complete business profile"""
        issues = []
        details = {}
        recommendations = []
        
        # Validate company name
        company_validation = self._validate_company_name(profile_data.get('company_name', ''))
        details['company_name_validation'] = company_validation
        if not company_validation['is_valid']:
            issues.extend(company_validation['issues'])
        
        # Validate industry-products alignment
        industry = profile_data.get('industry', '').lower()
        products = profile_data.get('products_offered', [])
        alignment_score = self._validate_industry_product_alignment(industry, products)
        details['industry_product_alignment'] = alignment_score
        
        if alignment_score < 0.5:
            issues.append("Products/services don't align well with stated industry")
            recommendations.append("Ensure products match your industry category")
        
        # Validate business size consistency
        size_validation = self._validate_business_size_consistency(profile_data)
        details['size_consistency'] = size_validation
        if not size_validation['is_consistent']:
            issues.extend(size_validation['issues'])
        
        # Calculate overall confidence
        confidence = self._calculate_profile_confidence(details, issues)
        
        return ValidationResult(
            is_valid=len(issues) == 0,
            confidence_score=confidence,
            details=details,
            issues=issues,
            recommendations=recommendations
        )
    
    def _validate_company_name(self, company_name: str) -> Dict[str, Any]:
        """Validate company name format and characteristics"""
        issues = []
        
        if len(company_name) < 3:
            issues.append("Company name too short")
        
        if len(company_name) > 100:
            issues.append("Company name too long")
        
        # Check for business suffixes
        business_suffixes = [
            'pvt ltd', 'private limited', 'ltd', 'limited', 'llp', 'llc',
            'inc', 'corporation', 'corp', 'company', 'co'
        ]
        
        has_suffix = any(suffix in company_name.lower() for suffix in business_suffixes)
        
        # Check for suspicious patterns
        suspicious_patterns = [
            r'\d{5,}',  # Too many numbers
            r'[!@#$%^&*()_+=\[\]{}|;\':",./<>?]',  # Special characters
            r'^(test|demo|sample|example)',  # Test names
        ]
        
        for pattern in suspicious_patterns:
            if re.search(pattern, company_name.lower()):
                issues.append("Company name contains suspicious patterns")
                break
        
        return {
            'is_valid': len(issues) == 0,
            'issues': issues,
            'has_business_suffix': has_suffix,
            'length': len(company_name)
        }
    
    def _validate_industry_product_alignment(self, industry: str, products: List[str]) -> float:
        """Validate alignment between industry and products using text similarity"""
        if not industry or not products:
            return 0.5
        
        # Industry keywords mapping
        industry_keywords = {
            'technology': ['software', 'hardware', 'app', 'digital', 'tech', 'it', 'computer'],
            'manufacturing': ['production', 'factory', 'assembly', 'industrial', 'equipment'],
            'retail': ['sales', 'store', 'shop', 'merchandise', 'customer'],
            'healthcare': ['medical', 'health', 'pharmaceutical', 'clinical', 'patient'],
            'education': ['training', 'learning', 'academic', 'school', 'course'],
            'finance': ['banking', 'investment', 'financial', 'money', 'payment'],
            'food': ['restaurant', 'catering', 'beverage', 'culinary', 'dining'],
            'construction': ['building', 'infrastructure', 'engineering', 'architecture'],
            'textile': ['fabric', 'clothing', 'garment', 'fashion', 'apparel'],
            'automotive': ['vehicle', 'car', 'auto', 'transport', 'mobility']
        }
        
        # Find matching industry keywords
        industry_terms = []
        for key, keywords in industry_keywords.items():
            if key in industry:
                industry_terms.extend(keywords)
        
        if not industry_terms:
            return 0.6  # Neutral score for unknown industries
        
        # Calculate similarity with products
        product_text = ' '.join(products).lower()
        industry_text = ' '.join(industry_terms)
        
        try:
            combined_text = [industry_text, product_text]
            tfidf_matrix = self.vectorizer.fit_transform(combined_text)
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            return float(similarity)
        except:
            # Fallback to keyword matching
            matches = sum(1 for term in industry_terms if term in product_text)
            return min(matches / len(industry_terms), 1.0)
    
    def _validate_business_size_consistency(self, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate consistency between employee count, revenue, and business type"""
        issues = []
        employee_count = profile_data.get('employee_count', 0)
        annual_revenue = profile_data.get('annual_revenue', 0)
        business_type = profile_data.get('business_type', '').lower()
        
        # Size category determination
        if employee_count == 0 and annual_revenue == 0:
            return {'is_consistent': True, 'issues': [], 'category': 'unknown'}
        
        # Employee count vs revenue consistency
        if employee_count > 0 and annual_revenue > 0:
            revenue_per_employee = annual_revenue / employee_count
            
            # Indian market revenue per employee benchmarks (in INR)
            if revenue_per_employee < 100000:  # Less than 1 lakh per employee
                issues.append("Revenue per employee seems too low")
            elif revenue_per_employee > 10000000:  # More than 1 crore per employee
                issues.append("Revenue per employee seems unusually high")
        
        # Business type consistency
        if 'private limited' in business_type or 'public limited' in business_type:
            if employee_count > 0 and employee_count < 3:
                issues.append("Private/Public limited company with very few employees")
        
        if 'sole proprietorship' in business_type:
            if employee_count > 50:
                issues.append("Sole proprietorship with large employee count")
        
        return {
            'is_consistent': len(issues) == 0,
            'issues': issues,
            'category': self._determine_business_size_category(employee_count, annual_revenue)
        }
    
    def _determine_business_size_category(self, employees: int, revenue: float) -> str:
        """Determine business size category"""
        if employees <= 10 or revenue <= 1000000:  # 10 lakhs
            return 'micro'
        elif employees <= 50 or revenue <= 10000000:  # 1 crore
            return 'small'
        elif employees <= 250 or revenue <= 100000000:  # 10 crores
            return 'medium'
        else:
            return 'large'
    
    def _calculate_profile_confidence(self, details: Dict[str, Any], issues: List[str]) -> float:
        """Calculate overall profile confidence score"""
        base_score = 0.8
        
        # Deduct for issues
        issue_penalty = len(issues) * 0.1
        
        # Adjust based on validations
        company_score = 0.1 if details.get('company_name_validation', {}).get('is_valid', False) else 0
        alignment_score = details.get('industry_product_alignment', 0.5) * 0.1
        consistency_bonus = 0.1 if details.get('size_consistency', {}).get('is_consistent', False) else 0
        
        final_score = base_score + company_score + alignment_score + consistency_bonus - issue_penalty
        return max(0.0, min(1.0, final_score))

class ComprehensiveSupplierValidator:
    """Main comprehensive supplier validation engine"""
    
    def __init__(self):
        self.business_validator = IndianBusinessValidator()
        self.contact_validator = EmailPhoneValidator()
        self.website_validator = WebsiteValidator()
        self.profile_validator = BusinessProfileValidator()
    
    async def validate_supplier_comprehensively(self, supplier_data: Dict[str, Any]) -> Dict[str, ValidationResult]:
        """Perform comprehensive validation of supplier data"""
        results = {}
        
        # GST validation
        if supplier_data.get('gst_number'):
            results['gst'] = await self.business_validator.validate_gst_number(
                supplier_data['gst_number'],
                supplier_data.get('state')
            )
        
        # PAN validation
        if supplier_data.get('pan_number'):
            results['pan'] = await self.business_validator.validate_pan_number(
                supplier_data['pan_number']
            )
        
        # Email validation
        if supplier_data.get('email'):
            results['email'] = await self.contact_validator.validate_email(
                supplier_data['email']
            )
        
        # Phone validation
        if supplier_data.get('phone'):
            results['phone'] = await self.contact_validator.validate_phone(
                supplier_data['phone']
            )
        
        # Website validation
        if supplier_data.get('website'):
            results['website'] = await self.website_validator.validate_website(
                supplier_data['website']
            )
        
        # Business profile validation
        results['business_profile'] = await self.profile_validator.validate_business_profile(
            supplier_data
        )
        
        return results
    
    def calculate_overall_validation_score(self, validation_results: Dict[str, ValidationResult]) -> Tuple[float, List[str], List[str]]:
        """Calculate overall validation score and compile issues/recommendations"""
        total_score = 0.0
        total_weight = 0.0
        all_issues = []
        all_recommendations = []
        
        # Weights for different validations
        weights = {
            'gst': 0.2,
            'pan': 0.15,
            'email': 0.1,
            'phone': 0.1,
            'website': 0.15,
            'business_profile': 0.3
        }
        
        for validation_type, result in validation_results.items():
            weight = weights.get(validation_type, 0.1)
            total_score += result.confidence_score * weight
            total_weight += weight
            
            all_issues.extend(result.issues)
            all_recommendations.extend(result.recommendations)
        
        # Normalize score
        if total_weight > 0:
            final_score = total_score / total_weight
        else:
            final_score = 0.5
        
        # Remove duplicate recommendations
        unique_recommendations = list(set(all_recommendations))
        
        return final_score, all_issues, unique_recommendations

# Example usage and testing
async def test_validation_engine():
    """Test the validation engine"""
    validator = ComprehensiveSupplierValidator()
    
    sample_data = {
        'company_name': 'ABC Electronics Pvt Ltd',
        'email': 'contact@abcelectronics.com',
        'phone': '+91-9876543210',
        'gst_number': '07AABCA1234M1Z5',
        'pan_number': 'AABCA1234M',
        'website': 'https://www.abcelectronics.com',
        'state': 'Delhi',
        'industry': 'Electronics Manufacturing',
        'products_offered': ['Smartphones', 'Laptops', 'Accessories'],
        'employee_count': 25,
        'annual_revenue': 50000000,
        'business_type': 'Private Limited Company'
    }
    
    results = await validator.validate_supplier_comprehensively(sample_data)
    score, issues, recommendations = validator.calculate_overall_validation_score(results)
    
    print(f"Overall Validation Score: {score:.2f}")
    print(f"Issues: {issues}")
    print(f"Recommendations: {recommendations}")
    
    return results, score, issues, recommendations

if __name__ == "__main__":
    asyncio.run(test_validation_engine())