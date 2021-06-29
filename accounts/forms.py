from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from .models import User


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('phone', 'first_name', 'last_name', 'email',)

        def clean_phone(self, *args, **kwargs):
            phone = self.cleaned_data.get('phone')
            print("\n -------------" + phone[0:2])
            if phone[:2] == '01':
                if phone[:3] == '010' or phone[:3] == '011' or phone[:3] == '012':
                    raise forms.ValidationError('Invalid Phone number')
                else:
                    return phone
            else:
                raise forms.ValidationError('Invalid Phone number')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('phone', 'first_name', 'last_name', 'email',)