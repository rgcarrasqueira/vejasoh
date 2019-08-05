from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class RegisterForm(UserCreationForm):

	username = forms.CharField(label=_('Login de Usuário'))
	password1 = forms.CharField(label=_('Senha de Acesso'), widget=forms.PasswordInput())
	password2 = forms.CharField(label=_('Repita sua Senha de Acesso'), widget=forms.PasswordInput())
	email = forms.EmailField(label=_('E-mail'))
	first_name = forms.CharField(label = _('Nome'))
	last_name = forms.CharField(label = _('Sobrenome'))

	class Meta:
		model = User
		fields = ("first_name", "last_name", "email", "username", "password1", "password2")

	def save(self, commit=True):

		user = super(RegisterForm, self).save(commit=False)
		user.email = self.cleaned_data["email"]
		user.first_name = self.cleaned_data["first_name"]
		user.last_name = self.cleaned_data["last_name"]
		user.is_active=True
	
		if commit:
			user.save()
			return user
