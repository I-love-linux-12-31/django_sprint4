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
    path('profile/', views.self_profile_view, name="profile"),
    path('profile/<slug:username>/', views.user_profile, name='profile'),
    path('posts/create/', views.update_post, name='create_post'),
    path('posts/<int:pk>/edit/', views.update_post, name='edit_post'),
    path('posts/<int:pk>/delete/', views.delete_post, name='delete_post'),
    path(
        'profile_edit/',
        lambda req: views.ProfileUpdateView.as_view()(req, req.user.id)
        if req.user.is_authenticated
        else views.self_profile_view(req),
        name='edit_profile'
    ),

    path('posts/<int:post_id>/edit_comment/<int:comment_id>/', views.index, name='edit_comment'), # todo views.edit_comment
    path('posts/<int:post_id>/comment', views.add_comment, name='add_comment'),
    path('posts/<int:post_id>/delete_comment/<int:comment_id>/', views.index, name='delete_comment'), # todo views.delete_comment

]
