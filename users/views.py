from .forms import ProfileUpdateForm
from .forms import UserRegisterForm
from .forms import UserUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.shortcuts import render

# .....


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            username = form.cleaned_data.get('username')
            selection = form.data['selection']

            user_group = Group.objects.get_or_create(name=form.data['username'])
            group = Group.objects.get(name=selection)
            user.groups.add(group)

            # if the user selects to be a teacher, create a classroom(group) for that user
            # named after their username. This user will be part of group Teacher and their username
            # Ex. username = John -- the user will be part of group Teacher and John
            if group.name == "Teacher":
                group = Group.objects.get(name=form.data['username'])
                user.groups.add(group)

            messages.success(request, f'Your account has been created! You are now able to login {username}!')

            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/profile.html', context)
