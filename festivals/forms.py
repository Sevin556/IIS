from django.forms import ModelForm, TextInput, DateInput, DateField
from . import models
from datetime import date

class NewFestivalForm(ModelForm):

    class Meta:
        model = models.t_festival
        labels ={
            "nazov": "name",
            "rocnik": "edition number",
            "popis": "description",
            "miesto": "location",
            "zaciatok": "start",
            "koniec": "end",
            "kapacita": "capacity",
            "obrazok": "thumbnail picture URL(if you dont have any use given placeholder)",
        }
        fields = ['nazov', 'rocnik', 'popis', 'miesto', 'zaciatok', 'koniec', 'kapacita', 'obrazok']
        widgets = {
            'nazov': TextInput(attrs={'placeholder': 'Grape'}),
            'miesto': TextInput(attrs={'placeholder': 'Letisko Piešťany'}),
            'rocnik': TextInput(attrs={'placeholder': '12'}),
            'zaciatok': DateInput(format=('%m/%d/%Y'), attrs={'type': 'date','min': date.today(), 'value': date.today()}),
            'koniec': DateInput(format=('%m/%d/%Y'), attrs={'type': 'date','min': date.today(), 'value': date.today()}),
            'kapacita': TextInput(attrs={'placeholder': '5000'})
        }



class NewStageForm(ModelForm):

    class Meta:
        model = models.t_stage
        exclude = ('festival_id',)
        widgets = {
            'nazov': TextInput(attrs={'placeholder': 'name'}),
            'miesto': TextInput(attrs={'placeholder': 'Description of stage...RnB, pop, rap stage etc'}),
        }


class NewInterpretForm(ModelForm):
    
    class Meta:
        model = models.t_interpret
        fields = ['nazov', 'datum_vzniku', 'clenovia', 'albumy']

        
class NewTicketForm(ModelForm):
    
    class Meta:
        model = models.t_listok
        labels ={
            "cena": "price (€ per piece)",
            "typ": "type",
            "pocet": "number of tickets",
            "popis": "description",
        }
        fields = ['cena', 'typ', 'pocet', 'popis']
        widgets = {
            'cena': TextInput(attrs={'placeholder': '10'}),
            'pocet': TextInput(attrs={'placeholder': '500'}),
            'typ': TextInput(attrs={'placeholder': 'Normal, VIP...'}),
            'popis': TextInput(attrs={'placeholder': 'Description of benefits'}),
        }
