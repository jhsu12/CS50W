from django import forms
from .models import User, Auction, Category

class Auctionform(forms.ModelForm):

    class Meta:
        model = Auction
        fields = ("title", "description", "start_bid", "image", "category")
        widgets = {'category' : forms.Select(choices=Category.objects.all()),
                   'image' : forms.TextInput(),
                   'title': forms.TextInput(attrs={'class': 'form-control'}),
                   'description': forms.Textarea(attrs={'class': 'form-control'}),
                   'start_bid': forms.NumberInput()} 
        
    #title, description, starting bid, image url, category 
    