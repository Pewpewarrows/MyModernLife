from django.template import Library, Node

register = Library()

class DumpNode(Node):
    def render(self, context):
        # for v in context.dicts[7]: print vars(context.get(v))
        # import ipdb; ipdb.set_trace()
        return ''

@register.tag
def dump_context(parser, token):
    return DumpNode()
dump_context.is_safe = True
