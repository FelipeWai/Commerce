from django import forms
from .models import Categories


categories = Categories.objects.all()
CATEGORY_CHOICES = [(category.id, category.category_name) for category in categories]
CATEGORY_CHOICES.insert(0, (None, '---'))

class CreateListingForm(forms.Form):
    title = forms.CharField(max_length=100, label='Title')
    description = forms.CharField(widget=forms.Textarea, label='Description')
    starting_bid = forms.DecimalField(max_digits=10, decimal_places=2, label='Starting Bid')
    image_url = forms.URLField(required=False, label='Image URL')
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, required=False, label='Category')
