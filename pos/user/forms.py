from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms import TextInput, PasswordInput, ModelForm, NumberInput, ImageField, FileInput, DateInput

from core.models import User


class UserForm(forms.ModelForm):
    #     class Meta:
    #         model = User
    #         fields = '__all__'
    #
    #     def __init__(self, *args, **kwargs):
    #         super(UserForm, self).__init__(*args, **kwargs)
    #         self.fields['name'].required = True
    #         self.fields['nid'].required = True
    pass


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Code',
                                                       'autofocus': True}))
    password = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password',
                                                           'autofocus': True}))


class AddNewEmployeeForm(ModelForm):
    # dob = forms.DateField(input_formats=['%m-%d-%Y'],
    #                       widget=forms.DateInput(
    #                           attrs={'class': 'form-control', 'placeholder': 'DOB', 'id': 'datepicker',
    #                                  'data-select': 'datepicker', 'readonly': True, 'required': True},
    #                           format='%m-%d-%Y'), )
    # profile_pic = forms.ImageField()
    # dob = forms.DateField(input_formats=['%m-%d-%Y'])

    class Meta:
        model = User
        fields = ['name', 'email', 'profile_pic', 'nid', 'gender', 'city', 'country',
                  'address', 'dob', 'is_staff', 'is_admin']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'id': 'fullname', 'placeholder': 'Full Name',
                                     'oninput': 'showName()', 'autofocus': True, 'required': True}),
            'email': TextInput(attrs={'class': 'form-control', 'type': 'email', 'placeholder': 'Email'}),
            'nid': NumberInput(attrs={'class': 'form-control', 'type': 'number', 'placeholder': 'NID',
                                      'required': True}),
            'city': TextInput(attrs={'class': 'form-control', 'placeholder': 'City', 'required': True}),
            'country': TextInput(attrs={'class': 'form-control', 'placeholder': 'Country', 'required': True}),
            'address': TextInput(attrs={'class': 'form-control', 'placeholder': 'Address', 'required': True}),
        }

    def __init__(self, *args, **kwargs):
        super(AddNewEmployeeForm, self).__init__(*args, **kwargs)
        self.fields['nid'].required = True
        self.fields['email'].required = False
        self.fields['dob'].required = True
        self.fields['dob'] = forms.DateField(input_formats=['%m-%d-%Y'])
        self.fields['dob'] = forms.DateField(input_formats=['%m-%d-%Y'],
                                             widget=forms.DateInput(
                                                 attrs={'class': 'form-control', 'placeholder': 'DOB',
                                                        'id': 'datepicker',
                                                        'data-select': 'datepicker', 'readonly': True,
                                                        'required': True},
                                                 format='%m-%d-%Y'), )
        self.fields['profile_pic'] = forms.ImageField(widget=FileInput(attrs={'id': 'img_input', 'hidden': True,
                                                                              'accept': 'image/*'}))
