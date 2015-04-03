from django import forms

from UnifiedTest.models import Page

class CreatePageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ('url', 'status_code', 'delay', 'response', 'dynamic_code')
