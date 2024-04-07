from decimal import Decimal
from typing import Any
import urllib.parse

from django.contrib import admin
from django.db.models.fields.related import ForeignKey
from django.forms.models import ModelChoiceField
from django.http import HttpResponse
from django.http.request import HttpRequest
from django.urls import path, reverse
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _
from django.db import transaction
from django.db.models import  Prefetch
from rangefilter.filters import DateRangeFilterBuilder
from django_admin_listfilter_dropdown.filters import ChoiceDropdownFilter

from commerce.models import (
    User, Order, OrderItem, Customer, Category, Product,
    CompanyDeliveryZone, Company
)
from commerce.actions.admin import GenerateOrderInvoice


class AdminSite(admin.AdminSite):
    site_header = 'Админ'
    site_title = 'Админ'
    index_title = 'Админ'


admin_site = AdminSite(name='admin-site')


class UserAdmin(DjangoUserAdmin, admin.ModelAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('username', 'password',
         'phone', 'role', 'is_staff', 'groups', 'telegram_chat_id')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'role', 'is_staff', 'groups', 'telegram_chat_id'),
        }),
    )
    list_display = ('username', 'phone', 'role')
    search_fields = ('username', 'phone')
    list_filter = ('role',)
    ordering = ('username', 'role')

    def get_form(self, request, obj=None, **kwargs):
        if obj is None:  # Creating a new user
            kwargs['form'] = self.add_form
        else:  # Changing an existing user
            kwargs['form'] = self.form
        kwargs['form'].request = request
        return super().get_form(request, obj, **kwargs)


class OrderItemInline(admin.StackedInline):
    model = OrderItem
    can_delete = True
    verbose_name_plural = _('Детали заказа')
    readonly_fields = ('price', 'total_price')
    extra = 0
    fk_name = 'order'


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderItemInline, )
    list_display = ('id', 'company', 'status', 'order_type', 'address', 'final_amount', 'is_paid')
    fields = ('user', 'status', 'order_type', 'address', 'delivery_zone', 'comment', 'payment_type', 'is_paid', 'discount', 'company',
              'total_amount', 'additional_charge', 'discount_amount', 'final_amount',)
    list_editable = ('is_paid', 'status', 'order_type', 'address')
    list_filter = (
        ('created_at', DateRangeFilterBuilder()), 'status'
    )
    ordering = ('-pk',)
    readonly_fields = ('total_amount', 'additional_charge', 'discount_amount', 'final_amount', 'discount',)
    list_per_page = 10

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related(
            Prefetch('items', OrderItem.objects.select_related('product').only('product__name', 'quantity', 'order_id'))
        ).select_related('user')

    @transaction.atomic
    def save_formset(self, request, form, formset, change):
        instances: list[OrderItem] = formset.save(commit=False)

        for obj in formset.deleted_objects:
            obj.delete()

        for instance in instances:
            instance.price = instance.price if instance.price else instance.product.price
            instance.total_price = instance.price * instance.quantity
            instance.save()

        formset.save_m2m()

        order: Order = form.save(commit=False)
        discount = form.cleaned_data.get('discount')
        customer: Customer = form.cleaned_data.get('customer')
        if discount is None:
            discount = customer.discount if customer else 0

        order.discount = discount
        order.total_amount = sum(
            [item.total_price for item in order.items.all()])
        order.discount_amount = order.total_amount * \
            Decimal.from_float(order.discount / 100)
        if order.order_type == Order.OrderType.DELIVERY:
            order.additional_charge = order.delivery_zone.additional_charge if order.delivery_zone else 0
        order.final_amount = order.total_amount + order.additional_charge - order.discount_amount
        order.save()

    @admin.display(description='Накладной')
    def download_link(self, obj):
        return format_html(
            '<a href="{}" target="_blank">Накладной</a>',
            reverse('admin:generate_invoice', args=[obj.pk])
        )

    def get_urls(self):
        return [
            path("<pk>/invoice/", self.admin_site.admin_view(self.generate_invoice), name="generate_invoice"),
            *super().get_urls(),
        ]
    
    def generate_invoice(self, request, pk):
        pdf_file, file_name = GenerateOrderInvoice()(pk)
        if pdf_file is None:
            return HttpResponse(status=204)
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response[
            'Content-Disposition'] = f'attachment;filename*=UTF-8\'\'{urllib.parse.quote(file_name)}'
        return response
    

class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'category', 'cost_price', 'price', 'hide')
    list_editable = ('name', 'category', 'cost_price', 'price', 'hide')
    search_fields = ('name',)
    list_filter = ('category', 'hide')
    ordering = ('category',)

    
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'discount', 'phone', 'user', )
    fields = ('name', 'address', 'customer_type', 'phone', 'discount', 'user')
    list_filter = ('customer_type', )

    def formfield_for_foreignkey(self, db_field: ForeignKey[Any], request: HttpRequest | None, **kwargs: Any) -> ModelChoiceField | None:
        if db_field.name == 'user':
            kwargs['queryset'] = User.objects.filter(role=User.Role.CUSTOMER)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'order', 'hide')
    list_editable = ('name', 'order', 'hide')
    list_filter = ('hide',)
    search_fields = ('name',)
    ordering = ('order',)


class DeliveryZoneInline(admin.TabularInline):
    model = CompanyDeliveryZone
    extra = 0  # Number of empty forms to display


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'address')
    search_fields = ('name', 'phone_number', 'instagram', 'whatsapp')
    inlines = [DeliveryZoneInline]
    exclude = ('site', 'type')


admin_site.register(Product, ProductAdmin)
admin_site.register(Customer, CustomerAdmin)
admin_site.register(Category, CategoryAdmin)
admin_site.register(Order, OrderAdmin)
admin_site.register(User, UserAdmin)
admin_site.register(Company, CompanyAdmin)
