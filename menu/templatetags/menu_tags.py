from django import template
from django.db import connection
from django.utils.html import format_html
from django.urls import reverse

register = template.Library()


def db_connect(menu_name: str) -> list:
    with connection.cursor() as cursor:
        cursor.execute("""
            WITH RECURSIVE menu_tree AS (
                SELECT id, title, url, parent_id
                FROM menu_menu
                WHERE title = %s
                UNION ALL
                SELECT m.id, m.title, m.url, m.parent_id
                FROM menu_menu m
                JOIN menu_tree mt ON m.parent_id = mt.id
            )
            SELECT id, title, url, parent_id
            FROM menu_tree;
        """, [menu_name])
        rows = cursor.fetchall()
        return rows


def change_url(row_url: str) -> str:
    if not row_url:
        return ''
    url = row_url if '/' in row_url else reverse(row_url)
    return url


@register.simple_tag
def draw_menu(menu_name: str, current_url: str = None):
    rows = db_connect(menu_name)

    menu_item = None
    menu_dict = {}
    for row in rows:
        url = change_url(row[2])
        new_row = (row[0], row[1], url, row[3])

        if url == current_url:
            menu_item = new_row
        menu_dict.setdefault(row[3], []).append(new_row)

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
    parent_item = None
    for row in rows:
        if row[0] == menu_item[3]:
            url = change_url(row[2])
            parent_item = (row[0], row[1], url, row[3])
            break

    # прерывание на корневом списке меню
    if not parent_item[3]:
        return html

    html_local = '<ul>'
    for item in menu_dict.get(parent_item[3], []):  # построение списка элементов меню
        html_local += f'<li><a href="{item[2]}">{item[1]}</a>'
        if item == parent_item:  # вставка предыдущего списка
            html_local += html
        html_local += '</li>'
    html_local += '</ul>'

    return recursive(rows, menu_dict, parent_item, html_local)
