from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from TOR_VM.settings import EMAIL_HOST_USER

from feedback.forms import FeedbackForm
from feedback.models import Feedback


class FeedbackView(CreateView):
    model = Feedback
    form_class = FeedbackForm
    template_name = 'feedback/feedback_page.html'
    extra_context = {'nav_selected': 1}

    def form_valid(self, form):
        data = form.data
        subject = f'Сообщение с формы от {data["first_name"]} {data["last_name"]} Почта отправителя: {data["email"]}'
        send_mail(subject, data['message'], EMAIL_HOST_USER, [EMAIL_HOST_USER])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('feedback:success_page')


def success(request):
    return render(request, 'feedback/feedback_success.html', {'nav_selected': 1})
