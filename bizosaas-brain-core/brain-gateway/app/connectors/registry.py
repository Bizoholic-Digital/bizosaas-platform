from typing import Dict, Type, List, Optional
from .base import BaseConnector, ConnectorConfig
import logging

logger = logging.getLogger(__name__)

class ConnectorRegistry:
    """
    Central registry for all available BizOSaaS Connectors.
    Handles registration, discovery, and instantiation.
    """
    _connectors: Dict[str, Type[BaseConnector]] = {}
    _configs: Dict[str, ConnectorConfig] = {}

    @classmethod
    def register(cls, connector_cls: Type[BaseConnector]):
        """
        Decorator to register a new connector class.
        
        Usage:
            @ConnectorRegistry.register
            class WordPressConnector(BaseConnector):
                ...
        """
        # We need to instantiate the class or access the property to get the config
        # Since config is a property on the instance in the base class, 
        # we might need to adjust the base class or how we access it.
        # For now, let's assume the class has a static config or we instantiate it.
        # Better approach: Make config a class attribute or static method for registration purposes.
        
        # Let's assume the class has a 'get_config()' class method or static attribute
        try:
            # Check if config is available as a class attribute
            if hasattr(connector_cls, 'get_config'):
                config = connector_cls.get_config()
            else:
                # Fallback: try to instantiate with dummy data if possible, or expect a static config
                # This is risky. Let's enforce a class method in the concrete implementation.
                raise ValueError(f"Connector {connector_cls.__name__} must implement get_config() class method")
            
            cls._connectors[config.id] = connector_cls
            cls._configs[config.id] = config
            logger.info(f"Registered connector: {config.name} ({config.id})")
        except Exception as e:
            logger.error(f"Failed to register connector {connector_cls.__name__}: {e}")
            
        return connector_cls

    @classmethod
    def get_connector_class(cls, connector_id: str) -> Optional[Type[BaseConnector]]:
        """Get a connector class by ID"""
        return cls._connectors.get(connector_id)

    @classmethod
    def get_all_configs(cls) -> List[ConnectorConfig]:
        """Get configurations for all registered connectors"""
        return list(cls._configs.values())

    @classmethod
    def create_connector(cls, connector_id: str, tenant_id: str, credentials: Dict) -> BaseConnector:
        """Factory method to instantiate a connector"""
        connector_cls = cls.get_connector_class(connector_id)
        if not connector_cls:
            raise ValueError(f"Connector {connector_id} not found")
        
        return connector_cls(tenant_id=tenant_id, credentials=credentials)
