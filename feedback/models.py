from django.db import models


class Feedback(models.Model):
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')
    email = models.EmailField(max_length=150, verbose_name='E-mail')
    message = models.TextField(max_length=1000, verbose_name='Сообщение')

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Обратная связь'
