from crispy_forms.bootstrap import InlineRadios
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout
from django import forms
from logserver.models import MQTTDevice
from mqtt.mqtt_logic import get_mqtt_cmd_list, get_mqtt_logger_modules_start, get_mqtt_publish_filter_list


class MQTTDeviceAddForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Привязать'))

    class Meta:
        model = MQTTDevice
        fields = [
            'modem_id',
        ]
        labels = {
            'modem_id': 'Номер модема на Китбоксе',
        }


class MQTTCmdForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cmd'] = forms.ChoiceField(widget=forms.Select(attrs={"onChange": "MqttCmdSelectOnChange(this)"}),
                                               choices=get_mqtt_cmd_list(),
                                               label="Выберите команду:")
        self.fields['publish_filter'] = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(),
                                                                  choices=get_mqtt_publish_filter_list(),
                                                                  label="Фильтр событий",
                                                                  required=False)
        self.fields['logger_filter'] = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(),
                                                                 choices=get_mqtt_logger_modules_start(),
                                                                 label="Запись логов из модулей:",
                                                                 required=False)

        self.helper = FormHelper()
        # self.helper.form_tag = False
        # self.helper.disable_csrf = True
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Отправить'))
