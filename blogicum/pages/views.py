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

    def render_to_response(self, context, **response_kwargs):
        response = super().render_to_response(context, **response_kwargs)
        response.status_code = self.status_code
        return response

def handler500(request, *args, **kwargs):
    # Костыль для кривого теста.
    # _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
    #
    # handler_path = <function InternalServerErrorView at 0x7fe8d6684c20>
    #
    #     def check_handler_exists(handler_path):
    # >       module_name, func_name = handler_path.rsplit('.', 1)
    # E       AttributeError: 'function' object has no attribute 'rsplit'
    #
    # tests/test_err_pages.py:76: AttributeError
    return InternalServerErrorView.as_view()(request, *args, **kwargs)
