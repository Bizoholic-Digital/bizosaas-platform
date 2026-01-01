import logging
from app.store import active_connectors
from app.connectors.base import ConnectorStatus

logger = logging.getLogger(__name__)

def seed_connectors():
    """
    Seeds the active_connectors store with Live Data for Coreldove and Bizoholic.
    This bypasses network validation and persistence issues for the MVP context.
    """
    try:
        logger.info("=" * 50)
        logger.info("🌱 Starting Connector Seeding...")
        logger.info("=" * 50)
        
        # Bizoholic - WordPress & FluentCRM
        # Using 'default' as the target for the demo
        
        logger.info("📝 Seeding Bizoholic WordPress connection...")
        active_connectors["default:wordpress"] = {
            "connector_id": "wordpress",
            "credentials": {
                "url": "https://www.bizoholic.com",
                "username": "bizoholic.digital@gmail.com",
                "application_password": "25IKC#1XiKABRo",
                "force_connect": True
            },
            "status": ConnectorStatus.CONNECTED,
            "last_sync": None
        }

        logger.info("📝 Seeding Bizoholic FluentCRM connection...")
        active_connectors["default:fluentcrm"] = {
            "connector_id": "fluentcrm",
            "credentials": {
                "url": "https://www.bizoholic.com",
                "username": "bizoholic.digital@gmail.com",
                "application_password": "25IKC#1XiKABRo",
                "force_connect": True
            },
            "status": ConnectorStatus.CONNECTED,
            "last_sync": None
        }

        # Coreldove - WooCommerce
        logger.info("📝 Seeding Coreldove WooCommerce connection...")
        active_connectors["default:woocommerce"] = {
            "connector_id": "woocommerce",
            "credentials": {
                "url": "https://www.coreldove.com",
                "consumer_key": "ck_mock_coreldove",
                "consumer_secret": "cs_mock_coreldove",
                "force_connect": True
            },
            "status": ConnectorStatus.CONNECTED,
            "last_sync": None
        }
        
        # Lago for Billing
        logger.info("📝 Seeding Lago Billing connection...")
        active_connectors["default:lago"] = {
            "connector_id": "lago",
            "credentials": {
                 "api_url": "http://lago-api:3000",
                 "api_key": "N3YbnttmAFCSMxyhyTPf696Pzyxfmud4RZGj0NMW4BOUjV61gRsBMN2jeq07c8Qw5x7eXpl3jiSakDgK7QbOQ1BexhWvpRHYKC4dQpWvAephZTJIzJVNoWar3wUd4An7",
                 "force_connect": True
            },
            "status": ConnectorStatus.CONNECTED
        }

        # Redis Cloud
        logger.info("📝 Seeding Redis Cloud connection...")
        active_connectors["default:redis"] = {
            "connector_id": "redis",
            "credentials": {
                "url": "redis://default:Gt7QxXA4ybMzYzD9e6KIBULfnv1IU6f9@redis-10690.c264.ap-south-1-1.ec2.cloud.redislabs.com:10690/0",
                "force_connect": True
            },
            "status": ConnectorStatus.CONNECTED
        }

        logger.info("=" * 50)
        logger.info(f"✅ Seeding Complete! Registered {len(active_connectors)} connectors")
        logger.info("=" * 50)
        
    except Exception as e:
        logger.error(f"❌ Seeding failed with error: {e}", exc_info=True)
        raise
