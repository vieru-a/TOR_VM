from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError("The given e-mail must be set")

        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(verbose_name='email',
                              max_length=150,
                              unique=True,
                              error_messages={"unique": "Пользователь с таким e-mail уже существует."})

    # направление бизнеса (физ/юр)
    business_type_choices = [('individuals', 'Физические лица'),
                             ('legal_entities', 'Юридические лица')]

    business_type = models.CharField(choices=business_type_choices, verbose_name='Направление бизнеса')

    # если юр лицо (Юр наименование, ИНН, КПП, ЮР.АДРЕС, Файл с контактами)
    legal_name = models.CharField(max_length=255, default='-', verbose_name='Юр. наименование')
    inn = models.CharField(max_length=255, default='-',  verbose_name='ИНН')
    kpp = models.CharField(max_length=255, default='-',  verbose_name='КПП')
    legal_address = models.CharField(max_length=255, default='-',  verbose_name='Юр. адрес')
    file_with_contacts = models.FileField(max_length=255, default='-',  verbose_name='Файл с контактами')

    # имя
    first_name = models.CharField(max_length=150, verbose_name='Имя')
    # фамилия
    last_name = models.CharField(max_length=150, verbose_name='Фамилия')
    # телефон
    phone_number = PhoneNumberField(unique=True,
                                    verbose_name='Номер телефона',
                                    error_messages={"unique": "Пользователь с таким номером уже существует.",
                                                    "invalid": "Введите корректный номер телефона (+79035743801)"})
    # факс
    fax = models.CharField(max_length=150, verbose_name='Факс')
    # компания
    company = models.CharField(max_length=150, verbose_name='Компания')
    # адрес 1
    address1 = models.CharField(max_length=255, verbose_name='Адрес')
    # адрес 2
    address2 = models.CharField(max_length=255, null=True, blank=True, verbose_name='Дополнительный адрес')
    # город
    city = models.CharField(max_length=150, verbose_name='Город')
    # индекс
    index = models.CharField(max_length=150, verbose_name='Индекс')
    # страна (выкидное меню)
    country = CountryField(default='ru', verbose_name='Страна')
    # рассылка
    mailing = models.BooleanField(default=False, verbose_name='Рассылка новостей')

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
