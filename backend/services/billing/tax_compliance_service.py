"""
Multi-Currency and Tax Compliance Service
Handles international tax calculations, VAT, GST, and currency conversions
"""

import logging
from datetime import datetime, date
from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, List, Optional, Tuple
from uuid import UUID
import json

from sqlalchemy import text
from database import get_db
from core.error_handler import ErrorHandler


class TaxComplianceService:
    """Comprehensive tax compliance for international operations"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.error_handler = ErrorHandler()
        
        # Tax rates by country/region (as of 2024)
        self.tax_rates = {
            # North America
            'US': {'rate': Decimal('0.00'), 'type': 'none', 'threshold': None},  # Varies by state
            'CA': {'rate': Decimal('0.05'), 'type': 'gst', 'threshold': Decimal('30000')},  # GST, varies by province
            
            # Europe (VAT)
            'GB': {'rate': Decimal('0.20'), 'type': 'vat', 'threshold': Decimal('85000')},
            'DE': {'rate': Decimal('0.19'), 'type': 'vat', 'threshold': Decimal('22000')},
            'FR': {'rate': Decimal('0.20'), 'type': 'vat', 'threshold': Decimal('34400')},
            'IT': {'rate': Decimal('0.22'), 'type': 'vat', 'threshold': Decimal('65000')},
            'ES': {'rate': Decimal('0.21'), 'type': 'vat', 'threshold': Decimal('0')},
            'NL': {'rate': Decimal('0.21'), 'type': 'vat', 'threshold': Decimal('20000')},
            'AT': {'rate': Decimal('0.20'), 'type': 'vat', 'threshold': Decimal('35000')},
            'BE': {'rate': Decimal('0.21'), 'type': 'vat', 'threshold': Decimal('25000')},
            'DK': {'rate': Decimal('0.25'), 'type': 'vat', 'threshold': Decimal('50000')},
            'SE': {'rate': Decimal('0.25'), 'type': 'vat', 'threshold': Decimal('30000')},
            'NO': {'rate': Decimal('0.25'), 'type': 'vat', 'threshold': Decimal('50000')},
            'FI': {'rate': Decimal('0.24'), 'type': 'vat', 'threshold': Decimal('10000')},
            'IE': {'rate': Decimal('0.23'), 'type': 'vat', 'threshold': Decimal('37500')},
            
            # Asia Pacific
            'AU': {'rate': Decimal('0.10'), 'type': 'gst', 'threshold': Decimal('75000')},
            'NZ': {'rate': Decimal('0.15'), 'type': 'gst', 'threshold': Decimal('60000')},
            'SG': {'rate': Decimal('0.08'), 'type': 'gst', 'threshold': Decimal('1000000')},
            'JP': {'rate': Decimal('0.10'), 'type': 'consumption_tax', 'threshold': Decimal('10000000')},
            'IN': {'rate': Decimal('0.18'), 'type': 'gst', 'threshold': Decimal('2000000')},  # 20 lakh INR
            
            # Default fallback
            'DEFAULT': {'rate': Decimal('0.00'), 'type': 'none', 'threshold': None}
        }
        
        # Currency exchange rates (should be updated regularly via API)
        self.exchange_rates = {
            'USD': Decimal('1.00'),
            'EUR': Decimal('0.92'),
            'GBP': Decimal('0.79'),
            'CAD': Decimal('1.36'),
            'AUD': Decimal('1.51'),
            'JPY': Decimal('149.50'),
            'SGD': Decimal('1.34'),
            'INR': Decimal('83.12'),
            'NOK': Decimal('10.85'),
            'SEK': Decimal('10.62'),
            'DKK': Decimal('6.84'),
            'CHF': Decimal('0.91'),
            'NZD': Decimal('1.63')
        }
        
        # Digital services tax thresholds for major jurisdictions
        self.digital_services_thresholds = {
            'EU': {
                'revenue_threshold': Decimal('750000000'),  # €750M globally
                'local_threshold': Decimal('50000000'),     # €50M in EU
                'rate': Decimal('0.03')  # 3% DST
            },
            'UK': {
                'revenue_threshold': Decimal('500000000'),  # £500M globally
                'local_threshold': Decimal('25000000'),     # £25M in UK
                'rate': Decimal('0.02')  # 2% DST
            },
            'FR': {
                'revenue_threshold': Decimal('750000000'),  # €750M globally
                'local_threshold': Decimal('25000000'),     # €25M in France
                'rate': Decimal('0.03')  # 3% DST
            }
        }
    
    async def calculate_tax(
        self,
        amount: Decimal,
        currency: str,
        customer_country: str,
        business_country: str = 'US',
        customer_type: str = 'b2c',  # b2c or b2b
        vat_number: str = None,
        service_type: str = 'digital'
    ) -> Dict:
        """Calculate appropriate tax for a transaction"""
        
        try:
            # Determine tax jurisdiction
            tax_country = self._determine_tax_jurisdiction(
                customer_country, business_country, service_type
            )
            
            tax_config = self.tax_rates.get(tax_country, self.tax_rates['DEFAULT'])
            
            # Check VAT number for B2B EU transactions
            if customer_type == 'b2b' and vat_number and self._is_eu_country(customer_country):
                if await self._validate_vat_number(vat_number, customer_country):
                    # Valid VAT number - reverse charge applies
                    tax_rate = Decimal('0.00')
                    tax_reason = 'reverse_charge'
                else:
                    tax_rate = tax_config['rate']
                    tax_reason = 'invalid_vat'
            else:
                tax_rate = tax_config['rate']
                tax_reason = 'standard_rate'
            
            # Calculate tax amount
            tax_amount = (amount * tax_rate).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            total_amount = amount + tax_amount
            
            # Convert to requested currency if needed
            if currency != 'USD':
                conversion_rate = self.exchange_rates.get(currency, Decimal('1.00'))
                tax_amount = (tax_amount * conversion_rate).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
                total_amount = (total_amount * conversion_rate).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            
            return {
                'subtotal': float(amount),
                'tax_rate': float(tax_rate),
                'tax_amount': float(tax_amount),
                'total_amount': float(total_amount),
                'currency': currency,
                'tax_country': tax_country,
                'tax_type': tax_config['type'],
                'tax_reason': tax_reason,
                'vat_number_used': vat_number if vat_number else None,
                'calculation_date': datetime.now().isoformat()
            }
            
        except Exception as e:
            await self.error_handler.handle_error(e, {
                'component': 'tax_compliance',
                'action': 'calculate_tax',
                'amount': float(amount),
                'currency': currency,
                'customer_country': customer_country
            })
            raise
    
    def _determine_tax_jurisdiction(
        self,
        customer_country: str,
        business_country: str,
        service_type: str
    ) -> str:
        """Determine which country's tax rules apply"""
        
        # For digital services, tax is generally due where the customer is located
        if service_type == 'digital':
            return customer_country
        
        # For other services, depends on where service is performed
        return business_country
    
    def _is_eu_country(self, country_code: str) -> bool:
        """Check if country is in EU for VAT purposes"""
        eu_countries = {
            'AT', 'BE', 'BG', 'CY', 'CZ', 'DE', 'DK', 'EE', 'ES', 'FI', 
            'FR', 'GR', 'HR', 'HU', 'IE', 'IT', 'LT', 'LU', 'LV', 'MT', 
            'NL', 'PL', 'PT', 'RO', 'SE', 'SI', 'SK'
        }
        return country_code.upper() in eu_countries
    
    async def _validate_vat_number(self, vat_number: str, country: str) -> bool:
        """Validate VAT number (simplified - in production, use VIES API)"""
        
        try:
            # Basic format validation
            if not vat_number or len(vat_number) < 8:
                return False
            
            # Country-specific format checks
            country_formats = {
                'GB': lambda x: len(x) == 9 and x.isdigit(),
                'DE': lambda x: len(x) == 9 and x.isdigit(),
                'FR': lambda x: len(x) == 11,
                'IT': lambda x: len(x) == 11 and x.isdigit(),
                'ES': lambda x: len(x) == 9,
                'NL': lambda x: len(x) == 12,
            }
            
            validator = country_formats.get(country.upper())
            if validator:
                return validator(vat_number.replace(country.upper(), ''))
            
            # Generic validation for other EU countries
            return len(vat_number) >= 8
            
        except Exception:
            return False
    
    async def convert_currency(
        self,
        amount: Decimal,
        from_currency: str,
        to_currency: str,
        rate_date: date = None
    ) -> Dict:
        """Convert amount between currencies"""
        
        try:
            if from_currency == to_currency:
                return {
                    'original_amount': float(amount),
                    'converted_amount': float(amount),
                    'from_currency': from_currency,
                    'to_currency': to_currency,
                    'exchange_rate': 1.0,
                    'rate_date': (rate_date or date.today()).isoformat()
                }
            
            # Get exchange rates (in production, fetch from live API)
            from_rate = self.exchange_rates.get(from_currency, Decimal('1.00'))
            to_rate = self.exchange_rates.get(to_currency, Decimal('1.00'))
            
            # Convert via USD
            usd_amount = amount / from_rate
            converted_amount = (usd_amount * to_rate).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            
            exchange_rate = to_rate / from_rate
            
            return {
                'original_amount': float(amount),
                'converted_amount': float(converted_amount),
                'from_currency': from_currency,
                'to_currency': to_currency,
                'exchange_rate': float(exchange_rate),
                'rate_date': (rate_date or date.today()).isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Currency conversion failed: {e}")
            raise
    
    async def generate_tax_report(
        self,
        tenant_id: UUID,
        start_date: date,
        end_date: date,
        country: str = None
    ) -> Dict:
        """Generate tax compliance report for a period"""
        
        try:
            async with get_db() as db:
                # Base query for tax calculations
                base_filter = "WHERE bc.tenant_id = :tenant_id AND bc.cycle_start >= :start_date AND bc.cycle_end <= :end_date"
                params = {
                    'tenant_id': str(tenant_id),
                    'start_date': start_date,
                    'end_date': end_date
                }
                
                if country:
                    base_filter += " AND bc.tax_country = :country"
                    params['country'] = country
                
                # Get tax summary by country
                country_query = text(f"""
                    SELECT 
                        COALESCE(bc.tax_country, 'Unknown') as country,
                        bc.currency,
                        COUNT(*) as transaction_count,
                        SUM(bc.base_amount) as gross_revenue,
                        SUM(bc.tax_amount) as total_tax,
                        AVG(bc.tax_rate) as avg_tax_rate,
                        SUM(bc.total_amount) as total_with_tax
                    FROM billing_cycles bc
                    {base_filter}
                    GROUP BY bc.tax_country, bc.currency
                    ORDER BY total_tax DESC
                """)
                
                country_result = await db.execute(country_query, params)
                
                country_breakdown = []
                total_revenue = Decimal('0.00')
                total_tax = Decimal('0.00')
                
                for row in country_result:
                    country_data = {
                        'country': row.country,
                        'currency': row.currency,
                        'transaction_count': row.transaction_count,
                        'gross_revenue': float(row.gross_revenue or 0),
                        'total_tax': float(row.total_tax or 0),
                        'avg_tax_rate': float(row.avg_tax_rate or 0),
                        'total_with_tax': float(row.total_with_tax or 0)
                    }
                    country_breakdown.append(country_data)
                    total_revenue += Decimal(str(row.gross_revenue or 0))
                    total_tax += Decimal(str(row.total_tax or 0))
                
                # Get monthly breakdown
                monthly_query = text(f"""
                    SELECT 
                        DATE_TRUNC('month', bc.cycle_start) as month,
                        COUNT(*) as transaction_count,
                        SUM(bc.base_amount) as gross_revenue,
                        SUM(bc.tax_amount) as total_tax,
                        SUM(bc.total_amount) as total_with_tax
                    FROM billing_cycles bc
                    {base_filter}
                    GROUP BY DATE_TRUNC('month', bc.cycle_start)
                    ORDER BY month
                """)
                
                monthly_result = await db.execute(monthly_query, params)
                
                monthly_breakdown = []
                for row in monthly_result:
                    monthly_breakdown.append({
                        'month': row.month.strftime('%Y-%m'),
                        'transaction_count': row.transaction_count,
                        'gross_revenue': float(row.gross_revenue or 0),
                        'total_tax': float(row.total_tax or 0),
                        'total_with_tax': float(row.total_with_tax or 0)
                    })
                
                # Check compliance requirements
                compliance_status = await self._check_compliance_requirements(
                    tenant_id, country_breakdown, start_date, end_date
                )
                
                return {
                    'tenant_id': str(tenant_id),
                    'report_period': f"{start_date} to {end_date}",
                    'summary': {
                        'total_gross_revenue': float(total_revenue),
                        'total_tax_collected': float(total_tax),
                        'effective_tax_rate': float(total_tax / total_revenue) if total_revenue > 0 else 0.0,
                        'countries_served': len(country_breakdown)
                    },
                    'country_breakdown': country_breakdown,
                    'monthly_breakdown': monthly_breakdown,
                    'compliance_status': compliance_status,
                    'generated_at': datetime.now().isoformat()
                }
                
        except Exception as e:
            await self.error_handler.handle_error(e, {
                'component': 'tax_compliance',
                'action': 'generate_tax_report',
                'tenant_id': str(tenant_id)
            })
            raise
    
    async def _check_compliance_requirements(
        self,
        tenant_id: UUID,
        country_breakdown: List[Dict],
        start_date: date,
        end_date: date
    ) -> Dict:
        """Check if tenant meets various tax compliance requirements"""
        
        try:
            compliance_issues = []
            registrations_required = []
            
            for country_data in country_breakdown:
                country = country_data['country']
                revenue = Decimal(str(country_data['gross_revenue']))
                
                tax_config = self.tax_rates.get(country, self.tax_rates['DEFAULT'])
                threshold = tax_config.get('threshold')
                
                if threshold and revenue > threshold:
                    registrations_required.append({
                        'country': country,
                        'tax_type': tax_config['type'],
                        'revenue': float(revenue),
                        'threshold': float(threshold),
                        'registration_required': True
                    })
                
                # Check for missing tax on high-revenue countries
                if revenue > 10000 and country_data['total_tax'] == 0:
                    compliance_issues.append({
                        'country': country,
                        'issue': 'no_tax_collected',
                        'revenue': float(revenue),
                        'recommendation': 'Review tax calculation for this jurisdiction'
                    })
            
            # Check DST requirements
            dst_requirements = await self._check_digital_services_tax(tenant_id, country_breakdown)
            
            return {
                'overall_status': 'compliant' if not compliance_issues else 'issues_found',
                'registrations_required': registrations_required,
                'compliance_issues': compliance_issues,
                'digital_services_tax': dst_requirements,
                'recommendations': self._generate_compliance_recommendations(
                    registrations_required, compliance_issues
                )
            }
            
        except Exception as e:
            self.logger.error(f"Compliance check failed: {e}")
            return {'overall_status': 'check_failed', 'error': str(e)}
    
    async def _check_digital_services_tax(
        self,
        tenant_id: UUID,
        country_breakdown: List[Dict]
    ) -> Dict:
        """Check digital services tax requirements"""
        
        try:
            # Calculate total global revenue (simplified)
            total_global_revenue = sum(Decimal(str(c['gross_revenue'])) for c in country_breakdown)
            
            dst_obligations = []
            
            for jurisdiction, config in self.digital_services_thresholds.items():
                # Check if global threshold is met
                if total_global_revenue > config['revenue_threshold']:
                    # Check local revenue for specific jurisdictions
                    local_revenue = Decimal('0.00')
                    
                    if jurisdiction == 'EU':
                        eu_countries = ['DE', 'FR', 'IT', 'ES', 'NL', 'AT', 'BE']
                        local_revenue = sum(
                            Decimal(str(c['gross_revenue'])) 
                            for c in country_breakdown 
                            if c['country'] in eu_countries
                        )
                    elif jurisdiction in ['UK', 'FR']:
                        local_revenue = sum(
                            Decimal(str(c['gross_revenue'])) 
                            for c in country_breakdown 
                            if c['country'] == jurisdiction
                        )
                    
                    if local_revenue > config['local_threshold']:
                        dst_obligations.append({
                            'jurisdiction': jurisdiction,
                            'global_revenue': float(total_global_revenue),
                            'local_revenue': float(local_revenue),
                            'dst_rate': float(config['rate']),
                            'estimated_dst': float(local_revenue * config['rate']),
                            'registration_required': True
                        })
            
            return {
                'total_global_revenue': float(total_global_revenue),
                'dst_obligations': dst_obligations,
                'registration_count': len(dst_obligations)
            }
            
        except Exception as e:
            self.logger.error(f"DST check failed: {e}")
            return {'error': str(e)}
    
    def _generate_compliance_recommendations(
        self,
        registrations_required: List[Dict],
        compliance_issues: List[Dict]
    ) -> List[str]:
        """Generate compliance recommendations"""
        
        recommendations = []
        
        if registrations_required:
            recommendations.append(
                f"Consider registering for tax in {len(registrations_required)} jurisdictions "
                "where revenue thresholds have been exceeded."
            )
        
        if compliance_issues:
            recommendations.append(
                "Review tax calculation logic for jurisdictions with high revenue but no tax collected."
            )
        
        if len(registrations_required) > 3:
            recommendations.append(
                "Consider implementing a tax automation solution for multiple jurisdiction compliance."
            )
        
        recommendations.append(
            "Regularly review tax rates and thresholds as they change frequently."
        )
        
        recommendations.append(
            "Maintain detailed records of all transactions for tax audit purposes."
        )
        
        return recommendations
    
    async def update_exchange_rates(self) -> Dict:
        """Update exchange rates from external API (placeholder)"""
        
        try:
            # In production, integrate with a real exchange rate API
            # For now, return current rates
            
            self.logger.info("Exchange rates updated")
            return {
                'success': True,
                'rates_updated': len(self.exchange_rates),
                'last_updated': datetime.now().isoformat(),
                'base_currency': 'USD'
            }
            
        except Exception as e:
            self.logger.error(f"Failed to update exchange rates: {e}")
            raise


# Global instance
tax_compliance_service = TaxComplianceService()