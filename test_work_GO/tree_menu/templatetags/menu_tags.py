from django import template
from django.urls import resolve
from django.http import HttpRequest
from tree_menu.models import Menu, MenuItem

register = template.Library()


@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    request = context.get('request')
    if not request:
        return ''
    
    # Получаем текущий URL
    current_url = request.path
    
    # Получаем все пункты указанного меню за один запрос
    menu_items = MenuItem.objects.filter(menu__name=menu_name).select_related('menu')
    
    # Создаем словарь с древовидной структурой меню
    menu_dict = {}
    active_item_id = None
    
    # Формируем словарь из всех пунктов меню
    for item in menu_items:
        item_url = item.get_url()
        is_active = current_url == item_url
        
        menu_dict[item.id] = {
            'id': item.id,
            'name': item.name,
            'url': item_url,
            'parent_id': item.parent_id,
            'is_active': is_active,
            'children': [],
        }
        
        # Запоминаем активный пункт меню
        if is_active:
            active_item_id = item.id
    
    # Если активный пункт не найден, проверяем частичное совпадение URL
    if not active_item_id:
        for item_id, item_data in menu_dict.items():
            if current_url.startswith(item_data['url']) and item_data['url'] != '#':
                menu_dict[item_id]['is_active'] = True
                active_item_id = item_id
                break
    
    # Формируем дерево
    menu_tree = []
    parents_of_active_item = get_parents_ids(active_item_id, menu_dict)
    
    for item_id, item_data in menu_dict.items():
        parent_id = item_data['parent_id']
        
        # Если это корневой элемент (без родителя)
        if parent_id is None:
            menu_tree.append(item_data)
        # Иначе добавляем элемент в список детей родительского элемента
        elif parent_id in menu_dict:
            menu_dict[parent_id]['children'].append(item_data)
    
    # Определяем, какие элементы нужно развернуть
    for item_id, item_data in menu_dict.items():
        item_data['expanded'] = (
            # Все, что над выделенным пунктом
            item_id in parents_of_active_item or
            # Первый уровень вложенности под выделенным пунктом
            item_data['parent_id'] == active_item_id or
            # Элементы первого уровня всегда видимы
            item_data['parent_id'] is None
        )
    
    # Рендерим дерево меню
    html = render_menu_tree(menu_tree)
    return html


def get_parents_ids(item_id, menu_dict):
    """Получить список ID всех родительских пунктов для заданного пункта"""
    result = []
    current_id = item_id
    
    while current_id:
        item = menu_dict.get(current_id)
        if not item:
            break
        
        parent_id = item['parent_id']
        if parent_id is not None:
            result.append(parent_id)
            current_id = parent_id
        else:
            break
    
    return result


def render_menu_tree(items):
    """Рекурсивно рендерит дерево меню в HTML"""
    if not items:
        return ''
    
    html = '<ul>'
    for item in items:
        active_class = ' class="active"' if item['is_active'] else ''
        expanded = item['expanded']
        
        html += f'<li{active_class}>'
        html += f'<a href="{item["url"]}">{item["name"]}</a>'
        
        if item['children'] and expanded:
            html += render_menu_tree(item['children'])
        
        html += '</li>'
    html += '</ul>'
    
    return html 