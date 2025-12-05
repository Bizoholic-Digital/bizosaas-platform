"""
Medusa.js Integration for Cross-Platform Billing
Unified customer and transaction management across Bizoholic and CoreLDove platforms
"""

import asyncio
import logging
from datetime import datetime
from decimal import Decimal
from typing import Dict, List, Optional, Union
from uuid import UUID
import httpx

from sqlalchemy import text
from database import get_db
from core.error_handler import ErrorHandler


class MedusaBillingIntegration:
    """Integration service for Medusa.js e-commerce backend"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.error_handler = ErrorHandler()
        
        # Medusa.js configuration
        self.medusa_base_url = self._get_medusa_url()
        self.medusa_api_key = self._get_medusa_api_key()
        
        # HTTP client for Medusa API calls
        self.client = httpx.AsyncClient(
            base_url=self.medusa_base_url,
            headers={
                'Authorization': f'Bearer {self.medusa_api_key}',
                'Content-Type': 'application/json'
            },
            timeout=30.0
        )
    
    def _get_medusa_url(self) -> str:
        """Get Medusa.js backend URL"""
        import os
        return os.getenv('MEDUSA_BACKEND_URL', 'http://localhost:9000')
    
    def _get_medusa_api_key(self) -> str:
        """Get Medusa.js API key"""
        import os
        return os.getenv('MEDUSA_API_KEY', '')
    
    async def sync_customer_data(
        self,
        tenant_id: UUID,
        customer_data: Dict
    ) -> Dict[str, Union[str, bool]]:
        """Sync customer data between platforms"""
        try:
            # Check if unified customer already exists
            unified_customer = await self._get_unified_customer(customer_data['email'])
            
            if unified_customer:
                # Update existing unified customer
                await self._update_unified_customer(unified_customer['id'], customer_data)
                return {
                    'success': True,
                    'unified_customer_id': unified_customer['id'],
                    'action': 'updated'
                }
            else:
                # Create new unified customer
                unified_customer_id = await self._create_unified_customer(tenant_id, customer_data)
                return {
                    'success': True,
                    'unified_customer_id': str(unified_customer_id),
                    'action': 'created'
                }
                
        except Exception as e:
            await self.error_handler.handle_error(e, {
                'component': 'medusa_billing_integration',
                'action': 'sync_customer_data',
                'tenant_id': str(tenant_id)
            })
            raise
    
    async def create_coreldove_order(
        self,
        customer_email: str,
        products: List[Dict],
        shipping_address: Dict,
        billing_address: Dict = None
    ) -> Dict:
        """Create order in CoreLDove (Medusa.js) system"""
        try:
            # Get or create Medusa customer
            medusa_customer = await self._get_or_create_medusa_customer(customer_email)
            
            # Create cart
            cart_data = {
                'customer_id': medusa_customer['id'],
                'region_id': await self._get_default_region_id(),
                'items': products
            }
            
            cart = await self._create_medusa_cart(cart_data)
            
            # Add shipping and billing addresses
            if shipping_address:
                await self._add_shipping_address(cart['id'], shipping_address)
            
            if billing_address:
                await self._add_billing_address(cart['id'], billing_address)
            
            # Complete cart to create order
            order = await self._complete_cart(cart['id'])
            
            # Record transaction in unified system
            await self._record_unified_transaction({
                'tenant_id': await self._get_tenant_from_email(customer_email),
                'customer_email': customer_email,
                'platform': 'coreldove',
                'transaction_type': 'product_purchase',
                'external_id': order['id'],
                'amount': Decimal(str(order['total'] / 100)),  # Convert from cents
                'currency': order['currency_code'],
                'status': order['status'],
                'description': f"CoreLDove Order #{order['display_id']}",
                'metadata': {
                    'order_id': order['id'],
                    'product_count': len(products),
                    'region': order['region']['name'] if order.get('region') else 'Unknown'
                }
            })
            
            return {
                'success': True,
                'order_id': order['id'],
                'order_number': order['display_id'],
                'total_amount': order['total'] / 100,
                'status': order['status']
            }
            
        except Exception as e:
            await self.error_handler.handle_error(e, {
                'component': 'medusa_billing_integration',
                'action': 'create_coreldove_order',
                'customer_email': customer_email
            })
            raise
    
    async def process_bizoholic_subscription_payment(
        self,
        tenant_id: UUID,
        customer_email: str,
        amount: Decimal,
        description: str,
        metadata: Dict = None
    ) -> Dict:
        """Process subscription payment for Bizoholic platform"""
        try:
            # Record unified transaction
            transaction_id = await self._record_unified_transaction({
                'tenant_id': tenant_id,
                'customer_email': customer_email,
                'platform': 'bizoholic',
                'transaction_type': 'subscription',
                'amount': amount,
                'currency': 'USD',
                'status': 'completed',
                'description': description,
                'metadata': metadata or {}
            })
            
            # Update customer lifetime value
            await self._update_customer_ltv(customer_email, amount, 'bizoholic')
            
            return {
                'success': True,
                'transaction_id': str(transaction_id),
                'amount': float(amount),
                'platform': 'bizoholic'
            }
            
        except Exception as e:
            await self.error_handler.handle_error(e, {
                'component': 'medusa_billing_integration',
                'action': 'process_bizoholic_payment',
                'tenant_id': str(tenant_id)
            })
            raise
    
    async def get_customer_journey_analytics(
        self,
        customer_email: str
    ) -> Dict:
        """Get cross-platform customer journey analytics"""
        try:
            async with get_db() as db:
                # Get unified customer data
                customer_query = text("""
                    SELECT 
                        id, email, first_name, last_name,
                        total_bizoholic_spend, total_coreldove_spend, lifetime_value,
                        acquisition_source, created_at
                    FROM unified_customers 
                    WHERE email = :email
                """)
                
                customer_result = await db.execute(customer_query, {'email': customer_email})
                customer = customer_result.first()
                
                if not customer:
                    return {'error': 'Customer not found'}
                
                # Get transaction history
                transactions_query = text("""
                    SELECT 
                        platform, transaction_type, amount, currency, status,
                        description, created_at, metadata
                    FROM unified_transactions 
                    WHERE unified_customer_id = :customer_id
                    ORDER BY created_at DESC
                    LIMIT 50
                """)
                
                transactions_result = await db.execute(transactions_query, {
                    'customer_id': customer.id
                })
                
                transactions = []
                platform_totals = {'bizoholic': Decimal('0.00'), 'coreldove': Decimal('0.00')}
                
                for txn in transactions_result:
                    transaction_data = {
                        'platform': txn.platform,
                        'type': txn.transaction_type,
                        'amount': float(txn.amount),
                        'currency': txn.currency,
                        'status': txn.status,
                        'description': txn.description,
                        'date': txn.created_at.isoformat(),
                        'metadata': txn.metadata
                    }
                    transactions.append(transaction_data)
                    
                    if txn.status in ['completed', 'paid', 'succeeded']:
                        platform_totals[txn.platform] += txn.amount
                
                # Calculate journey metrics
                total_transactions = len(transactions)
                avg_order_value = float(sum(platform_totals.values()) / total_transactions) if total_transactions > 0 else 0
                
                return {
                    'customer': {
                        'id': str(customer.id),
                        'email': customer.email,
                        'name': f"{customer.first_name} {customer.last_name}".strip(),
                        'total_bizoholic_spend': float(customer.total_bizoholic_spend),
                        'total_coreldove_spend': float(customer.total_coreldove_spend),
                        'lifetime_value': float(customer.lifetime_value),
                        'acquisition_source': customer.acquisition_source,
                        'member_since': customer.created_at.isoformat()
                    },
                    'analytics': {
                        'total_transactions': total_transactions,
                        'average_order_value': avg_order_value,
                        'platform_breakdown': {
                            'bizoholic': float(platform_totals['bizoholic']),
                            'coreldove': float(platform_totals['coreldove'])
                        },
                        'preferred_platform': 'bizoholic' if platform_totals['bizoholic'] > platform_totals['coreldove'] else 'coreldove'
                    },
                    'recent_transactions': transactions[:10]  # Most recent 10
                }
                
        except Exception as e:
            await self.error_handler.handle_error(e, {
                'component': 'medusa_billing_integration',
                'action': 'get_customer_journey_analytics',
                'customer_email': customer_email
            })
            raise
    
    async def sync_medusa_orders_to_unified(
        self,
        days_back: int = 7
    ) -> Dict:
        """Sync recent Medusa orders to unified transaction system"""
        try:
            # Get recent orders from Medusa
            response = await self.client.get(
                '/admin/orders',
                params={
                    'limit': 100,
                    'created_at[gte]': (datetime.now() - timedelta(days=days_back)).isoformat()
                }
            )
            
            if response.status_code != 200:
                raise Exception(f"Failed to fetch Medusa orders: {response.status_code}")
            
            orders_data = response.json()
            orders = orders_data.get('orders', [])
            
            synced_count = 0
            error_count = 0
            
            for order in orders:
                try:
                    # Check if transaction already exists
                    existing = await self._get_unified_transaction_by_external_id(order['id'])
                    if existing:
                        continue  # Skip already synced orders
                    
                    # Get customer data
                    customer_email = order['email']
                    if not customer_email:
                        continue
                    
                    # Record transaction
                    await self._record_unified_transaction({
                        'tenant_id': await self._get_tenant_from_email(customer_email),
                        'customer_email': customer_email,
                        'platform': 'coreldove',
                        'transaction_type': 'product_purchase',
                        'external_id': order['id'],
                        'amount': Decimal(str(order['total'] / 100)),
                        'currency': order['currency_code'],
                        'status': order['status'],
                        'description': f"CoreLDove Order #{order['display_id']}",
                        'metadata': {
                            'order_id': order['id'],
                            'display_id': order['display_id'],
                            'item_count': len(order.get('items', [])),
                            'payment_status': order.get('payment_status'),
                            'fulfillment_status': order.get('fulfillment_status')
                        },
                        'processed_at': datetime.fromisoformat(order['created_at'].replace('Z', '+00:00'))
                    })
                    
                    synced_count += 1
                    
                except Exception as e:
                    error_count += 1
                    self.logger.error(f"Failed to sync order {order.get('id', 'unknown')}: {e}")
            
            return {
                'success': True,
                'synced_orders': synced_count,
                'errors': error_count,
                'total_orders': len(orders)
            }
            
        except Exception as e:
            await self.error_handler.handle_error(e, {
                'component': 'medusa_billing_integration',
                'action': 'sync_medusa_orders'
            })
            raise
    
    # Private helper methods
    
    async def _get_unified_customer(self, email: str) -> Optional[Dict]:
        """Get unified customer by email"""
        async with get_db() as db:
            query = text("""
                SELECT id, email, first_name, last_name, coreldove_customer_id, stripe_customer_id
                FROM unified_customers 
                WHERE email = :email
            """)
            
            result = await db.execute(query, {'email': email})
            row = result.first()
            
            if row:
                return {
                    'id': str(row.id),
                    'email': row.email,
                    'first_name': row.first_name,
                    'last_name': row.last_name,
                    'coreldove_customer_id': row.coreldove_customer_id,
                    'stripe_customer_id': row.stripe_customer_id
                }
            return None
    
    async def _create_unified_customer(self, tenant_id: UUID, customer_data: Dict) -> UUID:
        """Create unified customer record"""
        async with get_db() as db:
            query = text("""
                INSERT INTO unified_customers (
                    tenant_id, email, first_name, last_name, phone,
                    acquisition_source, created_at, updated_at
                ) VALUES (
                    :tenant_id, :email, :first_name, :last_name, :phone,
                    :acquisition_source, NOW(), NOW()
                ) RETURNING id
            """)
            
            result = await db.execute(query, {
                'tenant_id': str(tenant_id),
                'email': customer_data['email'],
                'first_name': customer_data.get('first_name'),
                'last_name': customer_data.get('last_name'),
                'phone': customer_data.get('phone'),
                'acquisition_source': customer_data.get('source', 'unknown')
            })
            
            customer_id = result.scalar()
            await db.commit()
            
            return UUID(customer_id)
    
    async def _update_unified_customer(self, customer_id: str, customer_data: Dict):
        """Update unified customer record"""
        async with get_db() as db:
            query = text("""
                UPDATE unified_customers 
                SET first_name = COALESCE(:first_name, first_name),
                    last_name = COALESCE(:last_name, last_name),
                    phone = COALESCE(:phone, phone),
                    updated_at = NOW()
                WHERE id = :customer_id
            """)
            
            await db.execute(query, {
                'customer_id': customer_id,
                'first_name': customer_data.get('first_name'),
                'last_name': customer_data.get('last_name'),
                'phone': customer_data.get('phone')
            })
            
            await db.commit()
    
    async def _record_unified_transaction(self, transaction_data: Dict) -> UUID:
        """Record transaction in unified system"""
        async with get_db() as db:
            # Get or create unified customer
            unified_customer = await self._get_unified_customer(transaction_data['customer_email'])
            if not unified_customer:
                customer_id = await self._create_unified_customer(
                    transaction_data['tenant_id'],
                    {'email': transaction_data['customer_email']}
                )
            else:
                customer_id = UUID(unified_customer['id'])
            
            # Insert transaction
            query = text("""
                INSERT INTO unified_transactions (
                    tenant_id, unified_customer_id, platform, transaction_type,
                    external_id, amount, currency, status, description, metadata,
                    processed_at, created_at
                ) VALUES (
                    :tenant_id, :customer_id, :platform, :transaction_type,
                    :external_id, :amount, :currency, :status, :description, :metadata::JSONB,
                    COALESCE(:processed_at, NOW()), NOW()
                ) RETURNING id
            """)
            
            result = await db.execute(query, {
                'tenant_id': str(transaction_data['tenant_id']),
                'customer_id': str(customer_id),
                'platform': transaction_data['platform'],
                'transaction_type': transaction_data['transaction_type'],
                'external_id': transaction_data.get('external_id'),
                'amount': float(transaction_data['amount']),
                'currency': transaction_data['currency'],
                'status': transaction_data['status'],
                'description': transaction_data['description'],
                'metadata': json.dumps(transaction_data.get('metadata', {})),
                'processed_at': transaction_data.get('processed_at')
            })
            
            transaction_id = result.scalar()
            await db.commit()
            
            return UUID(transaction_id)
    
    async def _update_customer_ltv(self, customer_email: str, amount: Decimal, platform: str):
        """Update customer lifetime value"""
        async with get_db() as db:
            platform_column = f'total_{platform}_spend'
            
            query = text(f"""
                UPDATE unified_customers 
                SET {platform_column} = {platform_column} + :amount,
                    lifetime_value = total_bizoholic_spend + total_coreldove_spend + :amount,
                    updated_at = NOW()
                WHERE email = :email
            """)
            
            await db.execute(query, {
                'amount': float(amount),
                'email': customer_email
            })
            
            await db.commit()
    
    async def _get_or_create_medusa_customer(self, email: str) -> Dict:
        """Get or create customer in Medusa"""
        # Try to get existing customer
        response = await self.client.get(f'/admin/customers?email={email}')
        
        if response.status_code == 200:
            customers = response.json().get('customers', [])
            if customers:
                return customers[0]
        
        # Create new customer
        customer_data = {'email': email}
        response = await self.client.post('/admin/customers', json=customer_data)
        
        if response.status_code == 201:
            return response.json()['customer']
        
        raise Exception(f"Failed to create Medusa customer: {response.status_code}")
    
    async def _get_default_region_id(self) -> str:
        """Get default region ID from Medusa"""
        response = await self.client.get('/admin/regions')
        
        if response.status_code == 200:
            regions = response.json().get('regions', [])
            if regions:
                return regions[0]['id']
        
        raise Exception("No regions found in Medusa")
    
    async def _create_medusa_cart(self, cart_data: Dict) -> Dict:
        """Create cart in Medusa"""
        response = await self.client.post('/admin/carts', json=cart_data)
        
        if response.status_code == 201:
            return response.json()['cart']
        
        raise Exception(f"Failed to create Medusa cart: {response.status_code}")
    
    async def _complete_cart(self, cart_id: str) -> Dict:
        """Complete cart to create order"""
        response = await self.client.post(f'/admin/carts/{cart_id}/complete')
        
        if response.status_code == 200:
            return response.json()['order']
        
        raise Exception(f"Failed to complete cart: {response.status_code}")
    
    async def _add_shipping_address(self, cart_id: str, address: Dict):
        """Add shipping address to cart"""
        await self.client.post(f'/admin/carts/{cart_id}/shipping-address', json=address)
    
    async def _add_billing_address(self, cart_id: str, address: Dict):
        """Add billing address to cart"""
        await self.client.post(f'/admin/carts/{cart_id}/billing-address', json=address)
    
    async def _get_tenant_from_email(self, email: str) -> UUID:
        """Get tenant ID from customer email"""
        async with get_db() as db:
            query = text("""
                SELECT tenant_id FROM unified_customers WHERE email = :email
                UNION
                SELECT tenant_id FROM users WHERE email = :email
                LIMIT 1
            """)
            
            result = await db.execute(query, {'email': email})
            row = result.first()
            
            if row:
                return UUID(row.tenant_id)
            
            # Default tenant for unknown customers
            return UUID('00000000-0000-0000-0000-000000000001')
    
    async def _get_unified_transaction_by_external_id(self, external_id: str) -> Optional[Dict]:
        """Check if transaction already exists"""
        async with get_db() as db:
            query = text("""
                SELECT id FROM unified_transactions WHERE external_id = :external_id
            """)
            
            result = await db.execute(query, {'external_id': external_id})
            return result.first()


# Global instance
medusa_billing_integration = MedusaBillingIntegration()