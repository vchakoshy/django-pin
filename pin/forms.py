from django import forms
from django.forms.models import ModelForm
from pin.models import Post


class PinForm(ModelForm):
    class Meta:
        model=Post
        exclude = ('user', 'like', 'timestamp', 'category')
        
class PinDirectForm(forms.Form):
    image = forms.ImageField()
    description = forms.CharField()
    
class PinUpdateForm(ModelForm):
    class Meta:
        model=Post
        exclude = ('user', 'like', 'timestamp', 'image','category')
        