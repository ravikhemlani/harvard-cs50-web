from django import forms


class WikiPage(forms.Form):
    title = forms.CharField(label="Title", max_length=20, widget=forms.TextInput(
        attrs={'style': 'width:50%', 'class': 'form-control'}))
    markdown_content = forms.CharField(label="Content", widget=forms.Textarea(
        attrs={'style': 'height:300px; width:50%;', 'class': 'form-control'}))


class EditPage(forms.Form):
    markdown_content = forms.CharField(label="Content", widget=forms.Textarea(
        attrs={'style': 'height:300px; width:50%;', 'class': 'form-control'}))