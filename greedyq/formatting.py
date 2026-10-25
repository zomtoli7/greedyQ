"""Small escaped inline-markdown subset. Raw HTML is never executed."""
import html
import re


def inline(text):
    text=html.escape(str('' if text is None else text).replace('\x00','\ufffd'),quote=True).replace('&#x27;','&#39;')
    tokens=[]
    def code(match):
        tokens.append('<code>'+match.group(1)+'</code>')
        return '\x00'+str(len(tokens)-1)+'\x00'
    text=re.sub(r'`([^`\n]+)`',code,text)
    for pattern,tag in ((r'\*\*\*([^*\n]+)\*\*\*','strong><em'),(r'\*\*([^*\n]+)\*\*','strong'),(r'\*([^*\n]+)\*','em')):
        closing='em></strong' if tag=='strong><em' else tag
        text=re.sub(pattern,lambda m:'<'+tag+'>'+m.group(1)+'</'+closing+'>',text)
    return re.sub(r'\x00(\d+)\x00',lambda m:tokens[int(m.group(1))],text)
