from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def _create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError('The username must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(username, password, **extra_fields)


class User(AbstractUser, models.Model):

    username_validator = UnicodeUsernameValidator()

    class Role(models.IntegerChoices):
        ADMIN = 1, _('Админ')
        CUSTOMER = 2, _('Клиент')
        MANAGER = 3, _('Менеджер')
        DELIVERY_PERSON = 4, _('Доставщик')
        CHEF = 5, _('Шеф')
    
    username = models.CharField(
        _("логин"),
        max_length=150,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
        unique=True
    )
    role = models.PositiveSmallIntegerField(_('роль'), choices=Role.choices, default=Role.CUSTOMER)
    phone = models.CharField(_('номер телефона'), max_length=15, blank=True)
    telegram_chat_id = models.CharField(_('телеграм id'), max_length=12, blank=True, null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self,):
        return f'{self.username}'
    
    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
