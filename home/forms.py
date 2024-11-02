from django import forms

choices = [
        ('nyt', "New York Times Dataset"),
        ('healthcare', "Old Age Home Reports Dataset"),
        ('nursing', "Nursing Home Reports Dataset"),
    ]
 
# creating a form
class TrendForm(forms.Form):

    model_type = forms.ChoiceField(choices=choices)

    base_term = forms.CharField(max_length = 200, required=True, 
        widget=forms.TextInput(attrs={'class': 'form-control basicAutoComplete',}))
    
    rel_term1 = forms.CharField(max_length = 200, required=True, 
        widget=forms.TextInput(attrs={'class': 'form-control basicAutoComplete',}))

    rel_term2 = forms.CharField(max_length = 200, required=True, 
        widget=forms.TextInput(attrs={'class': 'form-control basicAutoComplete',}))

    rel_term3 = forms.CharField(max_length = 200, required=True, 
        widget=forms.TextInput(attrs={'class': 'form-control basicAutoComplete',}))

    rel_term4 = forms.CharField(max_length = 200, required=True, 
        widget=forms.TextInput(attrs={'class': 'form-control basicAutoComplete',}))
    

class ReverseForm(forms.Form):

    model_type = forms.ChoiceField(choices=choices)

    base_term = forms.CharField(max_length = 200, required=True, 
        widget=forms.TextInput(attrs={'class': 'form-control basicAutoComplete',}))
    
    rel_term1 = forms.CharField(max_length = 200, required=True, 
        widget=forms.TextInput(attrs={'class': 'form-control basicAutoComplete',}))

    rel_term2 = forms.CharField(max_length = 200, required=True, 
        widget=forms.TextInput(attrs={'class': 'form-control basicAutoComplete',}))
