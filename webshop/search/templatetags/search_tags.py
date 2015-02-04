# -*- coding: utf-8 -*-
#!/usr/bin/env python
import urllib

from django import template
from webshop.settings import ADMIN_EMAIL

from webshop.search.forms import SearchForm
from webshop.catalog.forms import MainForm

from django.core.mail import send_mail


register = template.Library()


@register.inclusion_tag("tags/search_box.html")
def search_box(request):
    """Вставка для отображения формы поиска"""
    query = request.GET.get('query','')
    form = SearchForm({'query': query })
    return {'form': form }

@register.inclusion_tag("tags/main_form.html")
def main_form(request):
    """Вставка для отображения формы поиска"""
    # query = request.GET.get('query','')
    form = MainForm()
    if request.method == 'POST':
        form = MainForm(request.POST)
        if form.is_valid():
            subject = u'лучремонт.рф Заявка от %s' % request.POST['name']
            message = u'Имя: %s \n телефон: %s ' % (request.POST['name'], request.POST['phone'])
            send_mail(subject, message, 'teamer777@gmail.com', [ADMIN_EMAIL], fail_silently=False)

    return {'form': form }

@register.inclusion_tag('tags/pagination_links.html')
def pagination_links(request, paginator):
    """Вставка для постраничного вывода"""
    raw_params = request.GET.copy()
    page = raw_params.get('page', 1)
    p = paginator.page(page)
    try:
        del raw_params['page']
    except KeyError:
        pass
    params = urllib.urlencode(raw_params)
    return {'request': request,
            'paginator': paginator,
            'p': p,
            'params': params }
