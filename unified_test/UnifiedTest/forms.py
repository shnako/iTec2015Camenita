from django import forms

from UnifiedTest.models import Page

class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ('ref', 'url', 'status_code', 'delay', 'response',
                  'dynamic_code')
