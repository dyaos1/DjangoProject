from django import forms
from regrep.models import MetaData, PrintHistory, ContractInfo


class LoadForm(forms.ModelForm):
    class META:
        model = MetaData
        fields = ["id", "report_name"]