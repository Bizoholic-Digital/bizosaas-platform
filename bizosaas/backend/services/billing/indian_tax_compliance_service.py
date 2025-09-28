"""
Indian Tax and GST Compliance Service
Handles GST calculation, invoice generation, and Indian tax compliance
Critical for operating in the Indian market with proper tax compliance
"""

import asyncio
import logging
import json
from datetime import datetime, date, timedelta
from decimal import Decimal, ROUND_HALF_UP
from enum import Enum
from typing import Dict, List, Optional, Union, Tuple
from uuid import UUID, uuid4

from sqlalchemy import text, select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from core.error_handler import ErrorHandler


class GSTRate(Enum):
    """GST rates for different service categories"""
    DIGITAL_SERVICES = Decimal('18.00')  # 18% for digital marketing services
    SAAS_SERVICES = Decimal('18.00')     # 18% for SaaS platforms
    MARKETPLACE_COMMISSION = Decimal('18.00')  # 18% for marketplace commissions
    CONSULTATION = Decimal('18.00')      # 18% for consultation services
    ZERO_RATED = Decimal('0.00')         # 0% for exports
    EXEMPTED = Decimal('0.00')           # Exempted services


class TaxType(Enum):
    CGST = "cgst"  # Central GST
    SGST = "sgst"  # State GST
    IGST = "igst"  # Integrated GST
    CESS = "cess"  # Additional Cess


class BusinessType(Enum):
    REGULAR = "regular"
    COMPOSITION = "composition"
    UNREGISTERED = "unregistered"
    EXPORT = "export"
    SEZ = "sez"


class InvoiceType(Enum):
    TAX_INVOICE = "tax_invoice"
    BILL_OF_SUPPLY = "bill_of_supply"
    RECEIPT_VOUCHER = "receipt_voucher"
    DEBIT_NOTE = "debit_note"
    CREDIT_NOTE = "credit_note"


class IndianState(Enum):
    """Indian states with their GST state codes"""
    ANDHRA_PRADESH = {"name": "Andhra Pradesh", "code": "37"}
    ARUNACHAL_PRADESH = {"name": "Arunachal Pradesh", "code": "12"}
    ASSAM = {"name": "Assam", "code": "18"}
    BIHAR = {"name": "Bihar", "code": "10"}
    CHHATTISGARH = {"name": "Chhattisgarh", "code": "22"}
    GOA = {"name": "Goa", "code": "30"}
    GUJARAT = {"name": "Gujarat", "code": "24"}
    HARYANA = {"name": "Haryana", "code": "06"}
    HIMACHAL_PRADESH = {"name": "Himachal Pradesh", "code": "02"}
    JHARKHAND = {"name": "Jharkhand", "code": "20"}
    KARNATAKA = {"name": "Karnataka", "code": "29"}
    KERALA = {"name": "Kerala", "code": "32"}
    MADHYA_PRADESH = {"name": "Madhya Pradesh", "code": "23"}
    MAHARASHTRA = {"name": "Maharashtra", "code": "27"}
    MANIPUR = {"name": "Manipur", "code": "14"}
    MEGHALAYA = {"name": "Meghalaya", "code": "17"}
    MIZORAM = {"name": "Mizoram", "code": "15"}
    NAGALAND = {"name": "Nagaland", "code": "13"}
    ODISHA = {"name": "Odisha", "code": "21"}
    PUNJAB = {"name": "Punjab", "code": "03"}
    RAJASTHAN = {"name": "Rajasthan", "code": "08"}
    SIKKIM = {"name": "Sikkim", "code": "11"}
    TAMIL_NADU = {"name": "Tamil Nadu", "code": "33"}
    TELANGANA = {"name": "Telangana", "code": "36"}
    TRIPURA = {"name": "Tripura", "code": "16"}
    UTTAR_PRADESH = {"name": "Uttar Pradesh", "code": "09"}
    UTTARAKHAND = {"name": "Uttarakhand", "code": "05"}
    WEST_BENGAL = {"name": "West Bengal", "code": "19"}
    # Union Territories
    DELHI = {"name": "Delhi", "code": "07"}
    CHANDIGARH = {"name": "Chandigarh", "code": "04"}
    JAMMU_KASHMIR = {"name": "Jammu & Kashmir", "code": "01"}
    LADAKH = {"name": "Ladakh", "code": "38"}
    PUDUCHERRY = {"name": "Puducherry", "code": "34"}
    LAKSHADWEEP = {"name": "Lakshadweep", "code": "31"}
    ANDAMAN_NICOBAR = {"name": "Andaman & Nicobar", "code": "35"}


class GSTTaxCalculator:
    """Calculate GST taxes for Indian transactions"""
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.gst_calculator")
    
    def calculate_gst(
        self,
        amount: Decimal,
        gst_rate: GSTRate,
        supplier_state: IndianState,
        recipient_state: IndianState,
        is_export: bool = False,
        is_composition: bool = False
    ) -> Dict:
        """Calculate GST breakdown for a transaction"""
        
        try:
            base_amount = amount
            gst_percentage = gst_rate.value
            
            # For exports, GST is zero
            if is_export:
                return {
                    "base_amount": float(base_amount),
                    "gst_rate": 0.00,
                    "cgst": 0.00,
                    "sgst": 0.00,
                    "igst": 0.00,
                    "cess": 0.00,
                    "total_gst": 0.00,
                    "total_amount": float(base_amount),
                    "tax_type": "export_zero_rated"
                }
            
            # For composition scheme, simplified tax
            if is_composition:
                # Composition dealers pay a fixed rate (typically 1% for services)
                composition_rate = Decimal('1.00')
                total_tax = (base_amount * composition_rate / 100).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
                
                return {
                    "base_amount": float(base_amount),
                    "gst_rate": float(composition_rate),
                    "cgst": 0.00,
                    "sgst": 0.00,
                    "igst": float(total_tax),
                    "cess": 0.00,
                    "total_gst": float(total_tax),
                    "total_amount": float(base_amount + total_tax),
                    "tax_type": "composition"
                }
            
            # Calculate tax amount
            total_gst_amount = (base_amount * gst_percentage / 100).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            
            # Determine CGST/SGST vs IGST based on state
            supplier_code = supplier_state.value["code"]
            recipient_code = recipient_state.value["code"]
            
            if supplier_code == recipient_code:
                # Intra-state transaction: CGST + SGST
                cgst = (total_gst_amount / 2).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
                sgst = total_gst_amount - cgst  # To handle rounding differences
                igst = Decimal('0.00')
                tax_type = "intra_state"
            else:
                # Inter-state transaction: IGST
                cgst = Decimal('0.00')
                sgst = Decimal('0.00')
                igst = total_gst_amount
                tax_type = "inter_state"
            
            # CESS calculation (if applicable - currently 0 for digital services)
            cess = Decimal('0.00')
            
            total_amount = base_amount + total_gst_amount + cess
            
            return {
                "base_amount": float(base_amount),
                "gst_rate": float(gst_percentage),
                "cgst": float(cgst),
                "sgst": float(sgst),
                "igst": float(igst),
                "cess": float(cess),
                "total_gst": float(total_gst_amount),
                "total_amount": float(total_amount),
                "tax_type": tax_type
            }
            
        except Exception as e:
            self.logger.error(f"GST calculation failed: {e}")
            raise
    
    def calculate_reverse_charge(
        self,
        amount: Decimal,
        gst_rate: GSTRate,
        supplier_state: IndianState,
        recipient_state: IndianState
    ) -> Dict:
        """Calculate reverse charge mechanism for applicable transactions"""
        
        # Reverse charge applies when recipient is registered and supplier is unregistered
        # Or for specific categories like legal services, etc.
        
        try:
            base_amount = amount
            gst_percentage = gst_rate.value
            
            # Under reverse charge, the recipient pays the tax
            total_gst_amount = (base_amount * gst_percentage / 100).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            
            # Determine CGST/SGST vs IGST
            supplier_code = supplier_state.value["code"]
            recipient_code = recipient_state.value["code"]
            
            if supplier_code == recipient_code:
                cgst = (total_gst_amount / 2).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
                sgst = total_gst_amount - cgst
                igst = Decimal('0.00')
            else:
                cgst = Decimal('0.00')
                sgst = Decimal('0.00')
                igst = total_gst_amount
            
            return {
                "base_amount": float(base_amount),
                "gst_rate": float(gst_percentage),
                "cgst": float(cgst),
                "sgst": float(sgst),
                "igst": float(igst),
                "total_gst": float(total_gst_amount),
                "total_amount": float(base_amount),  # Supplier doesn't charge GST
                "reverse_charge_amount": float(total_gst_amount),
                "tax_type": "reverse_charge"
            }
            
        except Exception as e:
            self.logger.error(f"Reverse charge calculation failed: {e}")
            raise


class IndianInvoiceGenerator:
    """Generate GST compliant invoices for Indian market"""
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.invoice_generator")
        self.gst_calculator = GSTTaxCalculator()
    
    async def generate_invoice(
        self,
        tenant_id: UUID,
        invoice_data: Dict,
        invoice_type: InvoiceType = InvoiceType.TAX_INVOICE
    ) -> Dict:
        """Generate GST compliant invoice"""
        
        try:
            # Get tenant GST information
            tenant_gst_info = await self._get_tenant_gst_info(tenant_id)
            
            if not tenant_gst_info:
                raise ValueError("Tenant GST information not found")
            
            # Generate invoice number
            invoice_number = await self._generate_invoice_number(tenant_id, invoice_type)
            
            # Calculate taxes for each line item
            invoice_lines = []
            total_base_amount = Decimal('0.00')
            total_cgst = Decimal('0.00')
            total_sgst = Decimal('0.00')
            total_igst = Decimal('0.00')
            total_cess = Decimal('0.00')
            
            for line_item in invoice_data.get("line_items", []):
                gst_rate = GSTRate(line_item.get("gst_rate", "DIGITAL_SERVICES"))
                amount = Decimal(str(line_item["amount"]))
                
                # Determine states
                supplier_state = IndianState(tenant_gst_info["state"])
                recipient_state = IndianState(invoice_data.get("recipient_state", "MAHARASHTRA"))
                
                # Calculate GST
                tax_calculation = self.gst_calculator.calculate_gst(
                    amount=amount,
                    gst_rate=gst_rate,
                    supplier_state=supplier_state,
                    recipient_state=recipient_state,
                    is_export=invoice_data.get("is_export", False),
                    is_composition=tenant_gst_info.get("is_composition", False)
                )
                
                line_item_data = {
                    "description": line_item["description"],
                    "quantity": line_item.get("quantity", 1),
                    "unit_price": float(amount),
                    "hsn_sac_code": line_item.get("hsn_sac_code", "998314"),  # SAC for digital marketing
                    "tax_calculation": tax_calculation
                }
                
                invoice_lines.append(line_item_data)
                
                # Accumulate totals
                total_base_amount += amount
                total_cgst += Decimal(str(tax_calculation["cgst"]))
                total_sgst += Decimal(str(tax_calculation["sgst"]))
                total_igst += Decimal(str(tax_calculation["igst"]))
                total_cess += Decimal(str(tax_calculation["cess"]))
            
            total_gst = total_cgst + total_sgst + total_igst + total_cess
            grand_total = total_base_amount + total_gst
            
            # Generate invoice
            invoice = {
                "invoice_number": invoice_number,
                "invoice_type": invoice_type.value,
                "invoice_date": invoice_data.get("invoice_date", date.today().isoformat()),
                "due_date": invoice_data.get("due_date", (date.today() + timedelta(days=30)).isoformat()),
                
                # Supplier information
                "supplier": {
                    "name": tenant_gst_info["business_name"],
                    "gstin": tenant_gst_info["gstin"],
                    "pan": tenant_gst_info["pan"],
                    "address": tenant_gst_info["address"],
                    "state": tenant_gst_info["state"],
                    "state_code": IndianState(tenant_gst_info["state"]).value["code"],
                    "email": tenant_gst_info.get("email"),
                    "phone": tenant_gst_info.get("phone")
                },
                
                # Recipient information
                "recipient": {
                    "name": invoice_data["recipient_name"],
                    "gstin": invoice_data.get("recipient_gstin"),
                    "pan": invoice_data.get("recipient_pan"),
                    "address": invoice_data.get("recipient_address"),
                    "state": invoice_data.get("recipient_state"),
                    "state_code": IndianState(invoice_data.get("recipient_state", "MAHARASHTRA")).value["code"],
                    "email": invoice_data.get("recipient_email"),
                    "phone": invoice_data.get("recipient_phone")
                },
                
                # Invoice details
                "line_items": invoice_lines,
                "totals": {
                    "base_amount": float(total_base_amount),
                    "cgst": float(total_cgst),
                    "sgst": float(total_sgst),
                    "igst": float(total_igst),
                    "cess": float(total_cess),
                    "total_gst": float(total_gst),
                    "grand_total": float(grand_total),
                    "amount_in_words": self._amount_to_words(grand_total)
                },
                
                # Additional information
                "place_of_supply": invoice_data.get("recipient_state", "Maharashtra"),
                "currency": "INR",
                "terms_conditions": invoice_data.get("terms_conditions", "Payment due within 30 days"),
                "notes": invoice_data.get("notes"),
                
                # Compliance information
                "irn": None,  # Invoice Reference Number (for B2B invoices above ₹5 Cr)
                "ack_no": None,  # Acknowledgment number from GST portal
                "ack_date": None,
                "qr_code_data": self._generate_qr_code_data(invoice_number, grand_total, invoice_data.get("invoice_date"))
            }
            
            # Store invoice in database
            invoice_id = await self._store_invoice(tenant_id, invoice)
            invoice["internal_invoice_id"] = str(invoice_id)
            
            self.logger.info(f"Invoice generated: {invoice_number} for tenant {tenant_id}")
            
            return {
                "success": True,
                "invoice": invoice
            }
            
        except Exception as e:
            self.logger.error(f"Invoice generation failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _get_tenant_gst_info(self, tenant_id: UUID) -> Optional[Dict]:
        """Get tenant GST information from database"""
        
        try:
            async with get_db() as db:
                query = text("""
                    SELECT 
                        business_name, gstin, pan, address_line1, address_line2,
                        city, state, pincode, email, phone, is_composition_dealer
                    FROM tenant_tax_info 
                    WHERE tenant_id = :tenant_id AND status = 'active'
                    LIMIT 1
                """)
                
                result = await db.execute(query, {"tenant_id": str(tenant_id)})
                row = result.first()
                
                if row:
                    return {
                        "business_name": row.business_name,
                        "gstin": row.gstin,
                        "pan": row.pan,
                        "address": f"{row.address_line1}, {row.address_line2 or ''}, {row.city}, {row.state} - {row.pincode}".strip(),
                        "state": row.state,
                        "email": row.email,
                        "phone": row.phone,
                        "is_composition": row.is_composition_dealer or False
                    }
                
                return None
                
        except Exception as e:
            self.logger.error(f"Failed to get tenant GST info: {e}")
            return None
    
    async def _generate_invoice_number(self, tenant_id: UUID, invoice_type: InvoiceType) -> str:
        """Generate sequential invoice number"""
        
        try:
            async with get_db() as db:
                # Get current financial year
                today = date.today()
                if today.month >= 4:  # April to March financial year
                    fy_start = date(today.year, 4, 1)
                    fy_end = date(today.year + 1, 3, 31)
                    fy_suffix = f"{today.year}-{str(today.year + 1)[2:]}"
                else:
                    fy_start = date(today.year - 1, 4, 1)
                    fy_end = date(today.year, 3, 31)
                    fy_suffix = f"{today.year - 1}-{str(today.year)[2:]}"
                
                # Get next sequence number
                query = text("""
                    SELECT COALESCE(MAX(sequence_number), 0) + 1 as next_sequence
                    FROM invoices 
                    WHERE tenant_id = :tenant_id 
                    AND invoice_date >= :fy_start 
                    AND invoice_date <= :fy_end
                """)
                
                result = await db.execute(query, {
                    "tenant_id": str(tenant_id),
                    "fy_start": fy_start,
                    "fy_end": fy_end
                })
                
                next_sequence = result.scalar() or 1
                
                # Generate invoice number format: INV-FY-XXXX
                invoice_number = f"INV-{fy_suffix}-{next_sequence:04d}"
                
                return invoice_number
                
        except Exception as e:
            self.logger.error(f"Invoice number generation failed: {e}")
            # Fallback to UUID-based number
            return f"INV-{uuid4().hex[:8].upper()}"
    
    def _amount_to_words(self, amount: Decimal) -> str:
        """Convert amount to words (Indian numbering system)"""
        
        # This is a simplified implementation
        # In production, use a proper Indian numbering system library
        
        try:
            amount_int = int(amount)
            amount_decimal = int((amount - amount_int) * 100)
            
            # Basic number to words conversion
            ones = ['', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine']
            teens = ['Ten', 'Eleven', 'Twelve', 'Thirteen', 'Fourteen', 'Fifteen', 'Sixteen', 'Seventeen', 'Eighteen', 'Nineteen']
            tens = ['', '', 'Twenty', 'Thirty', 'Forty', 'Fifty', 'Sixty', 'Seventy', 'Eighty', 'Ninety']
            
            def convert_hundreds(n):
                result = []
                if n >= 100:
                    result.append(ones[n // 100])
                    result.append('Hundred')
                    n %= 100
                if n >= 20:
                    result.append(tens[n // 10])
                    n %= 10
                elif n >= 10:
                    result.append(teens[n - 10])
                    n = 0
                if n > 0:
                    result.append(ones[n])
                return ' '.join(result)
            
            if amount_int == 0:
                words = "Zero"
            elif amount_int < 1000:
                words = convert_hundreds(amount_int)
            else:
                # Simplified for demo - proper Indian numbering would handle lakhs, crores
                words = f"Rupees {convert_hundreds(amount_int)}"
            
            if amount_decimal > 0:
                words += f" and {convert_hundreds(amount_decimal)} Paise"
            
            return f"{words} Only"
            
        except Exception:
            return f"Rupees {float(amount):.2f} Only"
    
    def _generate_qr_code_data(self, invoice_number: str, amount: Decimal, invoice_date: str) -> str:
        """Generate QR code data for GST invoice"""
        
        # GST QR code format
        qr_data = f"Invoice:{invoice_number}|Date:{invoice_date}|Amount:{amount}"
        return qr_data
    
    async def _store_invoice(self, tenant_id: UUID, invoice_data: Dict) -> UUID:
        """Store invoice in database"""
        
        try:
            async with get_db() as db:
                query = text("""
                    INSERT INTO invoices (
                        tenant_id, invoice_number, invoice_type, invoice_date, due_date,
                        recipient_name, recipient_gstin, base_amount, cgst_amount,
                        sgst_amount, igst_amount, total_amount, currency, status, invoice_data
                    ) VALUES (
                        :tenant_id::UUID, :invoice_number, :invoice_type, :invoice_date, :due_date,
                        :recipient_name, :recipient_gstin, :base_amount, :cgst_amount,
                        :sgst_amount, :igst_amount, :total_amount, :currency, 'generated', :invoice_data::JSONB
                    ) RETURNING id
                """)
                
                result = await db.execute(query, {
                    "tenant_id": str(tenant_id),
                    "invoice_number": invoice_data["invoice_number"],
                    "invoice_type": invoice_data["invoice_type"],
                    "invoice_date": invoice_data["invoice_date"],
                    "due_date": invoice_data["due_date"],
                    "recipient_name": invoice_data["recipient"]["name"],
                    "recipient_gstin": invoice_data["recipient"].get("gstin"),
                    "base_amount": invoice_data["totals"]["base_amount"],
                    "cgst_amount": invoice_data["totals"]["cgst"],
                    "sgst_amount": invoice_data["totals"]["sgst"],
                    "igst_amount": invoice_data["totals"]["igst"],
                    "total_amount": invoice_data["totals"]["grand_total"],
                    "currency": invoice_data["currency"],
                    "invoice_data": json.dumps(invoice_data)
                })
                
                invoice_id = result.scalar()
                await db.commit()
                
                return UUID(invoice_id)
                
        except Exception as e:
            self.logger.error(f"Failed to store invoice: {e}")
            raise


class IndianTaxComplianceService:
    """Main service for Indian tax compliance"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.error_handler = ErrorHandler()
        self.gst_calculator = GSTTaxCalculator()
        self.invoice_generator = IndianInvoiceGenerator()
    
    async def setup_tenant_gst_info(
        self,
        tenant_id: UUID,
        gst_info: Dict
    ) -> Dict:
        """Setup or update tenant GST information"""
        
        try:
            # Validate GST number
            gstin = gst_info.get("gstin")
            if gstin and not self._validate_gstin(gstin):
                return {
                    "success": False,
                    "error": "Invalid GSTIN format"
                }
            
            # Validate PAN
            pan = gst_info.get("pan")
            if pan and not self._validate_pan(pan):
                return {
                    "success": False,
                    "error": "Invalid PAN format"
                }
            
            async with get_db() as db:
                # Check if GST info already exists
                check_query = text("""
                    SELECT id FROM tenant_tax_info 
                    WHERE tenant_id = :tenant_id
                """)
                
                existing = await db.execute(check_query, {"tenant_id": str(tenant_id)})
                
                if existing.first():
                    # Update existing record
                    update_query = text("""
                        UPDATE tenant_tax_info SET
                            business_name = :business_name,
                            gstin = :gstin,
                            pan = :pan,
                            address_line1 = :address_line1,
                            address_line2 = :address_line2,
                            city = :city,
                            state = :state,
                            pincode = :pincode,
                            email = :email,
                            phone = :phone,
                            is_composition_dealer = :is_composition_dealer,
                            updated_at = NOW()
                        WHERE tenant_id = :tenant_id
                        RETURNING id
                    """)
                else:
                    # Insert new record
                    update_query = text("""
                        INSERT INTO tenant_tax_info (
                            tenant_id, business_name, gstin, pan, address_line1, address_line2,
                            city, state, pincode, email, phone, is_composition_dealer, status
                        ) VALUES (
                            :tenant_id::UUID, :business_name, :gstin, :pan, :address_line1, :address_line2,
                            :city, :state, :pincode, :email, :phone, :is_composition_dealer, 'active'
                        ) RETURNING id
                    """)
                
                result = await db.execute(update_query, {
                    "tenant_id": str(tenant_id),
                    "business_name": gst_info["business_name"],
                    "gstin": gstin,
                    "pan": pan,
                    "address_line1": gst_info["address_line1"],
                    "address_line2": gst_info.get("address_line2"),
                    "city": gst_info["city"],
                    "state": gst_info["state"],
                    "pincode": gst_info["pincode"],
                    "email": gst_info.get("email"),
                    "phone": gst_info.get("phone"),
                    "is_composition_dealer": gst_info.get("is_composition_dealer", False)
                })
                
                tax_info_id = result.scalar()
                await db.commit()
                
                return {
                    "success": True,
                    "tax_info_id": str(tax_info_id),
                    "message": "GST information updated successfully"
                }
                
        except Exception as e:
            await self.error_handler.handle_error(e, {
                "component": "indian_tax_compliance",
                "action": "setup_gst_info",
                "tenant_id": str(tenant_id)
            })
            return {
                "success": False,
                "error": str(e)
            }
    
    async def calculate_payment_tax(
        self,
        tenant_id: UUID,
        payment_data: Dict
    ) -> Dict:
        """Calculate tax for a payment transaction"""
        
        try:
            # Get tenant GST info
            tenant_gst_info = await self.invoice_generator._get_tenant_gst_info(tenant_id)
            
            if not tenant_gst_info:
                return {
                    "success": False,
                    "error": "Tenant GST information not configured"
                }
            
            amount = Decimal(str(payment_data["amount"]))
            service_type = payment_data.get("service_type", "digital_services")
            
            # Determine GST rate based on service type
            gst_rate_mapping = {
                "digital_services": GSTRate.DIGITAL_SERVICES,
                "saas_services": GSTRate.SAAS_SERVICES,
                "marketplace_commission": GSTRate.MARKETPLACE_COMMISSION,
                "consultation": GSTRate.CONSULTATION
            }
            
            gst_rate = gst_rate_mapping.get(service_type, GSTRate.DIGITAL_SERVICES)
            
            # Determine states
            supplier_state = IndianState(tenant_gst_info["state"])
            recipient_state = IndianState(payment_data.get("customer_state", "MAHARASHTRA"))
            
            # Calculate GST
            tax_calculation = self.gst_calculator.calculate_gst(
                amount=amount,
                gst_rate=gst_rate,
                supplier_state=supplier_state,
                recipient_state=recipient_state,
                is_export=payment_data.get("is_export", False),
                is_composition=tenant_gst_info.get("is_composition", False)
            )
            
            return {
                "success": True,
                "tax_calculation": tax_calculation,
                "service_type": service_type,
                "gst_rate": gst_rate.value
            }
            
        except Exception as e:
            await self.error_handler.handle_error(e, {
                "component": "indian_tax_compliance",
                "action": "calculate_payment_tax",
                "tenant_id": str(tenant_id)
            })
            return {
                "success": False,
                "error": str(e)
            }
    
    async def generate_gst_invoice(
        self,
        tenant_id: UUID,
        invoice_data: Dict
    ) -> Dict:
        """Generate GST compliant invoice"""
        
        try:
            result = await self.invoice_generator.generate_invoice(
                tenant_id=tenant_id,
                invoice_data=invoice_data,
                invoice_type=InvoiceType(invoice_data.get("invoice_type", "tax_invoice"))
            )
            
            return result
            
        except Exception as e:
            await self.error_handler.handle_error(e, {
                "component": "indian_tax_compliance",
                "action": "generate_gst_invoice",
                "tenant_id": str(tenant_id)
            })
            return {
                "success": False,
                "error": str(e)
            }
    
    async def get_gst_return_data(
        self,
        tenant_id: UUID,
        return_period: str
    ) -> Dict:
        """Generate GST return data for a period"""
        
        try:
            # Parse return period (format: MMYYYY)
            month = int(return_period[:2])
            year = int(return_period[2:])
            
            start_date = date(year, month, 1)
            if month == 12:
                end_date = date(year + 1, 1, 1) - timedelta(days=1)
            else:
                end_date = date(year, month + 1, 1) - timedelta(days=1)
            
            async with get_db() as db:
                # Get sales data
                sales_query = text("""
                    SELECT 
                        SUM(base_amount) as total_taxable_value,
                        SUM(cgst_amount) as total_cgst,
                        SUM(sgst_amount) as total_sgst,
                        SUM(igst_amount) as total_igst,
                        COUNT(*) as total_invoices,
                        currency
                    FROM invoices 
                    WHERE tenant_id = :tenant_id
                    AND invoice_date BETWEEN :start_date AND :end_date
                    AND status IN ('generated', 'sent', 'paid')
                    GROUP BY currency
                """)
                
                sales_result = await db.execute(sales_query, {
                    "tenant_id": str(tenant_id),
                    "start_date": start_date,
                    "end_date": end_date
                })
                
                sales_data = []
                for row in sales_result:
                    sales_data.append({
                        "currency": row.currency,
                        "total_taxable_value": float(row.total_taxable_value or 0),
                        "total_cgst": float(row.total_cgst or 0),
                        "total_sgst": float(row.total_sgst or 0),
                        "total_igst": float(row.total_igst or 0),
                        "total_invoices": row.total_invoices
                    })
                
                return {
                    "success": True,
                    "return_period": return_period,
                    "period_start": start_date.isoformat(),
                    "period_end": end_date.isoformat(),
                    "sales_data": sales_data,
                    "generated_at": datetime.now().isoformat()
                }
                
        except Exception as e:
            await self.error_handler.handle_error(e, {
                "component": "indian_tax_compliance",
                "action": "get_gst_return_data",
                "tenant_id": str(tenant_id),
                "return_period": return_period
            })
            return {
                "success": False,
                "error": str(e)
            }
    
    def _validate_gstin(self, gstin: str) -> bool:
        """Validate GSTIN format"""
        
        if not gstin or len(gstin) != 15:
            return False
        
        # GSTIN format: XXXXXAXXXXAXXA
        # Where X = alphanumeric, A = alphabet
        import re
        pattern = r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}[Z]{1}[0-9A-Z]{1}$'
        
        return bool(re.match(pattern, gstin))
    
    def _validate_pan(self, pan: str) -> bool:
        """Validate PAN format"""
        
        if not pan or len(pan) != 10:
            return False
        
        # PAN format: AAAAA9999A
        import re
        pattern = r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$'
        
        return bool(re.match(pattern, pan))
    
    async def get_compliance_health(self, tenant_id: UUID) -> Dict:
        """Get tax compliance health status"""
        
        try:
            async with get_db() as db:
                # Check GST registration status
                gst_query = text("""
                    SELECT gstin, is_composition_dealer, status
                    FROM tenant_tax_info 
                    WHERE tenant_id = :tenant_id
                """)
                
                gst_result = await db.execute(gst_query, {"tenant_id": str(tenant_id)})
                gst_info = gst_result.first()
                
                # Check recent invoice generation
                invoice_query = text("""
                    SELECT COUNT(*) as invoice_count
                    FROM invoices 
                    WHERE tenant_id = :tenant_id
                    AND invoice_date >= :last_month
                """)
                
                last_month = date.today() - timedelta(days=30)
                invoice_result = await db.execute(invoice_query, {
                    "tenant_id": str(tenant_id),
                    "last_month": last_month
                })
                
                invoice_count = invoice_result.scalar() or 0
                
                compliance_status = {
                    "gst_registered": bool(gst_info and gst_info.gstin),
                    "composition_scheme": bool(gst_info and gst_info.is_composition_dealer),
                    "recent_invoices": invoice_count,
                    "compliance_score": 0
                }
                
                # Calculate compliance score
                score = 0
                if compliance_status["gst_registered"]:
                    score += 50
                if compliance_status["recent_invoices"] > 0:
                    score += 30
                if gst_info and gst_info.status == "active":
                    score += 20
                
                compliance_status["compliance_score"] = score
                compliance_status["status"] = "compliant" if score >= 70 else "needs_attention"
                
                return {
                    "success": True,
                    "compliance_status": compliance_status
                }
                
        except Exception as e:
            self.logger.error(f"Compliance health check failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }


# Global instance
indian_tax_service = IndianTaxComplianceService()