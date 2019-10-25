from django import forms

class ServicePayForm(forms.Form):

    first_name = forms.CharField(label='', max_length=40)
    middle_name = forms.CharField(label='', max_length=40)
    last_name = forms.CharField(label='', max_length=40)
    email = forms.EmailField()
    phone = forms.CharField(label='', max_length=40)
    amount = forms.
