'use client';

import React, { useEffect, useRef, useState, useCallback } from 'react';
import { Loader } from '@googlemaps/js-api-loader';
import { MapPin, Navigation, ZoomIn, ZoomOut, RotateCcw, Filter } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Business, MapBounds, SearchFilters } from '@/types/business';
import { businessAPI } from '@/lib/api';
import { cn } from '@/lib/utils';

interface InteractiveMapProps {
  businesses: Business[];
  center?: { lat: number; lng: number };
  zoom?: number;
  height?: string;
  onBoundsChanged?: (bounds: MapBounds) => void;
  onBusinessSelect?: (business: Business) => void;
  filters?: SearchFilters;
  className?: string;
  showControls?: boolean;
  clustered?: boolean;
}

interface MarkerCluster {
  position: google.maps.LatLng;
  businesses: Business[];
  count: number;
}

const GOOGLE_MAPS_API_KEY = process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY || '';

export function InteractiveMap({
  businesses,
  center = { lat: 37.7749, lng: -122.4194 }, // San Francisco default
  zoom = 12,
  height = '400px',
  onBoundsChanged,
  onBusinessSelect,
  filters,
  className,
  showControls = true,
  clustered = true
}: InteractiveMapProps) {
  const mapRef = useRef<HTMLDivElement>(null);
  const [map, setMap] = useState<google.maps.Map | null>(null);
  const [markers, setMarkers] = useState<google.maps.Marker[]>([]);
  const [clusterMarkers, setClusterMarkers] = useState<google.maps.Marker[]>([]);
  const [infoWindow, setInfoWindow] = useState<google.maps.InfoWindow | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [userLocation, setUserLocation] = useState<{ lat: number; lng: number } | null>(null);
  const [mapReady, setMapReady] = useState(false);

  // Custom marker icons
  const getMarkerIcon = useCallback((business: Business, isCluster = false, count = 0) => {
    if (isCluster) {
      return {
        url: `data:image/svg+xml;charset=UTF-8,${encodeURIComponent(`
          <svg width="40" height="40" viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg">
            <circle cx="20" cy="20" r="18" fill="#3b82f6" stroke="#ffffff" stroke-width="2"/>
            <text x="20" y="25" text-anchor="middle" fill="white" font-family="Arial" font-size="12" font-weight="bold">
              ${count > 99 ? '99+' : count}
            </text>
          </svg>
        `)}`,
        scaledSize: new google.maps.Size(40, 40),
        anchor: new google.maps.Point(20, 20)
      };
    }

    const color = business.featured ? '#10b981' : 
                  business.verified ? '#3b82f6' : 
                  business.rating >= 4.5 ? '#f59e0b' : '#6b7280';

    return {
      url: `data:image/svg+xml;charset=UTF-8,${encodeURIComponent(`
        <svg width="32" height="42" viewBox="0 0 32 42" xmlns="http://www.w3.org/2000/svg">
          <path d="M16 0C7.163 0 0 7.163 0 16c0 16 16 26 16 26s16-10 16-26c0-8.837-7.163-16-16-16z" fill="${color}"/>
          <circle cx="16" cy="16" r="8" fill="white"/>
          <circle cx="16" cy="16" r="4" fill="${color}"/>
        </svg>
      `)}`,
      scaledSize: new google.maps.Size(32, 42),
      anchor: new google.maps.Point(16, 42)
    };
  }, []);

  // Initialize Google Maps
  useEffect(() => {
    if (!GOOGLE_MAPS_API_KEY) {
      setError('Google Maps API key is not configured');
      setLoading(false);
      return;
    }

    const loader = new Loader({
      apiKey: GOOGLE_MAPS_API_KEY,
      version: 'weekly',
      libraries: ['places', 'geometry']
    });

    loader.load().then(() => {
      if (mapRef.current) {
        const mapInstance = new google.maps.Map(mapRef.current, {
          center,
          zoom,
          mapTypeControl: false,
          streetViewControl: false,
          fullscreenControl: false,
          zoomControl: false,
          styles: [
            {
              featureType: 'poi',
              elementType: 'labels',
              stylers: [{ visibility: 'off' }]
            }
          ]
        });

        const infoWindowInstance = new google.maps.InfoWindow();

        // Add bounds change listener
        mapInstance.addListener('bounds_changed', () => {
          if (onBoundsChanged) {
            const bounds = mapInstance.getBounds();
            if (bounds) {
              const boundsData: MapBounds = {
                north: bounds.getNorthEast().lat(),
                south: bounds.getSouthWest().lat(),
                east: bounds.getNorthEast().lng(),
                west: bounds.getSouthWest().lng()
              };
              onBoundsChanged(boundsData);
            }
          }
        });

        setMap(mapInstance);
        setInfoWindow(infoWindowInstance);
        setMapReady(true);
        setLoading(false);
      }
    }).catch((error) => {
      console.error('Error loading Google Maps:', error);
      setError('Failed to load Google Maps');
      setLoading(false);
    });
  }, [center, zoom, onBoundsChanged]);

  // Get user location
  useEffect(() => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setUserLocation({
            lat: position.coords.latitude,
            lng: position.coords.longitude
          });
        },
        (error) => {
          console.warn('Geolocation error:', error);
        }
      );
    }
  }, []);

  // Create marker clusters
  const createClusters = useCallback((businesses: Business[]): MarkerCluster[] => {
    if (!clustered || businesses.length <= 3) return [];

    const clusters: MarkerCluster[] = [];
    const processed = new Set<string>();
    const clusterDistance = 0.01; // ~1km

    businesses.forEach((business) => {
      if (processed.has(business.id)) return;

      const cluster: MarkerCluster = {
        position: new google.maps.LatLng(
          business.location?.coordinates?.lat || 0,
          business.location?.coordinates?.lng || 0
        ),
        businesses: [business],
        count: 1
      };

      // Find nearby businesses
      businesses.forEach((otherBusiness) => {
        if (processed.has(otherBusiness.id) || business.id === otherBusiness.id) return;

        const distance = google.maps.geometry.spherical.computeDistanceBetween(
          cluster.position,
          new google.maps.LatLng(
            otherBusiness.location.coordinates.lat,
            otherBusiness.location.coordinates.lng
          )
        );

        if (distance < clusterDistance * 111320) { // Convert to meters
          cluster.businesses.push(otherBusiness);
          cluster.count++;
          processed.add(otherBusiness.id);
        }
      });

      processed.add(business.id);
      clusters.push(cluster);
    });

    return clusters.filter(cluster => cluster.count > 1);
  }, [clustered]);

  // Update markers when businesses change
  useEffect(() => {
    if (!map || !mapReady) return;

    // Clear existing markers
    markers.forEach(marker => marker.setMap(null));
    clusterMarkers.forEach(marker => marker.setMap(null));

    const newMarkers: google.maps.Marker[] = [];
    const newClusterMarkers: google.maps.Marker[] = [];

    if (businesses.length > 0) {
      const clusters = createClusters(businesses);
      const clusteredBusinessIds = new Set(
        clusters.flatMap(cluster => cluster.businesses.map(b => b.id))
      );

      // Create cluster markers
      clusters.forEach((cluster) => {
        if (cluster.count > 1) {
          const clusterMarker = new google.maps.Marker({
            position: cluster.position,
            map,
            icon: getMarkerIcon(cluster.businesses[0], true, cluster.count),
            zIndex: 1000
          });

          clusterMarker.addListener('click', () => {
            if (infoWindow) {
              const content = `
                <div class="p-3 max-w-xs">
                  <h3 class="font-semibold mb-2">${cluster.count} businesses</h3>
                  <div class="space-y-2 max-h-32 overflow-y-auto">
                    ${cluster.businesses.map(business => `
                      <div class="flex items-center space-x-2 p-2 hover:bg-gray-50 rounded cursor-pointer" 
                           onclick="window.selectBusiness('${business.id}')">
                        <div class="flex-1 min-w-0">
                          <p class="text-sm font-medium truncate">${business.name}</p>
                          <p class="text-xs text-gray-500">${business.category.name}</p>
                        </div>
                        <div class="flex items-center">
                          <span class="text-xs text-yellow-500">★</span>
                          <span class="text-xs ml-1">${business.rating.toFixed(1)}</span>
                        </div>
                      </div>
                    `).join('')}
                  </div>
                </div>
              `;
              infoWindow.setContent(content);
              infoWindow.setPosition(cluster.position);
              infoWindow.open(map);
            }
          });

          newClusterMarkers.push(clusterMarker);
        }
      });

      // Create individual business markers
      businesses.forEach((business) => {
        if (!clusteredBusinessIds.has(business.id)) {
          const marker = new google.maps.Marker({
            position: {
              lat: business.location?.coordinates?.lat || 0,
              lng: business.location?.coordinates?.lng || 0
            },
            map,
            icon: getMarkerIcon(business),
            title: business.name,
            zIndex: business.featured ? 500 : 100
          });

          marker.addListener('click', () => {
            if (infoWindow) {
              const content = `
                <div class="p-3 max-w-sm">
                  <div class="flex items-start space-x-3">
                    ${(business.images && business.images[0]) ? 
                      `<img src="${business.images[0]}" alt="${business.name}" 
                           class="w-16 h-16 object-cover rounded-lg flex-shrink-0">` : 
                      '<div class="w-16 h-16 bg-gray-200 rounded-lg flex-shrink-0"></div>'
                    }
                    <div class="flex-1 min-w-0">
                      <h3 class="font-semibold text-gray-900 truncate">${business.name}</h3>
                      <p class="text-sm text-gray-600">${business.category.name}</p>
                      <div class="flex items-center mt-1">
                        <span class="text-yellow-500 text-sm">★</span>
                        <span class="text-sm ml-1">${business.rating.toFixed(1)}</span>
                        <span class="text-xs text-gray-500 ml-1">(${business.reviewCount})</span>
                        ${business.verified ? '<span class="ml-2 text-xs bg-blue-100 text-blue-800 px-1 rounded">Verified</span>' : ''}
                      </div>
                      <p class="text-xs text-gray-600 mt-1">${business.location?.address || 'Address not available'}</p>
                      <div class="flex space-x-2 mt-2">
                        <button onclick="window.selectBusiness('${business.id}')" 
                                class="text-xs bg-blue-500 text-white px-2 py-1 rounded hover:bg-blue-600">
                          View Details
                        </button>
                        ${business.contact?.phone ? 
                          `<a href="tel:${business.contact.phone}" 
                             class="text-xs bg-green-500 text-white px-2 py-1 rounded hover:bg-green-600">
                            Call
                          </a>` : ''
                        }
                      </div>
                    </div>
                  </div>
                </div>
              `;
              infoWindow.setContent(content);
              infoWindow.setPosition(marker.getPosition()!);
              infoWindow.open(map);
            }

            if (onBusinessSelect) {
              onBusinessSelect(business);
            }
          });

          newMarkers.push(marker);
        }
      });

      // Fit map to show all markers
      if (newMarkers.length > 0 || newClusterMarkers.length > 0) {
        const bounds = new google.maps.LatLngBounds();
        [...newMarkers, ...newClusterMarkers].forEach(marker => {
          const position = marker.getPosition();
          if (position) bounds.extend(position);
        });
        map.fitBounds(bounds);
      }
    }

    setMarkers(newMarkers);
    setClusterMarkers(newClusterMarkers);
  }, [map, mapReady, businesses, getMarkerIcon, createClusters, infoWindow, onBusinessSelect]);

  // Global function for info window interactions
  useEffect(() => {
    (window as any).selectBusiness = (businessId: string) => {
      const business = businesses.find(b => b.id === businessId);
      if (business && onBusinessSelect) {
        onBusinessSelect(business);
      }
    };

    return () => {
      delete (window as any).selectBusiness;
    };
  }, [businesses, onBusinessSelect]);

  const handleZoomIn = () => {
    if (map) {
      map.setZoom((map.getZoom() || 10) + 1);
    }
  };

  const handleZoomOut = () => {
    if (map) {
      map.setZoom((map.getZoom() || 10) - 1);
    }
  };

  const handleCenterOnUser = () => {
    if (map && userLocation) {
      map.setCenter(userLocation);
      map.setZoom(15);
    } else if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const location = {
            lat: position.coords.latitude,
            lng: position.coords.longitude
          };
          setUserLocation(location);
          if (map) {
            map.setCenter(location);
            map.setZoom(15);
          }
        },
        (error) => {
          console.error('Geolocation error:', error);
        }
      );
    }
  };

  const handleReset = () => {
    if (map) {
      map.setCenter(center);
      map.setZoom(zoom);
    }
  };

  if (loading) {
    return (
      <Card className={cn("map-loading", className)} style={{ height }}>
        <CardContent className="flex items-center justify-center h-full">
          <div className="text-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto"></div>
            <p className="mt-2 text-sm text-muted-foreground">Loading map...</p>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (error) {
    return (
      <Card className={cn("map-error", className)} style={{ height }}>
        <CardContent className="flex items-center justify-center h-full">
          <div className="text-center">
            <MapPin className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <p className="text-sm text-gray-600 dark:text-gray-400">{error}</p>
            <p className="text-xs text-gray-500 dark:text-gray-500 mt-1">
              Interactive map unavailable
            </p>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className={cn("relative", className)} style={{ height }}>
      <div ref={mapRef} className="w-full h-full rounded-lg overflow-hidden" />
      
      {/* Map Controls */}
      {showControls && (
        <div className="absolute top-4 right-4 space-y-2">
          <div className="flex flex-col space-y-1 bg-white dark:bg-gray-800 rounded-lg shadow-lg p-1">
            <Button
              variant="ghost"
              size="sm"
              onClick={handleZoomIn}
              className="p-2"
              title="Zoom in"
            >
              <ZoomIn className="w-4 h-4" />
            </Button>
            <Button
              variant="ghost"
              size="sm"
              onClick={handleZoomOut}
              className="p-2"
              title="Zoom out"
            >
              <ZoomOut className="w-4 h-4" />
            </Button>
            <Button
              variant="ghost"
              size="sm"
              onClick={handleCenterOnUser}
              className="p-2"
              title="Center on my location"
            >
              <Navigation className="w-4 h-4" />
            </Button>
            <Button
              variant="ghost"
              size="sm"
              onClick={handleReset}
              className="p-2"
              title="Reset view"
            >
              <RotateCcw className="w-4 h-4" />
            </Button>
          </div>
        </div>
      )}
      
      {/* Legend */}
      {businesses.length > 0 && (
        <div className="absolute bottom-4 left-4 bg-white dark:bg-gray-800 rounded-lg shadow-lg p-3">
          <div className="text-xs font-semibold text-gray-600 dark:text-gray-400 mb-2">
            Legend
          </div>
          <div className="space-y-1">
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 rounded-full bg-green-500"></div>
              <span className="text-xs text-gray-600 dark:text-gray-400">Featured</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 rounded-full bg-blue-500"></div>
              <span className="text-xs text-gray-600 dark:text-gray-400">Verified</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
              <span className="text-xs text-gray-600 dark:text-gray-400">Top Rated</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 rounded-full bg-gray-500"></div>
              <span className="text-xs text-gray-600 dark:text-gray-400">Standard</span>
            </div>
          </div>
        </div>
      )}
      
      {/* Business Count Badge */}
      {businesses.length > 0 && (
        <div className="absolute top-4 left-4">
          <Badge variant="secondary" className="bg-white dark:bg-gray-800 shadow-lg">
            {businesses.length} business{businesses.length !== 1 ? 'es' : ''}
          </Badge>
        </div>
      )}
    </div>
  );
}