from crispy_forms.bootstrap import InlineRadios
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout
from django import forms
from logserver.models import KitBox


class KitboxAddForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Привязать'))

    class Meta:
        model = KitBox
        fields = [
            'modem_id',
        ]
        labels = {
            'modem_id': 'Номер модема на Китбоксе',
        }
