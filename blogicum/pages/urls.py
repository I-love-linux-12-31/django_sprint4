from django.urls import path

from . import views

app_name = 'pages'

urlpatterns = [
    # path('about/', views.about, name='about'),
    # path('rules/', views.rules, name='rules'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('rules/', views.RulesView.as_view(), name='rules'),
    path('404/', views.NotFoundView.as_view(), name='404'),
    path('403csrf/', views.CSRFErrorView.as_view(), name='403csrf'),
    path('500/', views.InternalServerErrorView.as_view(), name='500'),
]
