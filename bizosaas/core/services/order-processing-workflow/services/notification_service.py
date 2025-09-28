"""
Notification Service
Handles customer notifications throughout the order lifecycle
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from uuid import uuid4
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logger = logging.getLogger(__name__)


class NotificationService:
    """
    Comprehensive notification service
    Handles email, SMS, push notifications for order lifecycle events
    """
    
    def __init__(self):
        self.config = {
            "email_enabled": True,
            "sms_enabled": True,
            "push_enabled": True,
            "webhook_enabled": True,
            "template_engine": "jinja2",
            "smtp_host": "smtp.gmail.com",
            "smtp_port": 587,
            "smtp_username": "",  # Configure in production
            "smtp_password": "",  # Configure in production
            "from_email": "noreply@coreldove.com",
            "from_name": "CoreLDove"
        }
        
        # Notification templates
        self.email_templates = {
            "order_confirmation": {
                "subject": "Order Confirmation - Order #{order_number}",
                "template": self._get_order_confirmation_template()
            },
            "payment_confirmation": {
                "subject": "Payment Confirmed - Order #{order_number}",
                "template": self._get_payment_confirmation_template()
            },
            "shipping_notification": {
                "subject": "Your order has shipped - Order #{order_number}",
                "template": self._get_shipping_notification_template()
            },
            "delivery_confirmation": {
                "subject": "Order Delivered - Order #{order_number}",
                "template": self._get_delivery_confirmation_template()
            },
            "refund_confirmation": {
                "subject": "Refund Processed - Order #{order_number}",
                "template": self._get_refund_confirmation_template()
            },
            "order_cancelled": {
                "subject": "Order Cancelled - Order #{order_number}",
                "template": self._get_order_cancelled_template()
            },
            "inventory_backorder": {
                "subject": "Item Backordered - Order #{order_number}",
                "template": self._get_backorder_template()
            }
        }
        
        # SMS templates
        self.sms_templates = {
            "order_confirmation": "Your order #{order_number} has been confirmed. Total: {total}. Thank you for shopping with CoreLDove!",
            "shipping_notification": "Your order #{order_number} has shipped! Track it here: {tracking_url}",
            "delivery_confirmation": "Your order #{order_number} has been delivered. Enjoy your purchase!",
            "refund_confirmation": "Your refund for order #{order_number} has been processed. Amount: {refund_amount}"
        }
        
        # In-memory storage for demo
        self.notification_history = {}
        self.notification_queue = []
        self.webhook_endpoints = {}
        
    async def initialize(self):
        """Initialize notification service"""
        logger.info("Initializing Notification Service...")
        
        try:
            # Initialize notification channels
            await self._initialize_email_service()
            await self._initialize_sms_service()
            await self._initialize_push_service()
            
            # Start background tasks
            asyncio.create_task(self._process_notification_queue())
            
            logger.info("Notification Service initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Notification Service: {e}")
            raise
    
    async def shutdown(self):
        """Cleanup notification service"""
        logger.info("Shutting down Notification Service...")
    
    async def send_order_confirmation(self, order_result: Dict[str, Any]) -> Dict[str, Any]:
        """Send order confirmation notification"""
        logger.info(f"Sending order confirmation for order {order_result.get('id')}")
        
        try:
            # Prepare notification data
            notification_data = {
                "order_number": order_result.get("order_number"),
                "customer_email": self._get_customer_email(order_result),
                "customer_phone": self._get_customer_phone(order_result),
                "order_total": str(order_result.get("pricing", {}).get("total", "0")),
                "currency": order_result.get("pricing", {}).get("currency", "USD"),
                "items": order_result.get("items", []),
                "shipping_address": order_result.get("shipping_address", {}),
                "estimated_delivery": self._format_date(order_result.get("estimated_delivery"))
            }
            
            # Send notifications
            results = await self._send_multi_channel_notification(
                "order_confirmation",
                notification_data,
                channels=["email", "sms"]
            )
            
            # Send webhook notification
            if self.config["webhook_enabled"]:
                await self._send_webhook_notification("order.confirmed", order_result)
            
            return {
                "success": True,
                "notifications_sent": results
            }
            
        except Exception as e:
            logger.error(f"Order confirmation notification failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def send_payment_confirmation(self, order_result: Dict[str, Any]) -> Dict[str, Any]:
        """Send payment confirmation notification"""
        logger.info(f"Sending payment confirmation for order {order_result.get('id')}")
        
        try:
            notification_data = {
                "order_number": order_result.get("order_number"),
                "customer_email": self._get_customer_email(order_result),
                "payment_amount": str(order_result.get("pricing", {}).get("total", "0")),
                "currency": order_result.get("pricing", {}).get("currency", "USD"),
                "payment_method": order_result.get("payment_details", {}).get("method"),
                "transaction_id": order_result.get("payment_details", {}).get("transaction_id")
            }
            
            results = await self._send_multi_channel_notification(
                "payment_confirmation",
                notification_data,
                channels=["email"]
            )
            
            return {
                "success": True,
                "notifications_sent": results
            }
            
        except Exception as e:
            logger.error(f"Payment confirmation notification failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def send_shipping_notification(self, fulfillment_result: Dict[str, Any]) -> Dict[str, Any]:
        """Send shipping notification"""
        logger.info(f"Sending shipping notification for order {fulfillment_result.get('order_id')}")
        
        try:
            notification_data = {
                "order_number": fulfillment_result.get("order_number", "Unknown"),
                "customer_email": self._get_customer_email(fulfillment_result),
                "customer_phone": self._get_customer_phone(fulfillment_result),
                "tracking_number": fulfillment_result.get("tracking_number"),
                "tracking_url": f"https://track.coreldove.com/{fulfillment_result.get('tracking_number')}",
                "carrier": fulfillment_result.get("shipping_details", {}).get("carrier"),
                "estimated_delivery": self._format_date(fulfillment_result.get("estimated_delivery")),
                "shipping_method": fulfillment_result.get("shipping_details", {}).get("method")
            }
            
            results = await self._send_multi_channel_notification(
                "shipping_notification",
                notification_data,
                channels=["email", "sms"]
            )
            
            # Send webhook notification
            if self.config["webhook_enabled"]:
                await self._send_webhook_notification("order.shipped", fulfillment_result)
            
            return {
                "success": True,
                "notifications_sent": results
            }
            
        except Exception as e:
            logger.error(f"Shipping notification failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def send_delivery_confirmation(self, order: Dict[str, Any]) -> Dict[str, Any]:
        """Send delivery confirmation notification"""
        logger.info(f"Sending delivery confirmation for order {order.get('id')}")
        
        try:
            notification_data = {
                "order_number": order.get("order_number"),
                "customer_email": self._get_customer_email(order),
                "customer_phone": self._get_customer_phone(order),
                "delivered_at": self._format_date(datetime.utcnow()),
                "items": order.get("items", [])
            }
            
            results = await self._send_multi_channel_notification(
                "delivery_confirmation",
                notification_data,
                channels=["email", "sms"]
            )
            
            # Send webhook notification
            if self.config["webhook_enabled"]:
                await self._send_webhook_notification("order.delivered", order)
            
            return {
                "success": True,
                "notifications_sent": results
            }
            
        except Exception as e:
            logger.error(f"Delivery confirmation notification failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def send_refund_confirmation(self, refund_result: Dict[str, Any]) -> Dict[str, Any]:
        """Send refund confirmation notification"""
        logger.info(f"Sending refund confirmation for order {refund_result.get('order_id')}")
        
        try:
            notification_data = {
                "order_number": refund_result.get("order_number", "Unknown"),
                "customer_email": self._get_customer_email(refund_result),
                "customer_phone": self._get_customer_phone(refund_result),
                "refund_amount": str(refund_result.get("refunded_amount", "0")),
                "currency": refund_result.get("currency", "USD"),
                "refund_type": refund_result.get("refund_type", "full"),
                "refund_reason": refund_result.get("refund_reason", "Customer request"),
                "processing_time": "3-5 business days"
            }
            
            results = await self._send_multi_channel_notification(
                "refund_confirmation",
                notification_data,
                channels=["email", "sms"]
            )
            
            # Send webhook notification
            if self.config["webhook_enabled"]:
                await self._send_webhook_notification("order.refunded", refund_result)
            
            return {
                "success": True,
                "notifications_sent": results
            }
            
        except Exception as e:
            logger.error(f"Refund confirmation notification failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def send_order_cancelled_notification(self, order: Dict[str, Any]) -> Dict[str, Any]:
        """Send order cancellation notification"""
        logger.info(f"Sending cancellation notification for order {order.get('id')}")
        
        try:
            notification_data = {
                "order_number": order.get("order_number"),
                "customer_email": self._get_customer_email(order),
                "customer_phone": self._get_customer_phone(order),
                "cancellation_reason": order.get("cancellation_reason", "Customer request"),
                "refund_amount": str(order.get("pricing", {}).get("total", "0")),
                "currency": order.get("pricing", {}).get("currency", "USD")
            }
            
            results = await self._send_multi_channel_notification(
                "order_cancelled",
                notification_data,
                channels=["email"]
            )
            
            return {
                "success": True,
                "notifications_sent": results
            }
            
        except Exception as e:
            logger.error(f"Order cancellation notification failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def send_backorder_notification(self, order: Dict[str, Any], backorder_items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Send backorder notification"""
        logger.info(f"Sending backorder notification for order {order.get('id')}")
        
        try:
            notification_data = {
                "order_number": order.get("order_number"),
                "customer_email": self._get_customer_email(order),
                "backorder_items": backorder_items,
                "estimated_restock": self._format_date(datetime.utcnow() + timedelta(days=14))
            }
            
            results = await self._send_multi_channel_notification(
                "inventory_backorder",
                notification_data,
                channels=["email"]
            )
            
            return {
                "success": True,
                "notifications_sent": results
            }
            
        except Exception as e:
            logger.error(f"Backorder notification failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def send_custom_notification(
        self, 
        customer_email: str, 
        subject: str, 
        message: str,
        channels: List[str] = ["email"]
    ) -> Dict[str, Any]:
        """Send custom notification"""
        logger.info(f"Sending custom notification to {customer_email}")
        
        try:
            notification_data = {
                "customer_email": customer_email,
                "custom_subject": subject,
                "custom_message": message
            }
            
            results = []
            
            if "email" in channels and self.config["email_enabled"]:
                email_result = await self._send_email_notification(
                    customer_email,
                    subject,
                    message,
                    is_html=False
                )
                results.append({"channel": "email", "result": email_result})
            
            return {
                "success": True,
                "notifications_sent": results
            }
            
        except Exception as e:
            logger.error(f"Custom notification failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def get_notification_history(self, order_id: str) -> List[Dict[str, Any]]:
        """Get notification history for order"""
        
        return self.notification_history.get(order_id, [])
    
    async def get_health(self) -> Dict[str, Any]:
        """Get notification service health status"""
        
        return {
            "status": "healthy",
            "email_enabled": self.config["email_enabled"],
            "sms_enabled": self.config["sms_enabled"],
            "push_enabled": self.config["push_enabled"],
            "queue_size": len(self.notification_queue),
            "notifications_sent_today": len(self.notification_history)
        }
    
    # Private helper methods
    
    async def _initialize_email_service(self):
        """Initialize email service"""
        if self.config["email_enabled"]:
            logger.info("Email service initialized")
    
    async def _initialize_sms_service(self):
        """Initialize SMS service"""
        if self.config["sms_enabled"]:
            logger.info("SMS service initialized")
    
    async def _initialize_push_service(self):
        """Initialize push notification service"""
        if self.config["push_enabled"]:
            logger.info("Push notification service initialized")
    
    async def _send_multi_channel_notification(
        self,
        template_name: str,
        data: Dict[str, Any],
        channels: List[str]
    ) -> List[Dict[str, Any]]:
        """Send notification across multiple channels"""
        
        results = []
        
        # Send email notification
        if "email" in channels and self.config["email_enabled"]:
            email_result = await self._send_email_from_template(template_name, data)
            results.append({"channel": "email", "result": email_result})
        
        # Send SMS notification
        if "sms" in channels and self.config["sms_enabled"]:
            sms_result = await self._send_sms_from_template(template_name, data)
            results.append({"channel": "sms", "result": sms_result})
        
        # Send push notification
        if "push" in channels and self.config["push_enabled"]:
            push_result = await self._send_push_from_template(template_name, data)
            results.append({"channel": "push", "result": push_result})
        
        # Store in history
        self._store_notification_history(template_name, data, results)
        
        return results
    
    async def _send_email_from_template(self, template_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Send email using template"""
        
        if template_name not in self.email_templates:
            raise Exception(f"Email template {template_name} not found")
        
        template = self.email_templates[template_name]
        
        # Render subject and body
        subject = template["subject"].format(**data)
        body = template["template"].format(**data)
        
        customer_email = data.get("customer_email")
        if not customer_email:
            raise Exception("Customer email not provided")
        
        return await self._send_email_notification(customer_email, subject, body, is_html=True)
    
    async def _send_sms_from_template(self, template_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Send SMS using template"""
        
        if template_name not in self.sms_templates:
            return {"success": False, "error": f"SMS template {template_name} not found"}
        
        template = self.sms_templates[template_name]
        message = template.format(**data)
        
        customer_phone = data.get("customer_phone")
        if not customer_phone:
            return {"success": False, "error": "Customer phone not provided"}
        
        return await self._send_sms_notification(customer_phone, message)
    
    async def _send_push_from_template(self, template_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Send push notification using template"""
        
        # Simulate push notification
        logger.info(f"Sending push notification: {template_name}")
        
        return {
            "success": True,
            "message": "Push notification sent",
            "timestamp": datetime.utcnow()
        }
    
    async def _send_email_notification(self, to_email: str, subject: str, body: str, is_html: bool = True) -> Dict[str, Any]:
        """Send email notification"""
        
        try:
            # In production, this would use actual SMTP
            logger.info(f"Sending email to {to_email}: {subject}")
            
            # Simulate email sending
            await asyncio.sleep(0.1)
            
            return {
                "success": True,
                "message": "Email sent successfully",
                "to": to_email,
                "subject": subject,
                "timestamp": datetime.utcnow()
            }
            
        except Exception as e:
            logger.error(f"Email sending failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "to": to_email,
                "timestamp": datetime.utcnow()
            }
    
    async def _send_sms_notification(self, to_phone: str, message: str) -> Dict[str, Any]:
        """Send SMS notification"""
        
        try:
            # In production, this would use SMS service (Twilio, etc.)
            logger.info(f"Sending SMS to {to_phone}: {message[:50]}...")
            
            # Simulate SMS sending
            await asyncio.sleep(0.1)
            
            return {
                "success": True,
                "message": "SMS sent successfully",
                "to": to_phone,
                "timestamp": datetime.utcnow()
            }
            
        except Exception as e:
            logger.error(f"SMS sending failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "to": to_phone,
                "timestamp": datetime.utcnow()
            }
    
    async def _send_webhook_notification(self, event_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Send webhook notification"""
        
        try:
            webhook_data = {
                "event": event_type,
                "timestamp": datetime.utcnow().isoformat(),
                "data": data
            }
            
            logger.info(f"Sending webhook notification: {event_type}")
            
            # In production, this would make HTTP POST requests to registered webhook URLs
            
            return {
                "success": True,
                "event": event_type,
                "timestamp": datetime.utcnow()
            }
            
        except Exception as e:
            logger.error(f"Webhook notification failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _get_customer_email(self, order_data: Dict[str, Any]) -> str:
        """Extract customer email from order data"""
        
        # Try multiple locations for email
        billing_address = order_data.get("billing_address", {})
        shipping_address = order_data.get("shipping_address", {})
        
        return (
            billing_address.get("email") or 
            shipping_address.get("email") or
            order_data.get("customer_email") or
            "customer@example.com"  # Fallback
        )
    
    def _get_customer_phone(self, order_data: Dict[str, Any]) -> Optional[str]:
        """Extract customer phone from order data"""
        
        billing_address = order_data.get("billing_address", {})
        shipping_address = order_data.get("shipping_address", {})
        
        return (
            billing_address.get("phone") or 
            shipping_address.get("phone") or
            order_data.get("customer_phone")
        )
    
    def _format_date(self, date_obj: Optional[datetime]) -> str:
        """Format date for display"""
        
        if not date_obj:
            return "TBD"
        
        if isinstance(date_obj, str):
            return date_obj
        
        return date_obj.strftime("%B %d, %Y")
    
    def _store_notification_history(self, template_name: str, data: Dict[str, Any], results: List[Dict[str, Any]]):
        """Store notification in history"""
        
        order_id = data.get("order_id") or data.get("order_number", "unknown")
        
        if order_id not in self.notification_history:
            self.notification_history[order_id] = []
        
        self.notification_history[order_id].append({
            "template": template_name,
            "timestamp": datetime.utcnow(),
            "channels": [r["channel"] for r in results],
            "success": all(r["result"]["success"] for r in results),
            "results": results
        })
    
    async def _process_notification_queue(self):
        """Background task to process notification queue"""
        
        while True:
            try:
                if self.notification_queue:
                    notification = self.notification_queue.pop(0)
                    await self._process_queued_notification(notification)
                
                await asyncio.sleep(1)  # Process queue every second
                
            except Exception as e:
                logger.error(f"Notification queue processing failed: {e}")
                await asyncio.sleep(5)
    
    async def _process_queued_notification(self, notification: Dict[str, Any]):
        """Process queued notification"""
        
        try:
            # Process the notification based on type
            notification_type = notification.get("type")
            data = notification.get("data", {})
            
            if notification_type == "order_confirmation":
                await self.send_order_confirmation(data)
            elif notification_type == "shipping_notification":
                await self.send_shipping_notification(data)
            # Add more notification types as needed
            
        except Exception as e:
            logger.error(f"Queued notification processing failed: {e}")
    
    # Email templates
    
    def _get_order_confirmation_template(self) -> str:
        """Get order confirmation email template"""
        
        return """
        <html>
        <body>
            <h2>Order Confirmation</h2>
            <p>Thank you for your order!</p>
            
            <h3>Order Details</h3>
            <p><strong>Order Number:</strong> {order_number}</p>
            <p><strong>Order Total:</strong> {currency} {order_total}</p>
            
            <h3>Shipping Address</h3>
            <p>
                {shipping_address[first_name]} {shipping_address[last_name]}<br>
                {shipping_address[address_line_1]}<br>
                {shipping_address[city]}, {shipping_address[state]} {shipping_address[postal_code]}
            </p>
            
            <h3>Items Ordered</h3>
            <ul>
                {items_list}
            </ul>
            
            <p>We'll send you another email when your items ship.</p>
            
            <p>Thank you for shopping with CoreLDove!</p>
        </body>
        </html>
        """
    
    def _get_payment_confirmation_template(self) -> str:
        """Get payment confirmation email template"""
        
        return """
        <html>
        <body>
            <h2>Payment Confirmation</h2>
            <p>Your payment has been successfully processed.</p>
            
            <h3>Payment Details</h3>
            <p><strong>Order Number:</strong> {order_number}</p>
            <p><strong>Amount:</strong> {currency} {payment_amount}</p>
            <p><strong>Payment Method:</strong> {payment_method}</p>
            <p><strong>Transaction ID:</strong> {transaction_id}</p>
            
            <p>Your order is now being processed for shipment.</p>
            
            <p>Thank you for your business!</p>
        </body>
        </html>
        """
    
    def _get_shipping_notification_template(self) -> str:
        """Get shipping notification email template"""
        
        return """
        <html>
        <body>
            <h2>Your Order Has Shipped!</h2>
            <p>Great news! Your order is on its way.</p>
            
            <h3>Tracking Information</h3>
            <p><strong>Order Number:</strong> {order_number}</p>
            <p><strong>Tracking Number:</strong> {tracking_number}</p>
            <p><strong>Carrier:</strong> {carrier}</p>
            <p><strong>Estimated Delivery:</strong> {estimated_delivery}</p>
            
            <p><a href="{tracking_url}">Track Your Package</a></p>
            
            <p>Thank you for shopping with CoreLDove!</p>
        </body>
        </html>
        """
    
    def _get_delivery_confirmation_template(self) -> str:
        """Get delivery confirmation email template"""
        
        return """
        <html>
        <body>
            <h2>Order Delivered</h2>
            <p>Your order has been successfully delivered!</p>
            
            <h3>Delivery Details</h3>
            <p><strong>Order Number:</strong> {order_number}</p>
            <p><strong>Delivered At:</strong> {delivered_at}</p>
            
            <p>We hope you enjoy your purchase. If you have any issues, please don't hesitate to contact us.</p>
            
            <p>Thank you for choosing CoreLDove!</p>
        </body>
        </html>
        """
    
    def _get_refund_confirmation_template(self) -> str:
        """Get refund confirmation email template"""
        
        return """
        <html>
        <body>
            <h2>Refund Processed</h2>
            <p>Your refund has been processed successfully.</p>
            
            <h3>Refund Details</h3>
            <p><strong>Order Number:</strong> {order_number}</p>
            <p><strong>Refund Amount:</strong> {currency} {refund_amount}</p>
            <p><strong>Refund Type:</strong> {refund_type}</p>
            <p><strong>Processing Time:</strong> {processing_time}</p>
            
            <p>The refund will appear on your original payment method within the processing time mentioned above.</p>
            
            <p>Thank you for your business!</p>
        </body>
        </html>
        """
    
    def _get_order_cancelled_template(self) -> str:
        """Get order cancellation email template"""
        
        return """
        <html>
        <body>
            <h2>Order Cancelled</h2>
            <p>Your order has been cancelled as requested.</p>
            
            <h3>Cancellation Details</h3>
            <p><strong>Order Number:</strong> {order_number}</p>
            <p><strong>Reason:</strong> {cancellation_reason}</p>
            <p><strong>Refund Amount:</strong> {currency} {refund_amount}</p>
            
            <p>If a payment was processed, the refund will be issued to your original payment method within 3-5 business days.</p>
            
            <p>We're sorry to see you go, but we hope to serve you again in the future.</p>
        </body>
        </html>
        """
    
    def _get_backorder_template(self) -> str:
        """Get backorder notification email template"""
        
        return """
        <html>
        <body>
            <h2>Item Backordered</h2>
            <p>We're writing to inform you that some items in your order are currently on backorder.</p>
            
            <h3>Order Details</h3>
            <p><strong>Order Number:</strong> {order_number}</p>
            <p><strong>Estimated Restock Date:</strong> {estimated_restock}</p>
            
            <h3>Backordered Items</h3>
            <ul>
                {backorder_items_list}
            </ul>
            
            <p>We'll notify you as soon as these items are back in stock and ready to ship.</p>
            
            <p>Thank you for your patience!</p>
        </body>
        </html>
        """