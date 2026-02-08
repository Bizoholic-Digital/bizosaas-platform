"""
Pagination classes for Django CRM
Standardized pagination with metadata
"""
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict


class StandardResultsSetPagination(PageNumberPagination):
    """Standard pagination with configurable page size"""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100
    page_query_param = 'page'
    
    def get_paginated_response(self, data):
        """Return paginated response with metadata"""
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('total_pages', self.page.paginator.num_pages),
            ('current_page', self.page.number),
            ('page_size', self.get_page_size(self.request)),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))
    
    def get_paginated_response_schema(self, schema):
        """Schema for paginated response"""
        return {
            'type': 'object',
            'properties': {
                'count': {
                    'type': 'integer',
                    'example': 123,
                },
                'total_pages': {
                    'type': 'integer',
                    'example': 7,
                },
                'current_page': {
                    'type': 'integer',
                    'example': 1,
                },
                'page_size': {
                    'type': 'integer',
                    'example': 20,
                },
                'next': {
                    'type': 'string',
                    'nullable': True,
                    'format': 'uri',
                    'example': 'http://api.example.org/accounts/?page=4'
                },
                'previous': {
                    'type': 'string',
                    'nullable': True,
                    'format': 'uri',
                    'example': 'http://api.example.org/accounts/?page=2'
                },
                'results': schema,
            },
        }


class SmallResultsSetPagination(PageNumberPagination):
    """Smaller pagination for quick lists"""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50
    
    def get_paginated_response(self, data):
        """Return paginated response with metadata"""
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('total_pages', self.page.paginator.num_pages),
            ('current_page', self.page.number),
            ('page_size', self.get_page_size(self.request)),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))


class LargeResultsSetPagination(PageNumberPagination):
    """Larger pagination for bulk operations"""
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 500
    
    def get_paginated_response(self, data):
        """Return paginated response with metadata"""
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('total_pages', self.page.paginator.num_pages),
            ('current_page', self.page.number),
            ('page_size', self.get_page_size(self.request)),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))


class NoPagination(PageNumberPagination):
    """Pagination class that can be disabled"""
    page_size = None
    
    def paginate_queryset(self, queryset, request, view=None):
        """Don't paginate if page_size is explicitly set to 'none'"""
        if request.query_params.get('page_size') == 'none':
            return None
        
        # Use default pagination otherwise
        self.page_size = 20
        return super().paginate_queryset(queryset, request, view)