from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomerSignUpForm(UserCreationForm):
    """Self-registration form used on the public /register/ page (role locked to CUSTOMER)."""

    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'First name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'you@example.com'}))
    phone = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'placeholder': '10-digit mobile number'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email', 'phone')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Role.CUSTOMER
        user.email = self.cleaned_data['email']
        user.phone = self.cleaned_data['phone']
        user.first_name = self.cleaned_data['first_name']
        if commit:
            user.save()
        return user


class StaffCreationForm(UserCreationForm):
    """Used by the Owner to create Advisor / Mechanic accounts from the dashboard."""

    role = forms.ChoiceField(choices=[(User.Role.ADVISOR, 'Service Advisor'), (User.Role.MECHANIC, 'Mechanic')])
    email = forms.EmailField()
    phone = forms.CharField(max_length=15)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'role', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = self.cleaned_data['role']
        user.email = self.cleaned_data['email']
        user.phone = self.cleaned_data['phone']
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username', 'autofocus': True}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
