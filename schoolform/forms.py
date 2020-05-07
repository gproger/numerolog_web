from django import forms


class RefundForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    is_percent = forms.BooleanField(default=False, label=u'Возврат в процентах?')
    amount = forms.IntegerField(label=u'Сумма возврата')