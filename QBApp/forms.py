from django import forms

from . import boomiAPIBuildRequests
from . import boomiAPIParseResults

import logging


class SearchForm(forms.Form):
    """ Definition of the main search form used in the "main" landing page after login.
    """

    # TODO: Check and refactor the field named environment because right now is the
    # atom's information what is showed there.
    def __init__(self, atomsLoV, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.fields['environment'] = forms.ChoiceField(label="Environment", choices=atomsLoV)
        self.fields['environment'].widget.attrs.update({'class' : 'custom-select d-block w-100'})
        self.fields['environment'].widget.attrs.update({'id' : 'environment'})
        self.fields['environment'].widget.attrs.update({'required' : ''})

        self.fields['processesToFind'] = forms.CharField(label="Filter to find the processes you need", max_length=100)
        self.fields['processesToFind'].widget.attrs.update({'class' : 'form-control'})
        self.fields['processesToFind'].widget.attrs.update({'id' : 'processesToFind'})
        self.fields['processesToFind'].widget.attrs.update({'placeholder' : ''})
        self.fields['processesToFind'].widget.attrs.update({'value' : ''})
        self.fields['processesToFind'].widget.attrs.update({'required' : ''})


class LoginForm(forms.Form):
    """ Definition of the login form located on the home page.
    """
    email = forms.EmailField(label="email", max_length=100)
    email.widget.attrs.update({'type' : 'email'})
    email.widget.attrs.update({'id' : 'inputEmail'})
    email.widget.attrs.update({'class' : 'form-control'})
    email.widget.attrs.update({'placeholder' : 'Email address'})
    email.widget.attrs.update({'required' : ''})
    email.widget.attrs.update({'autofocus' : ''})

    password = forms.CharField(label="Password", widget=forms.PasswordInput, max_length=100)
    password.widget.attrs.update({'type' : 'password'})
    password.widget.attrs.update({'id' : 'inputPassword'})
    password.widget.attrs.update({'class' : 'form-control'})
    password.widget.attrs.update({'placeholder' : 'Password'})
    password.widget.attrs.update({'required' : ''})

    accountId = forms.CharField(label="Boomi account", max_length=100)
    accountId.widget.attrs.update({'type' : 'user'})
    accountId.widget.attrs.update({'id' : 'boomiAccountId'})
    accountId.widget.attrs.update({'class' : 'form-control'})
    accountId.widget.attrs.update({'placeholder' : 'boomiAccountId'})
    accountId.widget.attrs.update({'required' : ''})
    accountId.widget.attrs.update({'autofocus' : ''})
