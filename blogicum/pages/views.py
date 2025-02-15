from django.shortcuts import render
# from django.views import View
from django.views.generic import TemplateView

# def rules(request):
#     template = 'pages/rules.html'
#     return render(request, template)
#
#
# def about(request):
#     template = 'pages/about.html'
#     return render(request, template)

class RulesView(TemplateView):
    template_name = 'pages/rules.html'

class AboutView(TemplateView):
    template_name = 'pages/about.html'

class CSRFErrorView(TemplateView):
    template_name = 'pages/403csrf.html'
    status_code = 403

class NotFoundView(TemplateView):
    template_name = 'pages/404.html'
    status_code = 404

class InternalServerErrorView(TemplateView):
    template_name = 'pages/500.html'
    status_code = 500

