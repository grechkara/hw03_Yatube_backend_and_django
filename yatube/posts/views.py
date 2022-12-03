from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Group, User
from .forms import PostForm


def index(request):
    post_list = Post.objects.all()
    # Показывать по 10 записей на странице.
    paginator = Paginator(post_list, 10)
    # Из URL извлекаем номер запрошенной страницы - это значение параметра page
    page_number = request.GET.get('page')
    # Получаем набор записей для страницы с запрошенным номером
    page_obj = paginator.get_page(page_number)
    # Отдаем в словаре контекста
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def profile(request, username):
    user_profile = get_object_or_404(User, username=username)
    post_list = Post.objects.filter(author=user_profile).all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    amount_of_posts = post_list.count()
    # Здесь код запроса к модели и создание словаря контекста
    context = {
        'user_profile': user_profile,
        'page_obj': page_obj,
        'amount_of_posts': amount_of_posts,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    detailed_post = Post.objects.get(id=post_id)
    post_list = Post.objects.filter(author=detailed_post.author).all()
    amount_of_posts = post_list.count()
    # Здесь код запроса к модели и создание словаря контекста
    context = {
        'detailed_post': detailed_post,
        'amount_of_posts': amount_of_posts,
    }
    return render(request, 'posts/post_detail.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = Post.objects.filter(group=group).all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
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
    if post.author == request.user:
        form = PostForm(request.POST or None, instance=post)
        if request.method == 'GET':
            context = {
                'form': form,
                'is_edit': post,
            }
            return render(request, 'posts/create_post.html', context)
        if request.method == 'POST':
            if form.is_valid():
                post.save()
    return redirect('posts:post_detail', post_id)
