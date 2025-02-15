from django.http import HttpResponseForbidden, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from django.urls import reverse
from django.core.paginator import Paginator

from django.contrib.auth import get_user_model
from django.views.generic import CreateView, UpdateView

from .models import Post, Category


def index(request):
    template = 'blog/index.html'
    # posts = [i for i in Post.objects.filter(
    #     is_published=True,
    #     category__is_published=True,
    #     pub_date__lte=timezone.now()
    # )[:5]]

    filter_obj = Post.objects.filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=timezone.now()
    )
    paginator = Paginator(filter_obj, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'page_obj': page_obj}
    # {'post_list': posts[::-1]}
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

def user_profile(request, username):
    # if not request.user.is_authenticated:
    #     return HttpResponseForbidden(
    #         "403. Не авторизованным пользователям запрещено смотреть информацию о пользователях."
    #     )
    template = 'blog/profile.html'
    try:
        user = get_user_model().objects.get(username=username)
    except get_user_model().DoesNotExist:
        # return HttpResponseRedirect(reverse("pages:404"))
        return render(
            request,
            "errors/404.html",
            status=404,
            context={"details": f"Пользователь {username} не найден."}
        )
    if not user:
        return HttpResponseNotFound(F"Нет пользователя с таким именем: {username}")

    filter_obj = Post.objects.filter(
        author=user,
        is_published=True,
        category__is_published=True,
        pub_date__lte=timezone.now()
    )
    paginator = Paginator(filter_obj, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'profile': user,
        'page_obj': page_obj,

    }
    return render(request, template, context)

# @method_decorator(staff_member_required, name='dispatch')
class ProfileUpdateView(UpdateView):
    model = get_user_model()
    fields = ['first_name', 'last_name']
    template_name = 'blog/profile_update.html'