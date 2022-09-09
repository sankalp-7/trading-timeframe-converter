from dataclasses import fields
from socket import fromshare
from django import forms 
from.models import csv 

class csvform(forms.ModelForm):
    class Meta:
        model=csv 
        fields=('csv_file','timeframe')