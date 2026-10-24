from django.db import transaction
from apps.orders.models import Order, OrderItem
from apps.inventory.selectors import get_product_by_id
from infrastructure.payment.gateway import charge_card

class OrderService:
    @staticmethod
    @transaction.atomic
    def create_order(user, product_id, quantity, payment_token):
        product = get_product_by_id(product_id)

        if product.stock < quantity:
            raise ValueError("Insufficient stock")

        order = Order.objects.create(user=user, total=product.price * quantity)
        OrderItem.objects.create(order=order, product=product, quantity=quantity)

        charge_card(token=payment_token, amount=order.total)
        product.reduce_stock(quantity)

        return order