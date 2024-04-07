from django.core.cache import cache
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from commerce.models.orders import Order


def clear_company_cache_on_save_delete(sender, instance, *args, **kwargs):
    cache.delete('company_list')


def send_order_status_to_ws(sender, instance: Order, **kwargs):
    # Get the status of the saved order
    status = instance.get_status_display()

    # Send message to room group
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'orders_{instance.uuid}',
        {
            'type': 'receive',
            'status': status
        }
    )