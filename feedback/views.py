from django.core.mail import send_mail
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView

from feedback.forms import FeedbackForm
from feedback.models import Feedback


class FeedbackView(CreateView):
    model = Feedback
    form_class = FeedbackForm
    template_name = 'feedback/feedback_page.html'

    def form_valid(self, form):
        data = form.data
        subject = f'Сообщение с формы от {data["first_name"]} {data["last_name"]} Почта отправителя: {data["email"]}'
        send_mail(subject, data['message'], 'djangomailtest7@yandex.ru', ['djangomailtest7@yandex.ru'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('feedback:success_page')


def success(request):
    return HttpResponse('Письмо отправлено!')
