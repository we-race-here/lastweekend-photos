from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.core import signing
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect

from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

from apps.photo_gallery.forms import LoginForm, SignUpForm, ActivationSignUpForm, \
    ForgotPasswordForm, PasswordRecoveryForm
from apps.photo_gallery.models import User
from wrh_photos.helpers.shortcuts import unsign
from wrh_photos.helpers.utils import success_message, send_form_errors, ex_reverse, \
    error_message


class IndexView(View):

    def get(self, request, *args, **kwargs):
        ctx = {}
        # return render(request, 'photo_gallery/index.html', ctx)
        return redirect('/static/vue/index.html')


class UiPanelView(View):
    def get(self, request, *args, **kwargs):
        return redirect('/static/vue/index.html')


class LoginView(View):
    template_name = 'photo_gallery/registration/signin.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        form = LoginForm()
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, *args, **kwargs):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            next = request.GET.get('next') or settings.LOGIN_REDIRECT_URL
            return redirect(next)
        else:
            send_form_errors(form, request)
        ctx = {'form': form}
        return render(request, self.template_name, ctx)


class SignUpView(View):
    template_name = 'photo_gallery/registration/signup.html'
    success_message = 'Activation link sent to your email, please check your email.'
    redirect_url = settings.LOGIN_URL

    def get_context(self, **kwargs):
        kwargs['public_sign_up_disabled'] = self.is_public_signup_disabled()
        return kwargs

    def is_public_signup_disabled(self):
        return settings.SIGNUP_REQUEST_PUBLIC_DISABLED

    def _send_activation_email(self, email):
        sign = signing.dumps({'email': email}, salt=settings.SIGNUP_ACTIVATION_SALT)
        url = ex_reverse('photo_gallery:activation-signup', request=self.request, scheme='http', kwargs={'sign': sign})
        context = {
            'activation_url': url,
        }
        message = render_to_string('photo_gallery/email/signup-activation.html', context)
        subject = 'WRH/Photos Registration'
        from_email = settings.DEFAULT_EMAIL_FROM
        return send_mail(subject, message, from_email, [email], html_message=message, fail_silently=False)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        form = SignUpForm()
        return render(request, self.template_name, self.get_context(form=form))

    def post(self, request, *args, **kwargs):
        if self.is_public_signup_disabled():
            raise PermissionDenied("Not allowed public signup. only invitation from admin allowed!")
        
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            self._send_activation_email(email)
            success_message(self.success_message.format(email=email), request)
            return redirect(self.redirect_url)

        send_form_errors(form, request)
        return render(request, self.template_name, self.get_context(form=form))


@method_decorator(staff_member_required, name='dispatch')
class AdminSendSignupInvitationView(SignUpView):
    success_message = 'Activation link sent to "{email}" successfully.'
    redirect_url = reverse_lazy("admin:photo_gallery_user_changelist")

    def get(self, request, *args, **kwargs):
        return redirect(self.redirect_url)

    def post(self, request, *args, **kwargs):
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            self._send_activation_email(email)
            success_message(self.success_message.format(email=email), request)
        else:
            send_form_errors(form, request)
        return redirect(self.redirect_url)


class ActivationSignUpView(View):
    template_name = 'photo_gallery/registration/activation-signup.html'
    sign_url_kwarg = 'sign'
    _unsigned_data = None

    def get_unsigned_args(self):
        if not self._unsigned_data:
            signed_data = self.kwargs.get(self.sign_url_kwarg)
            self._unsigned_data = unsign(signed_data, salt=settings.SIGNUP_ACTIVATION_SALT,
                                         max_age=settings.SIGNUP_ACTIVATION_AGE)
        return self._unsigned_data

    @property
    def email_address(self):
        return self.get_unsigned_args()['email'].lower()

    def get_context_data(self, **kwargs):
        kwargs['email'] = self.email_address
        return kwargs

    def exists_email(self):
        if User.objects.filter(email=self.email_address).exists():
            return True
        return False

    def get(self, request, *args, **kwargs):
        if self.exists_email():
            error_message('An account with this email already registered!', request)
            return redirect(settings.LOGIN_REDIRECT_URL)
        form = ActivationSignUpForm()
        return render(request, self.template_name, self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        if self.exists_email():
            error_message('An account with this email already registered!', request)
            return redirect(settings.LOGIN_REDIRECT_URL)
        form = ActivationSignUpForm(data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = self.email_address
            user.save()
            auth_login(request, user)
            success_message('Registration finished successfully.', request)
            return redirect('photo_gallery:index')

        return render(request, self.template_name, self.get_context_data(form=form))


class ForgotPasswordView(View):
    template_name = 'photo_gallery/registration/forgot-password.html'

    def _send_recovery_email(self, email):
        sign = signing.dumps({'email': email}, salt=settings.RECOVERY_PASSWORD_SALT)
        url = ex_reverse('photo_gallery:password-recovery', request=self.request, scheme='http', kwargs={'sign': sign})
        context = {
            'recovery_url': url,
        }
        message = render_to_string('photo_gallery/email/recovery-password.html', context)
        subject = 'WRH/Photos Recovery Password'
        from_email = settings.DEFAULT_EMAIL_FROM
        return send_mail(subject, message, from_email, [email], html_message=message, fail_silently=False)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        form = ForgotPasswordForm()
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, *args, **kwargs):
        form = ForgotPasswordForm(data=request.POST)
        if form.is_valid():
            self._send_recovery_email(form.cleaned_data['email'])
            success_message('Recovery password link sent to your email, please check your email.', request)
            return redirect(settings.LOGIN_URL)

        send_form_errors(form, request)
        ctx = {'form': form}
        return render(request, self.template_name, ctx)


class PasswordRecoveryView(View):
    template_name = 'photo_gallery/registration/password-recovery.html'
    sign_url_kwarg = 'sign'
    _unsigned_data = None

    def get_unsigned_args(self):
        if not self._unsigned_data:
            signed_data = self.kwargs.get(self.sign_url_kwarg)
            self._unsigned_data = unsign(signed_data, salt=settings.RECOVERY_PASSWORD_SALT,
                                         max_age=settings.RECOVERY_PASSWORD_AGE)
        return self._unsigned_data

    @property
    def email_address(self):
        return self.get_unsigned_args()['email'].lower()

    def get_context_data(self, **kwargs):
        kwargs['email'] = self.email_address
        kwargs['current_user'] = self.get_user()
        return kwargs

    def get_user(self):
        return User.objects.filter(email=self.email_address).first()

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        user = self.get_user()
        if not user:
            error_message('No account registered with this email', request)
            return redirect(settings.LOGIN_REDIRECT_URL)
        form = PasswordRecoveryForm(user=user)
        return render(request, self.template_name, self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        user = self.get_user()
        if not user:
            error_message('No account registered with this email', request)
            return redirect(settings.LOGIN_REDIRECT_URL)
        form = PasswordRecoveryForm(user=user, data=request.POST)
        if form.is_valid():
            form.save()
            success_message('Password reset successfully.', request)
            return redirect('photo_gallery:index')

        return render(request, self.template_name, self.get_context_data(form=form))


class LogoutView(View):

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        next_url = request.headers.get('Referer') or 'photo_gallery:index'
        return redirect(next_url)
