from django import forms
from django.forms import Textarea

from feedback.models import Feedback


class FeedbackForm(forms.ModelForm):

    # текст для плейсхолдера
    class Meta:
        model = Feedback
        fields = ['first_name', 'last_name', 'email', 'message']
        widgets = {
            'message': Textarea(attrs={'placeholder': 'Напишите тут ваше сообщение'})
        }
