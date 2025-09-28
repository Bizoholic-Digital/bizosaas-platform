"""
Platform-specific clients for all directory and mapping platforms
Implements the platform abstraction layer for each supported platform
"""

# Import all platform clients when this module is imported
# This ensures they are registered with the platform registry

from .google_maps_client import GoogleMapsClient
from .bing_maps_client import BingMapsClient  
from .bing_places_client import BingPlacesClient
from .tripadvisor_client import TripAdvisorClient
from .foursquare_client import FoursquareClient
from .here_maps_client import HereMapsClient
from .mapquest_client import MapQuestClient
from .yellow_pages_client import YellowPagesClient
from .superpages_client import SuperpagesClient

__all__ = [
    "GoogleMapsClient",
    "BingMapsClient",
    "BingPlacesClient", 
    "TripAdvisorClient",
    "FoursquareClient",
    "HereMapsClient",
    "MapQuestClient",
    "YellowPagesClient",
    "SuperpagesClient"
]