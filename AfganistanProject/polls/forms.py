from django import forms


class SearchInDbForm(forms.Form):
    index_for_req = forms.CharField(label="Wyszukaj w bazie", max_length=255)
