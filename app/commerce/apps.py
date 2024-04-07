from django.apps import AppConfig


class CommerceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'commerce'

    def ready(self):
        from django.db.models.signals import post_delete, post_save

        from commerce.handlers import (
            clear_company_cache_on_save_delete,
            send_order_status_to_ws
        )

        from commerce.models import (
            Company, Order
        )

        post_save.connect(clear_company_cache_on_save_delete, sender=Company)
        post_delete.connect(clear_company_cache_on_save_delete, sender=Company)
        post_save.connect(send_order_status_to_ws, sender=Order)


