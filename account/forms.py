from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from .models import CustomUser

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'
    }))
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'class': 'custom-control-input',
        'id': 'remember-me'
    }))

class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control form-control-user',
            'placeholder': 'Email Address'
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-user',
            'placeholder': 'Password'
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-user',
            'placeholder': 'Repeat Password'
        })
    )
    
    class Meta:
        model = CustomUser
        fields = ('email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Yardım metinlerini kaldır
        for field in self.fields.values():
            field.help_text = None
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
            
    def save(self, commit=True):
        user = super().save(commit=False)
        email = self.cleaned_data["email"]
        username = email.split('@')[0]
        count = 1
        while CustomUser.objects.filter(username=username).exists():
            username = f"{email.split('@')[0]}{count}"
            count += 1
        user.username = username
        if commit:
            user.save()
        return user

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'avatar', 'bio')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'avatar': forms.FileInput(attrs={'class': 'form-control-file'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.username_changed:
            self.fields['username'].disabled = True
            self.fields['username'].widget.attrs['readonly'] = True
            self.fields['username'].help_text = 'Kullanıcı adı sadece bir kez değiştirilebilir.'

    def clean(self):
        cleaned_data = super().clean()
        if self.instance and self.instance.username_changed:
            cleaned_data['username'] = self.instance.username
        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if self.instance and self.instance.pk:
            if self.instance.username_changed and username != self.instance.username:
                raise forms.ValidationError('Kullanıcı adınızı sadece bir kez değiştirebilirsiniz.')
        return username

class PasswordChangeCustomForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
