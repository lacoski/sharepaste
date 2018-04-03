from django import forms
from .models import Paste


class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)


class PasteForm(forms.ModelForm):    
    class Meta:
        model = Paste
        fields = ['paste_name', 'type_content_paste','content_paste', 'user_own', 'short_link']

class PasteCreateForm(forms.ModelForm):
    class Meta:
        model = Paste
        fields = ['paste_name', 'type_content_paste','content_paste', 'user_own']       
        widgets = {
            'paste_name': forms.fields.TextInput(attrs={               
                'class': 'form-control',
            }),
            'type_content_paste': forms.Select(                
                attrs={               
                    'class': 'form-control',
                }
            ),
            'content_paste': forms.Textarea(attrs={               
                'class': 'form-control'
            }),
            'user_own': forms.Select(attrs={               
                'class': 'form-control',
            }),           
        }
        