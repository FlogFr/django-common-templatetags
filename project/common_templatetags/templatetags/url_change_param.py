# -*- coding: utf-8 -*-

from django import template

register = template.Library()


class UrlChangeParamNode(template.Node):
    def __init__(self, param_name, param_value):
        self._param_name = param_name
        self._param_value = template.Variable(param_value)
        self._request = template.Variable('request')

    def render(self, context):
        param_name = self._param_name
        param_value = self._param_value.resolve(context)
        request = self._request.resolve(context)

        # building new querydict
        new_querydict = request.GET.copy()
        new_querydict[param_name] = param_value

        return u'{}?{}'.format(
            request.path,
            new_querydict.urlencode(),
        )


@register.tag(name='url_change_param')
def do_url_change_param(parser, token):
    try:
        tag_name, param_name, param_value = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            u'{} tag require two arguments: <query_string_key> <query_string_param>'.format(
                token.split_contents()[0]
            )
        )

    if (param_name[0] != param_name[-1]) or param_name[0] != '"':
        raise template.TemplateSyntaxError(u'<query_string_key> should be quoted (string)')

    return UrlChangeParamNode(param_name[1:-1], param_value)
