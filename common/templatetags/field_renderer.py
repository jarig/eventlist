from django import template
register = template.Library()

class RenderFieldNode(template.Node):
    def __init__(self, field, options):
        self.field = template.Variable(field)
        self.options = options

    def render(self, context):
        try:
            bField = self.field.resolve(context)
            att = {}
            for attr in self.options:
                splitted = attr.strip("'\"").split("=")
                att[splitted[0]] = ""
                if len(splitted) > 1: att[splitted[0]] = splitted[1]
            if bField.field.show_hidden_initial:
                return bField.as_widget(attrs=att) + bField.as_hidden(only_initial=True)
            return bField.as_widget(attrs=att)
        except template.VariableDoesNotExist:
            return ''

def field(parser, token):
    contents = token.split_contents()
    field = contents[1]
    options = contents[2:]
    return RenderFieldNode(field, options)

register.tag('field', field)
