from django import forms


class BidForm(forms.Form):
    newbid = forms.CharField(label='Your Price', max_length=10)