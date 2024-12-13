import os
from xhtml2pdf import pisa
from django.db import models
from datetime import datetime
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template.loader import get_template

from fms.settings import BASE_DIR


def redirect_homepage(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("accounts:homepage")
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if (
                request.user.profile.role in allowed_roles
                or request.user.is_staff
                or request.user.is_superuser
            ):
                return view_func(request, *args, **kwargs)
            return redirect("accounts:home")

        return wrapper_func

    return decorator


def render_file_else_response(template_path, context={}, output_as_file=True):
    file = str(datetime.now().strftime("%m%S%f")) + '.pdf'
    file_path = os.path.join(BASE_DIR, 'media', 'temp', file)
    template = get_template(template_path)
    html = template.render(context)
    if output_as_file:
        temp_file = open(file_path, "w+b")
        pisa_status = pisa.CreatePDF(html, dest=temp_file, link_callback=get_absolute_path)
        temp_file.close()
        if pisa_status.err:
            return False, file_path
        return True, file_path
    else:
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{file}"'
        pisa_status = pisa.CreatePDF(
            html, dest=response, link_callback=get_absolute_path)
        if pisa_status.err:
            return False, response
        return True, response


def get_absolute_path(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those resources
    """
    sUrl = settings.STATIC_URL
    if settings.DEBUG:
        sRoot = settings.STATICFILES_DIRS[0]
    else:
        sRoot = settings.STATIC_ROOT
    mUrl = settings.MEDIA_URL
    mRoot = settings.MEDIA_ROOT
    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
    else:
        return uri
    if not os.path.isfile(path):
        raise Exception('media URI must start with %s or %s' % (sUrl, mUrl))
    return path


class ActiveManager(models.Manager):
    def get_queryset(self):
        return (
            super(ActiveManager, self)
            .get_queryset()
            .filter(is_Active=True, deleted=False)
        )


class InactiveManager(models.Manager):
    def get_queryset(self):
        return (
            super(InactiveManager, self)
            .get_queryset()
            .filter(is_Active=False, deleted=False)
        )


class ActiveDeleteManager(models.Manager):
    def get_queryset(self):
        return (
            super(ActiveManager, self)
            .get_queryset()
            .filter(is_Active=True, deleted=True)
        )


class InactiveDeleteManager(models.Manager):
    def get_queryset(self):
        return (
            super(InactiveManager, self)
            .get_queryset()
            .filter(is_Active=False, deleted=True)
        )


# eof
