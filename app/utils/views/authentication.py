from django.contrib.auth.backends import ModelBackend
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model

from django.utils.translation import gettext_lazy as _
from django.utils.functional import cached_property
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.models import TokenUser
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import Token, AccessToken


class CustomTokenUser(TokenUser):
    @cached_property
    def id(self):
        id = super().id
        if isinstance(id, str) and id.isdigit():
            id = int(id)
        return id

    @cached_property
    def groups(self):
        groups = self.token.get('groups')
        return groups if groups is not None else []
    
    @cached_property
    def site_id(self):
        site_id = self.token.get('site_id')
        if isinstance(site_id, str) and site_id.isdigit():
            site_id = int(id)
        return site_id


class ServiceToken(AccessToken):
    token_type = 'service'


class CustomJWTTokenAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        """
        Returns a stateless user object which is backed by the given validated
        token.
        """
        if api_settings.USER_ID_CLAIM not in validated_token:
            # The TokenUser class assumes tokens will have a recognizable user
            # identifier claim.
            raise InvalidToken(
                _('Token contained no recognizable user identification'))

        return CustomTokenUser(validated_token)