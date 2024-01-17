from django import forms
from .models import Item
INPUT_CLASSES='w-2/3 flex rounded-xl border bg-gray-500'
class Sellerform(forms.ModelForm):
    class Meta:
        model=Item
        fields=('category','name','description','price','country','district','state','village')
        widgets={
            'category':forms.Select(attrs={
                'class':INPUT_CLASSES
            }),

             'name':forms.TextInput(attrs={
                'class':INPUT_CLASSES
            }),

             'description':forms.Textarea(attrs={
                'class':INPUT_CLASSES
            }),
             'country':forms.Select(attrs={
                'class':INPUT_CLASSES
            }),
             'state':forms.Select(attrs={
                'class':INPUT_CLASSES
            }),
             'district':forms.Select(attrs={
                'class':INPUT_CLASSES
            }),
             'village':forms.TextInput(attrs={
                'class':INPUT_CLASSES
            }),

             'price':forms.TextInput(attrs={
                'class':INPUT_CLASSES
            })
        }


class Edititemform(forms.ModelForm):
    class Meta:
        model=Item
        fields=('name','description','price','country','district','state','village','is_sold')
        widgets={ 
            'name':forms.TextInput(attrs={
                'class':INPUT_CLASSES
            }),

             'description':forms.Textarea(attrs={
                'class':INPUT_CLASSES
            }),

             'price':forms.TextInput(attrs={
                'class':INPUT_CLASSES
            }),
              'country':forms.Select(attrs={
                'class':INPUT_CLASSES
            }),
              'district':forms.Select(attrs={
                'class':INPUT_CLASSES
            }),
              'state':forms.Select(attrs={
                'class':INPUT_CLASSES
            }),
              'village':forms.TextInput(attrs={
                'class':INPUT_CLASSES
            }),

        }