from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from blog.models import Category, Post

POSTS_DISP = 5


def get_published_posts(category=None):
    """
    Возвращает QuerySet опубликованных постов.
    Если передан category, фильтрует только по этой категории.
    """
    queryset = Post.objects.all()

    base_filters = {
        'is_published': True,
        'pub_date__lte': timezone.now().date(),
        'category__isnull': False,
        'category__is_published': True,
    }
    # Если нужна конкретная категория, добавляем её к фильтрам
    if category is not None:
        base_filters['category'] = category

    return queryset.filter(**base_filters)


def index(request):
    template = 'blog/index.html'
    post_list = get_published_posts()
    post_list = post_list.select_related(
        'category',
    ).order_by('-pub_date')[:POSTS_DISP]
    context = {'post_list': post_list}
    return render(request, template, context)


def post_detail(request, post_id):
    template = 'blog/detail.html'
    valid_posts = get_published_posts()
    post = get_object_or_404(
        valid_posts,
        id=post_id,
    )
    context = {'post': post}
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True,
    )
    posts = get_published_posts(category=category)
    context = {'category': category, 'post_list': posts}
    return render(request, template, context)
