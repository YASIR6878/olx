from django import forms
from .models import ConversationMessages
INPUT_CLASSES='w-full h-8 py-4 px-6 rounded-xl border mb-2'
class ConversationmessageForm(forms.ModelForm):
    class Meta:
        model=ConversationMessages
        fields=('content',)
        widgets={
            'content':forms.Textarea(attrs={
                'class':INPUT_CLASSES
            })
        }