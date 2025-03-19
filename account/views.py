from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from .forms import LoginForm, RegisterForm, ProfileUpdateForm, PasswordChangeCustomForm  # ProfileUpdateForm eklendi
from django.core.mail import send_mail

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if form.cleaned_data.get('remember_me'):
                request.session.set_expiry(1209600)  # 2 weeks
            else:
                request.session.set_expiry(0)
            login(request, user)
            messages.success(request, 'Başarıyla giriş yaptınız.')
            return redirect('home_page')
        else:
            messages.error(request, 'Lütfen bilgilerinizi kontrol ediniz.')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Hoşgeldin e-postası gönder
            send_mail(
                'Hoş Geldiniz',
                f'Merhaba {user.username}, sitemize hoş geldiniz!',
                'noreply@example.com',  # Gönderen e-posta
                [user.email],  # Alıcı e-posta
                fail_silently=False,
            )
            
            login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect('home_page')
    else:
        form = RegisterForm()
    return render(request, 'account/register.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'Successfully logged out.')
    return redirect('home_page')

def profile_view(request):
    return render(request, 'account/profile.html')

@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            
            # Eğer kullanıcı adı değiştirilmişse ve daha önce değiştirilmemişse
            if user.username != request.user.username:
                if request.user.username_changed:
                    messages.error(request, 'Kullanıcı adınızı sadece bir kez değiştirebilirsiniz.')
                    return redirect('profile_edit')
                user.username_changed = True
                messages.success(request, 'Kullanıcı adınız başarıyla değiştirildi.')
            
            user.save()
            messages.success(request, 'Profil başarıyla güncellendi.')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'account/profile_edit.html', {'form': form})

@login_required
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeCustomForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Parolanız başarıyla değiştirildi.')
            return redirect('profile')
    else:
        form = PasswordChangeCustomForm(request.user)
    return render(request, 'account/password_change.html', {'form': form})
