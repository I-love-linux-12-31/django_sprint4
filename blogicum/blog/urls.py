from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('', views.index, name='homepage'),
    path('posts/<int:id>/', views.post_detail, name='post_detail'),
    path('category/<slug:category_slug>/',
         views.category_posts, name='category_posts'
         ),

    path('accounts/profile/', views.self_profile_view, name="my_profile"),
    path('rofile/', views.self_profile_view, name="profile"),
    path('profile/<slug:username>/', views.user_profile, name='profile'),
    path('posts/create/', views.index, name='create_post'), # views.create_post # todo: implement view function
    path(
        'profile_edit/',
        lambda req: views.ProfileUpdateView.as_view()(req, req.user.id)
        if req.user.is_authenticated
        else views.self_profile_view(req),
        name='edit_profile'
    ),

]
