from io import BytesIO

from django.http import Http404
from django.template.loader import render_to_string
from django.db.models import Prefetch, F
from weasyprint import HTML

from commerce.models import Order, OrderItem


class GenerateOrderInvoice:

    def __call__(self, order_id: int) -> (str, str):
        try:
            order = Order.objects.select_related(
                'customer'
            ).prefetch_related(
                Prefetch('items', OrderItem.objects.annotate(
                        product_name=F('product__name')
                    ).order_by('product__category_id', 'product__name')
                )
            ).get(pk=order_id)
        except Order.DoesNotExist:
            raise Http404

        context = {
            'order': order
        }

        rendered_html = self.get_rendered_html(context)
        pdf_content = self.rendered_html_to_pdf(rendered_html)
        file_name = f'Заказ {order.pk}.pdf'
        return pdf_content, file_name

    def get_rendered_html(self, context: dict) -> str:
        return render_to_string('order/invoice.html', context)

    def rendered_html_to_pdf(self, rendered_html: str) -> bytes:
        return HTML(string=rendered_html).write_pdf()
