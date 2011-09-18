import re
from django import template
from django.core.urlresolvers import reverse, resolve
from django.db import models


class Menu:

    def __init__(self, context):
        self.context= context
        self.items = []
        self.current_path = template.resolve_variable('request.path', self.context)
        self.user = template.resolve_variable('request.user', self.context)

    def addItem(self, label, view='', show=True, enabled=True):
        item = MenuItem(label, view, show, enabled)
        self.items.append(item)

    def getMenu(self):
        for item in self.items:
            match = resolve(self.current_path)
            if re.match(match.url_name, item.view):
                item.selected = True
            else:
                item.selected = False
        return self.items

    #TODO Remove
    def sideMenu(self):
        return [
                {
                    "title":"Friends",
                    "url": '', #reverse("accounts.views.friends"),
                    "active": False,
                    "enabled": self.user.is_authenticated()
                },
                {
                    "title":"Messages",
                    "url": '', #reverse("accounts.views.friends"),
                    "active": False,
                    "enabled": self.user.is_authenticated()
                }
            ]

class MenuItem:
    def __init__(self,label, view='', show=True, enabled=True):
        self.label = label
        self.url = reverse(view)
        self.view = view
        self.show = show
        self.enabled = enabled
        self.selected = False