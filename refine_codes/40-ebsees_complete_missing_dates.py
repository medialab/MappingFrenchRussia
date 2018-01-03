import re
# ebsees id: 95513
single_year_regex = re.compile(r'.*(?:,|\.) ?([0-9]{4})(?:, |$)')
max_year_regex = re.compile(r'[0-9]{4}')

if value is None or value == "":
  m = single_year_regex.match(cells["StdSource"]["value"])
  if m:
    return m.group(1)
  m = max_year_regex.findall(cells["StdSource"]["value"])
  max_year = max(m)
  if int(max_year) > 1980:
    return max_year
return value
