#!/usr/bin/env python

'''for css values: http://www.westciv.com/style_master/academy/css_tutorial/properties/values.html

- length: number unit
- percentage: number%
- color: #FFF #abcdef green rgb(0, 255, 50%) rgba(0, 0, 0, 50%)
- url: url(...)
- keyword: bold bolder
- shape: rect( 0px 10px auto 2em )

'''

from css.tokens import *
from codetalker.pgm.special import commas, no_ignore, _or, star, _not

def value(rule):
    from css.grammar import cssid
    rule | COLOR | HEXCOLOR | percentage | length | uri | rgb | rgba | cssid | ',' | STRING | SSTRING
    rule.pass_single = True

def length(rule):
    rule | (['-'], NUMBER, [UNIT])
    rule.astAttrs = {'neg':SYMBOL, 'value':NUMBER, 'unit':UNIT}

def percentage(rule):
    rule | (['-'], no_ignore(NUMBER, '%'))
    rule.astAttrs = {'neg':SYMBOL, 'value':NUMBER}

def uri(rule):
    rule | ('url', '(', _or(STRING, SSTRING, uri_contents), ')')
    rule.astAttrs = {
        'uri':{'type':[STRING, SSTRING, uri_contents], 'single':True}
    }

def uri_contents(rule):
    rule | star(_not(')'))
    rule.dont_ignore = True
    rule.astAttrs = {
        'items':the_tokens,
        }

def rgb(rule):
    rule | ('rgb', '(', ((_or(percentage, NUMBER), ',')*3)[:-1], ')')
    rule.astAttrs = {
            'red':{'type':[percentage, NUMBER],
                   'single':True,
                   'start':0},
            'green':{'type':[percentage, NUMBER],
                   'single':True,
                   'start':1},
            'blue':{'type':[percentage, NUMBER],
                   'single':True,
                   'start':2},
            }

def rgba(rule):
    rule | ('rgba', '(', ((_or(percentage, NUMBER), ',')*4)[:-1], ')')
    rule.astAttrs = {
            'red':{'type':[percentage, NUMBER],
                   'single':True,
                   'start':0},
            'green':{'type':[percentage, NUMBER],
                   'single':True,
                   'start':1},
            'blue':{'type':[percentage, NUMBER],
                   'single':True,
                   'start':2},
            'alpha':{'type':[percentage, NUMBER],
                   'single':True,
                   'start':3},
            }

# vim: et sw=4 sts=4
