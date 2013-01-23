from django.forms.models import ModelForm
from pin.models import Post

class PinForm(ModelForm):
    class Meta:
        model=Post
        exclude = ('user', 'like', 'timestamp', 'category')
        
class PinUpdateForm(ModelForm):
    class Meta:
        model=Post
        exclude = ('user', 'like', 'timestamp', 'image','category')
        