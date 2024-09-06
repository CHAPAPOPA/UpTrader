from django import template

from menu.models import MenuItem

register = template.Library()


@register.inclusion_tag("menu/draw_menu.html", takes_context=True)
def draw_menu(context, menu_name):
    # Определяем текущий URL
    current_url = context["request"].path

    # Загружаем все элементы меню по имени меню
    menu_items = (
        MenuItem.objects.filter(menu_name=menu_name)
        .select_related("parent")
        .order_by("id")
    )

    # Строим древовидную структуру меню
    menu_tree = build_menu_tree(menu_items)

    # Определяем активный пункт меню
    active_item = find_active_item(menu_items, current_url)

    return {"menu": menu_tree, "active_item": active_item}


def build_menu_tree(menu_items):
    menu_tree = {}
    for item in menu_items:
        if item.parent_id is None:
            menu_tree[item] = []
        else:
            parent = next((i for i in menu_items if i.id == item.parent_id), None)
            if parent:
                if parent not in menu_tree:
                    menu_tree[parent] = []
                menu_tree[parent].append(item)
    return menu_tree


def find_active_item(menu_items, current_url):
    return next(
        (item for item in menu_items if item.get_absolute_url() == current_url), None
    )


def expand_menu_tree(menu_tree, active_item):
    expanded_menu = {}
    for parent, children in menu_tree.items():
        if parent == active_item or (
            active_item and parent in active_item.get_ancestors()
        ):
            expanded_menu[parent] = children
        elif not parent.parent:
            expanded_menu[parent] = []
    return expanded_menu
