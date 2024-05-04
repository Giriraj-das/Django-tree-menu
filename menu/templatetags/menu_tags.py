from django import template
from django.db import connection
from django.utils.html import format_html
from django.urls import reverse

from menu.models import Menu

register = template.Library()


def change_url(row_url: str) -> str:
    if not row_url:
        return ''
    url = row_url if '/' in row_url else reverse(row_url)
    return url


@register.simple_tag
def draw_menu(menu_name: str, current_url: str = None):
    rows = Menu.objects.filter(menu_name__name=menu_name)

    menu_item = None
    menu_dict = {}
    for row in rows:
        url = change_url(row.url)
        new_row = (row.id, row.title, url, row.parent_id)

        if url == current_url:
            menu_item = new_row
        menu_dict.setdefault(row.parent_id, []).append(new_row)

    if not menu_item:
        return 'Menu is not associated with the current address'

    html = '<ul>'
    for item in menu_dict.get(menu_item[3], []):
        if item == menu_item:
            html += f'<li><a id="active" href="{item[2]}">{item[1]}</a>'
            html += '<ul>'
            for sub_item in menu_dict.get(menu_item[0], []):
                html += f'<li><a href="{sub_item[2]}">{sub_item[1]}</a></li>'
            html += '</ul></li>'
        else:
            html += f'<li><a href="{item[2]}">{item[1]}</a></li>'
    html += '</ul>'

    html = recursive(rows, menu_dict, menu_item, html)

    return format_html(html)


def recursive(rows, menu_dict, menu_item, html):
    # прерывание на корневом списке меню
    if not menu_item[3]:
        return html

    parent_item = None
    for row in rows:
        if row.id == menu_item[3]:
            url = change_url(row.url)
            parent_item = (row.id, row.title, url, row.parent_id)
            break

    html_local = '<ul>'
    for item in menu_dict.get(parent_item[3], []):  # построение списка элементов меню
        html_local += f'<li><a href="{item[2]}">{item[1]}</a>'
        if item == parent_item:  # вставка предыдущего списка
            html_local += html
        html_local += '</li>'
    html_local += '</ul>'

    return recursive(rows, menu_dict, parent_item, html_local)
