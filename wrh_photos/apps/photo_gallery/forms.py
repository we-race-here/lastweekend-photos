from django.contrib.auth import password_validation
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.forms.widgets import PasswordInput, TextInput, EmailInput
from django import forms

from apps.photo_gallery.models import User

boolean_toggle_attrs = {
    'data-onstyle': 'success', 'data-offstyle': 'danger', 'data-toggle': 'toggle', 'data-on': 'Enabled',
    'data-off': 'Disabled', 'data-width': '110px',
}


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username',
               'required': True}))
    password = forms.CharField(widget=PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password',
               'required': True}))


class SignUpForm(forms.Form):
    email = forms.EmailField(widget=EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'E-mail Address',
               'required': True}))

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        if User.objects.filter(email=email).exists():
            raise ValidationError('An account with this email already registered')
        return email


class ActivationSignUpForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        strip=False,
    )
    re_password = forms.CharField(
        label="Re-type Password",
        widget=forms.PasswordInput,
        strip=False,
    )

    class Meta:
        model = User
        fields = [ 'username', 'first_name', 'last_name', 'gender', 'password']

    def clean_re_password(self):
        password = self.cleaned_data.get("password")
        re_password = self.cleaned_data.get("re_password")
        if password and re_password and password != re_password:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return re_password

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('re_password')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('re_password', error)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(widget=EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'E-mail Address',
               'required': True}))

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        if not User.objects.filter(email=email).exists():
            raise ValidationError('No account registered with this email')
        return email


class PasswordRecoveryForm(forms.Form):
    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
    }

    password = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput,
        strip=False,
    )
    re_password = forms.CharField(
        label="Re-type New Password",
        widget=forms.PasswordInput,
        strip=False,
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_re_password(self):
        password = self.cleaned_data.get("password")
        re_password = self.cleaned_data.get("re_password")
        if password and re_password and password != re_password:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return re_password

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('re_password')
        if password:
            try:
                password_validation.validate_password(password, self.user)
            except forms.ValidationError as error:
                self.add_error('re_password', error)

    def save(self, commit=True):
        password = self.cleaned_data["password"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user
