from django import forms
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

from rango.models import Page, Category, UserProfile


class CategoryForm(forms.ModelForm):
    name = forms.CharField(
        max_length=128,
        help_text="Please enter the category name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Category
        fields = ('name',)

    def clean(self):
        cleaned_data = super(CategoryForm, self).clean()
        name = cleaned_data.get('name')

        if Category.objects.filter(slug=slugify(name)).exists():
            msg = "That category already exists"
            self.add_error('slug', msg)

        return cleaned_data


class PageForm(forms.ModelForm):
    title = forms.CharField(
        max_length=128,
        help_text="Please enter the title of the page."
        )
    url = forms.URLField(
        max_length=200,
        help_text="Please enter the URL of the page."
        )
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Page
        exclude = ('category',)

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        if url and not url.startswith('http://'):
            url = 'http://' + url
            cleaned_data['url'] = url

        return cleaned_data


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')
