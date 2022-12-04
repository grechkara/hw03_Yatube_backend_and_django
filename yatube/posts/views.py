from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Group, User
from .forms import PostForm

OBJECTS_PER_PAGE = 10

def paginator_creater(request, obj_list):
    paginator = Paginator(obj_list, OBJECTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


def index(request):
    post_list = Post.objects.all()
    page_obj = paginator_creater(request, post_list)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def profile(request, username):
    user_profile = get_object_or_404(User, username=username)
    post_list = Post.objects.filter(author=user_profile).all()
    page_obj = paginator_creater(request, post_list)
    amount_of_posts = post_list.count()
    context = {
        'user_profile': user_profile,
        'page_obj': page_obj,
        'amount_of_posts': amount_of_posts,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    detailed_post = get_object_or_404(Post, id=post_id)
    post_list = detailed_post.author.posts.all() 
    amount_of_posts = post_list.count()
    context = {
        'detailed_post': detailed_post,
        'amount_of_posts': amount_of_posts,
    }
    return render(request, 'posts/post_detail.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.all()
    page_obj = paginator_creater(request, post_list)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


@login_required
def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:profile', post.author)
    context = {
        'form': form
    }
    return render(request, 'posts/create_post.html', context)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return redirect('posts:post_detail', post_id)
    form = PostForm(request.POST or None, instance=post)
    context = {
        'form': form,
        'is_edit': True,
    }
    return render(request, 'posts/create_post.html', context)
