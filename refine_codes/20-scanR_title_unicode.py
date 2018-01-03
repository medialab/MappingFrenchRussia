import re
if '<U+' not in value:
  return value
else:
  tab = re.split(r'<U\+(.+?)>', value)
  for i in range(len(tab)):
    if len(tab[i]) == 4:
      tab[i] = unichr(int(tab[i], base=16))
  return ''.join(tab)