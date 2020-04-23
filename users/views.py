from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.shortcuts import render


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            selection = form.data['selection']
            # working on stuff below
            #group = Group.objects.get(name=selection)
            #group.user_set.add(request.user.id)
            messages.success(request, f'Your account has been created! You are now able to login {username}!')

            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'users/profile.html')
