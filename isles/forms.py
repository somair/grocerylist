# isles/forms.py
from __future__ import absolute_import
#
from django.forms import ModelForm, TextInput, CheckboxSelectMultiple

from . import models

class IsleForm(ModelForm):
    class Meta:
        fields = (
            'name',
            'notes',
            'content',
            )
        model = models.Isle
        widgets = {
            'name' : TextInput(), 
            'content' : CheckboxSelectMultiple(),
            }
        
    def __init__(self, *args, **kwargs):
        super(IsleForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['size'] = 1
        self.fields['name'].widget.attrs['maxlength'] = 2 # This is enforced by a regex in models. *sad panda*
        self.fields['notes'].widget.attrs['rows'] = 8
        self.fields['notes'].widget.attrs['cols'] = 16
