from django import forms

from UnifiedTest.models import Page

class PageForm(forms.ModelForm):
    url = forms.URLField()

    class Meta:
        model = Page
        fields = ('ref', 'url', 'status_code', 'delay', 'response',
                  'dynamic_code')
