# myapp/middleware.py
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseNotFound

class CurrentSiteMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            current_site = get_current_site(request)
        except ObjectDoesNotExist:
            return HttpResponseNotFound("Site not found")
        
        request.current_site = current_site

        response = self.get_response(request)
        return response
