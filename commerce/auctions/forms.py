from .models import AuctionListing, Categories, Comments
from django import forms


class CreateListingForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Categories.objects.all(),
                                      widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = AuctionListing

        fields = ["title", "description", "starting_bid", "category", "image"]
        labels = {"title": "Title", "description": "Description", "starting_bid": "Starting Bid",
                  "category": "Category", "image": "Image URL"}

        widgets = {"title": forms.TextInput(attrs={'class': 'form-control'}),
                   "description": forms.Textarea(attrs={'class': 'form-control'}),
                   "starting_bid": forms.NumberInput(attrs={'class': 'form-control'}),
                   "image": forms.URLInput(attrs={'class': 'form-control',
                                                  'placeholder': "Enter URL source for image (Optional)"})}

    def clean_bid(self):
        bid = self.cleaned_data['starting_bid']
        if bid < 0.0:
            raise forms.ValidationError("Please enter a non negative number")
        return self.cleaned_data["starting_bid"]

    def clean_title(self):
        title = self.cleaned_data['title']
        same_titles = AuctionListing.objects.filter(title__iexact=title)
        if same_titles:
            raise forms.ValidationError("Title is already in use. Please use another title name.")
        return title

    # def clean(self):
    #     cleaned_data = super().clean()
    #     bid_data = float(cleaned_data.get('bid'))
    #     if bid_data < 0:
    #         raise forms.ValidationError({'bid': ["Please enter a number higher than 0"]})
    #     return cleaned_data


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ["content"]
        widgets = {"content": forms.Textarea(attrs={"class": "form-control"})}


