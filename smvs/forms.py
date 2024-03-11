from django.forms import ModelForm
from django import forms
from .models import Election, Candidate
from django.forms.widgets import DateTimeInput
import datetime

class create_candidate(ModelForm):
    class Meta:
        model = Candidate
        fields = "__all__"

class create_election(forms.ModelForm):
    # Override the candidates field to use a checkbox widget
    candidates = forms.ModelMultipleChoiceField(queryset=Candidate.objects.all(), widget=forms.CheckboxSelectMultiple)
    
    class Meta:
        # Specify the model and the fields to include in the form
        model = Election
        fields = ["position", "candidates", "user", "startDateTime", "endDateTime"]
    def __init__(self, *args, **kwargs):
        # Get the candidates queryset from the kwargs
        candidates = kwargs.pop("candidates", None)
        # Call the parent constructor
        super().__init__(*args, **kwargs)
        # Set the candidates queryset to the field
        if candidates is not None:
            self.fields["candidates"].queryset = candidates