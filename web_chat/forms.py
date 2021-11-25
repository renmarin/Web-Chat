from django import forms


class SignUpIn(forms.Form):
    username = forms.CharField(label="Username", max_length=25,
                               widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(label="Password", max_length=100,
                               widget=forms.TextInput(attrs={'placeholder': 'Password'}))


class ChooseRoom(forms.Form):
    room = forms.CharField(label="Room name", max_length=25,
                           widget=forms.TextInput(attrs={'placeholder': 'Room name'}))


class DelaySend(forms.Form):
    date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    # time = forms.TimeField(widget=forms.widgets.TimeInput(attrs={'type': 'time'}), format='%Y-%m-%d  %H:%M')
    time = forms.TimeField(widget=forms.widgets.TimeInput(attrs={'type': 'time', 'format': '%H:%M:%S'}))
    message = forms.CharField(label="Message", max_length=500,
                               widget=forms.Textarea(attrs={'placeholder': 'Message'}))
    CHOICES = [('Anon', 'Anon'), ('NotAnon', 'NotAnon')]
    anon = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)

    # date = forms.CharField(label="Date", max_length=25)
    # time = forms.CharField(label="Time", max_length=25)
    # message = forms.CharField(label="Message", max_length=500,
    #                            widget=forms.TextInput(attrs={'placeholder': 'Message'}))


class Tok(forms.Form):
    token = forms.CharField(label="Token", max_length=250)