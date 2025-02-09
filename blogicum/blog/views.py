from django.shortcuts import render
from django.utils import timezone

from .models import Post, Category


def index(request):
    template = 'blog/index.html'
    posts = [i for i in Post.objects.filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=timezone.now()
    )[:5]]
    # print(posts[0].author)
    # print([str(post.author) + " : " + post.text[:32] for post in posts])
    context = {'post_list': posts[::-1]}
    return render(request, template, context)


def post_detail(request, id):
    template = 'blog/detail.html'
    try:
        if post := Post.objects.get(
                pk=id,
                is_published=True,
                pub_date__lte=timezone.now(),
                category__is_published=True
        ):
            context = {'post': post}
            return render(request, template, context)
    except Exception as e:
        print(e)
        pass

    return render(request, "errors/404.html",
                  status=404, context={"details": f"Не найден пост {id}."})


def category_posts(request, category_slug):
    template = 'blog/category.html'
    try:
        category = Category.objects.get(
            slug=category_slug,
            is_published=True
        )
        context = {
            'post_list': [i for i in Post.objects.filter(
                category=category,
                is_published=True,
                pub_date__lte=timezone.now()
            )],
            'category': category_slug,
        }
        if context['post_list']:
            return render(request, template, context)
    except Exception:
        pass

    return render(
        request,
        "errors/404.html",
        status=404,
        context={"details": f"Не найда категория {category_slug}."}
    )
