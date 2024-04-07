from dataclasses import dataclass
from decimal import Decimal
from typing import List

from django.db import transaction

from commerce.models import Order, OrderItem, Product, User
from commerce.services import telegram_client


class CreateOrder:

    @dataclass
    class Command:
        
        @dataclass
        class OrderItemCommand:
            product_id: int
            quantity: int

        user_id: int
        company_id: int
        order_items: List[OrderItemCommand]
        order_type: int
        number_of_cutlery: int
        address: str
        comment: str | None = None
        delivery_zone_id: int | None = None

    @transaction.atomic
    def __call__(self, cmd: Command) -> Order:
        order = Order.objects.create(
            company_id=cmd.company_id, 
            user_id=cmd.user_id, 
            status=Order.Status.NEW,
            order_type=cmd.order_type,
            number_of_cutlery=cmd.number_of_cutlery,
            comment=cmd.comment,
            delivery_zone_id=cmd.delivery_zone_id
        )
        total_amount = 0
        discount_amount = 0
        for order_item in cmd.order_items:
            product = Product.objects.get(pk=order_item.product_id)
            db_order_item = OrderItem.objects.create(
                order_id=order.pk, 
                product_id=product.pk, 
                quantity=order_item.quantity,
                price=product.price,
                total_price=product.price * order_item.quantity
            )

            total_amount += db_order_item.total_price
            discount_amount += db_order_item.total_price

        order.total_amount = total_amount
        order.discount_amount = discount_amount
        order.final_amount = total_amount - discount_amount
        order.address = cmd.address
        order.save()
        self.notify_staffs(order)
        return order
    
    @staticmethod
    def get_notify_message(order: Order) -> str:
        ingredients=''
        for index, item in enumerate(order.items.all(), start=1):
            ingredients+=f'{index}. {item.product.name} X {item.quantity}\n'
        
        ordered_user: User = order.user

        text = f'<b>Новый заказ {order.pk}</b>\nИмя: {ordered_user.get_full_name()}\nНомер телефона: {ordered_user.phone}\n'
        text += 'Самовывоз\n' if order.order_type == Order.OrderType.PICKUP else f'Адрес: {order.address}\n'
        text += f'Итог: {order.final_amount}\nСумма к полате: {order.paid_amount}\n\n'
        text += ingredients

        return text
    
    def notify_staffs(self, order: Order):
        users = User.objects.filter(
            is_staff=True, 
            role__in=(User.Role.ADMIN, User.Role.MANAGER), telegram_chat_id__isnull=False
        ).only('telegram_chat_id')

        text = self.get_notify_message(order)

        for staff in users:
            try:
                telegram_client.notify_user(staff.telegram_chat_id, text)
            except Exception as e:
                pass
