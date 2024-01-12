from django.urls import path

from feedback.views import FeedbackView, success

app_name = 'feedback'

urlpatterns = [
    path('feedback_page/', FeedbackView.as_view(), name='feedback_page'),
    path('success/', success, name='success_page'),
]
