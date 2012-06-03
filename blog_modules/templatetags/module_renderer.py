from django import template
from django.template.base import VariableDoesNotExist
from rest.blog_modules.settings import INSTALLED_MODULES
register = template.Library()

class RenderBlogModule(template.Node):
    def __init__(self, map, position):
        self.map = template.Variable(map)
        self.position = template.Variable(position)

    def render(self, context):
        module = None
        try:
            self.map = self.map.resolve(context)
            self.position = self.position.resolve(context)
            if self.map.has_key(self.position):
                if INSTALLED_MODULES.has_key(self.map[self.position]):
                    module = INSTALLED_MODULES[self.map[self.position]]
            if module:
                return module.content(context)
            else:
                return ''
        except VariableDoesNotExist:
            return ''


def blogModule(parser, token):
    contents = token.split_contents()
    map = contents[1]
    position = contents[2]
    return RenderBlogModule(map, position)

register.tag('blogModule', blogModule)