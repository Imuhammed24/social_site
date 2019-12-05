from .models import Image
from .forms import ImageCreateForm
from actions.utils import create_action
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST


@login_required()
def image_create(request):
    if request.method == 'POST':
        print('posted')
        form = ImageCreateForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            # cd = form.cleaned_data
            new_item = form.save(commit=False)
            new_item.user = request.user
            new_item.save()
            create_action(request.user, 'added', new_item)
            messages.success(request, 'Image Added Successfully')
            # return redirect(new_item.get_absolute_url())
            return redirect('profile')
    else:
        form = ImageCreateForm()
    return render(request, 'images/create.html', {'display_section': 'images',
                                                  'form': form})


@login_required
def image_detail(request, i_d, slug):
    post = get_object_or_404(Image, id=i_d, slug=slug)

    if post.users_like.filter(id=request.user.id).exists():
        is_liked = True
    else:
        is_liked = False

    context = {'total_no_likes': post.users_like.count,
               'users_like': post.users_like.all,
               'display_section': 'images',
               'is_liked': is_liked,
               'post': post}
    return render(request, 'images/detail.html', context)


@login_required
def list_view(request):
    posts = Image.objects.all()
    paginator = Paginator(posts, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        posts = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request, 'images/list_ajax.html', {'display_section': 'images',
                                                         'posts': posts})
    return render(request, 'images/list.html', {'display_section': 'images',
                                                'posts': posts})


@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('post_id')
    post = get_object_or_404(Image, id=image_id)
    if post.users_like.filter(id=request.user.id).exists():
        post.users_like.remove(request.user)
        is_liked = False
    else:
        post.users_like.add(request.user)
        create_action(request.user, 'likes', post)
        is_liked = True

    context = {'post': post,
               'is_liked': is_liked,
               'total_no_likes': post.users_like.count,
               'users_like': post.users_like.all}
    if request.is_ajax():
        html = render_to_string('like_section.html', context, request=request)
        return JsonResponse({'form': html})
