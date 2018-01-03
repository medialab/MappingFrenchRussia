import re

bnf_regex = re.compile(r'(.*?)(?:\. auteur du texte,?)?$')
tab = []
for author in value.split(' // '):
    m = bnf_regex.match(author)
    if m:
        tab.append(m.group(1))
return value if tab == [] else ' // '.join(tab)