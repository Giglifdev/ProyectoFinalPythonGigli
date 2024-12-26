from django import forms
from .models import Blog
from .models import Message

#post
class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'subtitle', 'body', 'image']
        
        
        
#mensajes
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['receiver', 'content']