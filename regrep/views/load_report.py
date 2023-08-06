from django.shortcuts import render
from regrep.models import MetaData
from regrep.forms import LoadForm

# Create your views here.
def load_report(req):
    form = LoadForm()
    