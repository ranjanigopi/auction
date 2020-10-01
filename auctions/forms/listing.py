from django import forms

from ..models import Category

class Listing(forms.Form):
    name = forms.CharField(label="Product Name", widget=forms.TextInput(attrs={"placeholder": "Enter Product Name"}))
    category = forms.ModelChoiceField(label="Product Category", queryset=Category.objects.all()) 
    current_price = forms.DecimalField(max_digits=10, decimal_places=2,label="Bid Amount", widget=forms.NumberInput(attrs={"placeholder": "Enter Start Bid Amount"}))
    description = forms.CharField(label="Description", widget=forms.Textarea(attrs={"placeholder": "Enter Product Description"}))
    image_url = forms.CharField(label="Image URL", widget=forms.URLInput(attrs={"placeholder": "Enter Image URL"}))
