from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import (
    HttpResponseForbidden,
    HttpResponseNotFound,
    HttpResponseRedirect,
    HttpResponseBadRequest,
    HttpResponse


)
from django.shortcuts import render, redirect
from django.utils import timezone
from django.urls import reverse, reverse_lazy
from django.core.paginator import Paginator

from django.contrib.auth import get_user_model
from django.views.generic import CreateView, UpdateView

from .models import Post, Category, Comment
from .forms import CommentForm, PostForm


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
    ).order_by('-pub_date')
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
            comments = Comment.objects.filter(post=post).order_by('created_at')
            context = {
                'post': post,
                'form': CommentForm(),
                'comments': comments,
            }
            return render(request, template, context)
    except Exception as e:
        print(e, type(e))
        # raise e
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
        # context = {
        #     'post_list': [i for i in Post.objects.filter(
        #         category=category,
        #         is_published=True,
        #         pub_date__lte=timezone.now()
        #     )],
        #     'category': category_slug,
        # }
        # if context['post_list']:
        #     return render(request, template, context)
        filter_obj = Post.objects.filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=timezone.now(),
            category=category

        ).order_by('-pub_date')
        paginator = Paginator(filter_obj, 10)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {'page_obj': page_obj}
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

    if request.user.is_authenticated and request.user.id == user.id:
        filter_obj = Post.objects.filter(
            author=user,
        ).order_by('-pub_date')
    else:
        filter_obj = Post.objects.filter(
            author=user,
            is_published=True,
            category__is_published=True,
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')
    paginator = Paginator(filter_obj, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    comment_form = CommentForm()

    context = {
        'profile': user,
        'page_obj': page_obj,

    }
    return render(request, template, context)


# @method_decorator(staff_member_required, name='dispatch')
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    fields = ['first_name', 'last_name']
    template_name = 'blog/profile_update.html'
    success_url = reverse_lazy('blog:profile')

    def get_object(self, queryset=None):
        return self.request.user

class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    fields = []
    template_name = ...  # todo


def self_profile_view(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden(
            "Требуется авторизация"
        )
    return user_profile(request, request.user.username)


def add_comment(request, post_id):
    if request.user.is_authenticated:
        form = CommentForm(request.POST)
        form.post_id = post_id
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = Post.objects.get(pk=post_id)
            comment.save()
            # print(comment)
            return redirect('blog:post_detail', post_id)
        else:
            # print(form.errors)
            return redirect('blog:post_detail', post_id)
    return redirect('login')


def update_post(request, pk=None):
    if not request.user.is_authenticated:
        return HttpResponseForbidden()

    if request.method == "GET":
        form = PostForm()
        context = {'form': form}
        template = 'blog/create.html'
    else:
        form = PostForm(request.POST or None)

        if form.is_valid():
            # form.save()
            post = form.save(commit=False)
            # post.author = request.user
            if pk is not None:
                post.id = pk
            post.author = request.user
            post.save()
        else:
            return HttpResponseBadRequest(form.errors)
        # return HttpResponse(status=200)
        return redirect("blog:post_detail", post.id)
    return render(request, template, context)


