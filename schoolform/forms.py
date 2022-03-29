from django import forms


class RefundForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    is_percent = forms.BooleanField(initial=False, label=u'Возврат в процентах?', required=False)
    amount = forms.IntegerField(label=u'Сумма возврата', required=True, initial=0)

class EmailTemplateForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    template = forms.CharField(required=True, label=u'Шаблон письма', widget=forms.Textarea(attrs={'rows': 40, 'cols': 80}))
