from celery import shared_task
from django.core.mail import send_mail

from TOR_VM.settings import EMAIL_HOST_USER

from .models import Order
# import django
# django.setup()


@shared_task
def order_created(order_id):
    """
    Отправка уведомления по электронной почте при успешном создании заказа.
    """
    order = Order.objects.get(id=order_id)
    subject = f'Номер Вашего заказа - {order_id}'
    message = f'Уважаемый, {order.first_name},\n\nВаш заказ успешно создан. Номер Вашего заказа {order_id}.'
    mail_sent = send_mail(subject,
                          message,
                          EMAIL_HOST_USER,
                          [order.email])
    return mail_sent
