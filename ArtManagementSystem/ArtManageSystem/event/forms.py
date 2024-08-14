from django import forms
from  django.core.exceptions import ValidationError
from event.models import SuggestionBox,Registration,Event


class SuggestionBoxForm(forms.ModelForm):


    def clean_description(self):
        description= self.cleaned_data['description'].strip()
        if len(description) < 20:
            raise ValidationError('Atleast 20 characters required for description',code='invalid')
        return description



    class Meta:
        model= SuggestionBox
        fields=['category','description','event']


class BlogForm(forms.Form):
    title = forms.CharField(max_length=256, required=True)
    description= forms.CharField(widget=forms.Textarea)
    event = forms.ModelChoiceField(queryset=Event.objects.all())
    date = forms.DateField()
    time = forms.TimeField()
    datetime = forms.DateTimeField()
    file = forms.FileField()
    quantity = forms.IntegerField()
    choices = forms.ChoiceField(choices=[
        ('A','a'),
        ('B','b'),
        ('C','c')
    ])
