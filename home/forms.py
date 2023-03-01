from django import forms
 
# creating a form
class TrendForm(forms.Form):
    # COMMENT : add trend models here
    choices = [
        ('nyt', "New York Times Dataset"),
        ('healthcare', "Old Age Home Reports Dataset"),
    ]

    model_type = forms.ChoiceField(choices=choices)

    # TODO : add logic to make the base term only selectable in commom words autofil dropdown

    base_term = forms.CharField(max_length = 200, required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control basicAutoComplete',
        }))
    
    rel_term1 = forms.CharField(max_length = 200, required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control basicAutoComplete',
        }))

    rel_term2 = forms.CharField(max_length = 200, required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control basicAutoComplete',
        }))

    rel_term3 = forms.CharField(max_length = 200, required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control basicAutoComplete',
        }))

    rel_term4 = forms.CharField(max_length = 200, required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control basicAutoComplete',
        }))
