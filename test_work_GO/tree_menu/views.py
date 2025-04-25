from django.shortcuts import render
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'tree_menu/base.html'


def page_view(request, page_path):
    """Представление для отображения произвольных страниц"""
    return render(request, 'tree_menu/page.html', {
        'page_path': page_path
    })
