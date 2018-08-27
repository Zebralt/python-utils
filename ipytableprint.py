from IPython.display import HTML, display as hdisplay

class Obj:
    pass

def display(*x):
    hdisplay(HTML(''.join(x)))
    
def html_tag(content, tag='div', attributes={}, _style={}):
    if 'style' not in attributes and _style:
        if not attributes:
            attributes = {}
        attributes['style'] = ' '.join(('{}:{};'.format(a, b) for a, b in _style.items()))
    ans = '<{1}{2}>{0}</{1}>'.format(content, tag, ' ' * (not not attributes) +  ' '.join(['{}="{}"'.format(x, y) for x, y in attributes.items()]))
    #print(ans)
    return ans

global_style = {'font-family' : 'Inconsolata', 'font-size' : '14px', 'font-weight' : 'normal'}
line_style = {'border' : '1px solid black', 'background-color' : '#FDFDFD'}
col_style = {'border' : '1px solid gray', 'text-align' : 'left'}
header_style = {'font-weight' : 'bold', 'border' : '1px solid gray', 'text-align' : 'left', 'background-color': '#ADF'}
title_style = {'font-size': '24px', 'font-weight' : 'normal', 'margin' : '0', 'padding' : 0}
table_style = {'margin' : 0, 'padding' : 0, 'margin': '10px auto'}
div_style = {'display': 'inline-block', 'margin' : '10px 2px 0 auto'}
highlight_style = {'font-weight' : 'bold', 'color' : 'green'}

styles = Obj()
styles.body = global_style
styles.row = line_style
styles.col = col_style
styles.header = header_style
styles.title = title_style
styles.table = table_style
styles.div = div_style
styles.highlight = highlight_style

def print_table(tuples, 
                 headers=[], 
                 headerUpper=False,
                 title=None,
                 colsize=[],
                 ellipsis=True, 
                 align=-1,
                 inline=False,
                diff=None,
                diffstyle=highlight_style,
                enableAddition=False):
    
    output = ''
    
    if len(colsize) < len(headers):
        colsize += (len(headers) - len(colsize)) * [10 * align] # [10 if not colsize else colsize[-1]]
    
    if headerUpper:
        headers = list(map(str.upper, headers))
    # print header
    
    if headers:
        header_div = map(lambda x : html_tag(x, tag='div', _style={**global_style}), headers)
        header_th = map(lambda x : html_tag(x, tag='th', _style=header_style), header_div)
        output += html_tag(''.join(header_th), tag='tr', _style={**line_style})
    
    
    if not diff:
        for t in tuples:
            output += html_tag(' '.join(map(lambda x : html_tag(x, tag='td', _style={**col_style, **global_style}), t)), tag='tr', _style=line_style)
    elif diff:# and len(diff) == len(tuples) and len(tuples[0]) == len(diff[0]):
        for t, u in zip(tuples, diff):
            elems = []
            for v, w in zip(t, u):
                if v != w:
                    elems.append(html_tag(v, _style={**diffstyle}))
                else:
                    elems.append(v)
            output += html_tag(' '.join(map(lambda x : html_tag(x, tag='td', _style={**col_style, **global_style}), elems)), tag='tr', _style=line_style)
    
    if title:
        result = html_tag(title, 'h4', _style=title_style) + html_tag(output, tag='table', _style=table_style)
        result = html_tag(result, tag='div', _style={**div_style})
    else:
        result = html_tag(output, tag='table', _style=table_style)
    if not enableAddition:
        display(result)
    else:
        return result