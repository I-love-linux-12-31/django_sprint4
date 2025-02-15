from django.shortcuts import render

def csrf_failure_view(request, *args, **kwargs):
    template = 'pages/403csrf.html'
    # print("403 CSRF error! Got : ", args, kwargs)
    # >> 403 CSRF error! Got :  () {'reason': 'CSRF token missing or incorrect.'}
    return render(request, template, status=403)


def raise_500_error(request):
    assert False, "Managed server error."


