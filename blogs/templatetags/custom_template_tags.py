import re

import readtime
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.html import strip_tags

register = template.Library()


def calc_read_time(article):
    return readtime.of_html(article)


@stringfilter
def split_string_get_index_0(value, delimiter=None):
    return value.split(delimiter)[0]


split_string_get_index_0.is_safe = True


def parse_text(text, patterns=None):
    """
    delete all HTML tags and entities
    :param text : (str)given text
    :param patterns : (dict)patterns for re.sub
    :return str: final text

    usage like:
    parse_text('<div class="super"><p>Hello&ldquo;&rdquo;!&nbsp;&nbsp;</p>&lsquo;</div>')

    """
    base_patterns = {
        '&[rl]dquo;': '',
        '&[rl]squo;': '',
        '&nbsp;': ''
    }

    patterns = patterns or base_patterns

    final_text = strip_tags(text)
    for pattern, repl in patterns.items():
        final_text = re.sub(pattern, repl, final_text)
    return final_text


def article_styles(body):
    styled = body.replace(
        '<p>', '<p class="mt-4 mb-4">').replace(
        '<img', '<img class="img-fluid" style="width:100%;height:auto;"').replace(
        '<table', '<table class="table table-bordered border-dark"'
    )
    return styled


register.filter('readtime', calc_read_time)
register.filter('show_till', split_string_get_index_0)
register.filter('format_text', parse_text)
register.filter('style_article', article_styles)
