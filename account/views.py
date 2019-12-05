from actions.models import Action
from actions.utils import create_action
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST

from .forms import LoginForm, UserRegistrationForm, ProfileEditForm, UserEditForm
from .models import Profile, Contact


# Create your views here.


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('profile')
                else:
                    return HttpResponse('Disabled Account')
            else:
                return HttpResponse('Invalid Login')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


@login_required
def account_view(request):
    actions = Action.objects.all().exclude(user=request.user)
    following_ids = request.user.following.values_list('id', flat=True)

    if following_ids:
        actions = actions.filter(user_id__in=following_ids).select_related('user',
                                                                          'user__profile').prefetch_related('target')
    actions = actions[:10]

    context = {'display_section': 'dashboard',
               'actions': actions}
    return render(request, 'account_base.html', context)


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)

        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile edited successfully')
        else:
            messages.error(request, 'Error editing profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html', {'user_form': user_form,
                                                 'profile_form': profile_form})


@login_required
def user_list_view(request):
    users = User.objects.filter(is_active=True)
    return render(request, 'account/user/user-list.html', {'display_section': 'people',
                                                           'users': users})


@login_required
def user_detail_view(request, username):
    user = get_object_or_404(User, username=username, is_active=True)
    if user.followers.filter(id=request.user.id).exists():
        is_followed = True
    else:
        is_followed = False
    return render(request, 'account/user/user-detail.html', {'display_section': 'people',
                                                             'is_followed': is_followed,
                                                             'total_no_followers': user.followers.count,
                                                             'all_followers': user.followers.all,
                                                             'total_no_following': user.following.count,
                                                             'user': user})


@login_required
@require_POST
def user_follow(request):
    user_id = request.POST.get('user_id')
    user = get_object_or_404(User, id=user_id, is_active=True)

    if user.followers.filter(id=request.user.id).exists():
        Contact.objects.filter(user_from=request.user,
                               user_to=user).delete()
        # create_action(request.user, 'is following', user)
        is_followed = False
    else:
        Contact.objects.get_or_create(user_from=request.user,
                                      user_to=user)
        create_action(request.user, 'started following', user)
        is_followed = True

    context = {'user': user,
               'is_followed': is_followed,
               'total_no_followers': user.followers.count,
               'all_followers': user.followers.all,
               'total_no_following': user.following.count,
               'display_section': 'people'}

    if request.is_ajax():
        html = render_to_string('account/user/user-follow-section.html', context, request=request)
        return JsonResponse({'form': html})


def logout_view(request):
    logout(request)
    return render(request, 'registration/logged_out.html')


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            create_action(new_user, 'just created an account')
            profile = Profile.objects.create(user=new_user)
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()

    return render(request, 'account/register.html', {'form': user_form})
