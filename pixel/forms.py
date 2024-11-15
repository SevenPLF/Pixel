# forms.py
from django import forms

class SearchForm(forms.Form):
    query = forms.CharField(label='搜索', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '输入搜索内容...'}))



