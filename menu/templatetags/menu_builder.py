from django import template
from menu.models import Menu

register = template.Library()

@register.inclusion_tag('menu/subMenu.html')
def subMenu(menuItems):
    return {"menuItems": menuItems }




def sidemenu(parser, token):
    tag_name = token.split_contents()
    return MenuNode()


class MenuNode(template.Node):
    def __init__(self):
        pass

    def render(self, context):
        context['menuItems'] = Menu(context).sideMenu()
        return ''

register.tag("sidemenu",sidemenu)
