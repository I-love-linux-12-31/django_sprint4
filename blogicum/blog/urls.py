from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('posts/<int:id>/', views.post_detail, name='post_detail'),
    path('category/<slug:category_slug>/',
         views.category_posts, name='category_posts'
         ),

    path('profile/<slug:username>/', views.user_profile, name='profile'),
    path('posts/create/', views.index, name='create_post'), # views.create_post # todo: implement view function
    path('profile_edit/', views.ProfileUpdateView.as_view(), name='edit_profile'),

]
