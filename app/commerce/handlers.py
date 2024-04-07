from django.core.cache import cache


def clear_company_cache_on_save_delete(sender, instance, *args, **kwargs):
    cache.delete('company_list')
