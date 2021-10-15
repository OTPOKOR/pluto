from django import forms
class Searchform(forms.Form):
    # 사이트선택
    site_choices = [('내셔널지오그래픽','내셔널지오그래픽'),('코닥','코닥')]
    site_select = forms.MultipleChoiceField(
        widget=forms.Select(attrs={'class':'form-select','aria-label':'Default select example'}),
        choices=site_choices,
        label='사이트선택',
        )

    # url검색
    search_url = forms.CharField(
        label='url',
        widget=forms.TextInput(attrs={'class':'form-control'}),
        )