from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='E-mail', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    error_messages = {"invalid_login": (
            "Пожалуйста, введите правильные почту и пароль. "
            "Оба поля могут быть чувствительны к регистру."), }

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


class RegisterUserForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ['email', 'phone_number', 'first_name', 'last_name',
                  'business_type', 'legal_name', 'inn', 'kpp', 'legal_address', 'file_with_contacts',
                  'fax', 'company', 'address1', 'address2', 'city', 'index', 'country', 'mailing',
                  'password1', 'password2']
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-input'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-input'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'business_type': forms.Select(attrs={'onchange': 'business_type_select(this.value)'}),
            'legal_name': forms.TextInput(attrs={'class': 'form-input'}),
            'inn': forms.TextInput(attrs={'class': 'form-input'}),
            'kpp': forms.TextInput(attrs={'class': 'form-input'}),
            'legal_address': forms.TextInput(attrs={'class': 'form-input'}),
            'file_with_contacts': forms.FileInput(attrs={'class': 'form-input'}),
            'fax': forms.TextInput(attrs={'class': 'form-input'}),
            'company': forms.TextInput(attrs={'class': 'form-input'}),
            'address1': forms.TextInput(attrs={'class': 'form-input'}),
            'address2': forms.TextInput(attrs={'class': 'form-input'}),
            'city': forms.TextInput(attrs={'class': 'form-input'}),
            'index': forms.TextInput(attrs={'class': 'form-input'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-input'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-input'}),
        }


class ProfileUserForm(forms.ModelForm):
    email = forms.CharField(disabled=True, label='E-mail', widget=forms.TextInput(attrs={'class': 'form-input'}))
    phone_number = forms.CharField(disabled=True, label='Номер телефона', widget=forms.TextInput(attrs={'class': 'form-input'}))

    class Meta:
        model = get_user_model()
        fields = ['email', 'phone_number', 'first_name', 'last_name',
                  'business_type', 'legal_name', 'inn', 'kpp', 'legal_address', 'file_with_contacts',
                  'fax', 'company', 'address1', 'address2', 'city', 'index', 'country', 'mailing']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'business_type': forms.Select(attrs={'disabled': 'disabled'}),
            'legal_name': forms.TextInput(attrs={'class': 'form-input'}),
            'inn': forms.TextInput(attrs={'class': 'form-input'}),
            'kpp': forms.TextInput(attrs={'class': 'form-input'}),
            'legal_address': forms.TextInput(attrs={'class': 'form-input'}),
            'file_with_contacts': forms.FileInput(attrs={'class': 'form-input'}),
            'fax': forms.TextInput(attrs={'class': 'form-input'}),
            'company': forms.TextInput(attrs={'class': 'form-input'}),
            'address1': forms.TextInput(attrs={'class': 'form-input'}),
            'address2': forms.TextInput(attrs={'class': 'form-input'}),
            'city': forms.TextInput(attrs={'class': 'form-input'}),
            'index': forms.TextInput(attrs={'class': 'form-input'}),
        }


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="Cтарый пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password1 = forms.CharField(label="Новый пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password2 = forms.CharField(label="Подтвердите пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
