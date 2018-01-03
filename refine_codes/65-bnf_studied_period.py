################## START HERE ###################

import re

title_regex = re.compile(r'.*?([0-9]{3,4}\??\s?-\s?[0-9]{3,4}).*')
subject_regex = re.compile(r'.*?([0-9]{3,4}\??\s?-\s?[0-9\.]{3,4}).*')
#title_regex_2 = re.compile('.*?([0-9]{3,4}).*?(nos jours)?')
title_regex_2 = re.compile('.*?([0-9]{3,4})(?:.*?(nos jours))?')



if cells["BNF_Ark"]["value"] is not None:
  m = title_regex.match(value)
  if m:
    return m.group(1)

  m = title_regex_2.match(value) # for later use
  title_date = m.group(1) if m is not None else None

  subject_tab = []
  try:
    subjects_tab = cells["StdMots-clés"]["value"].split(' // ')# if ("StdMots-clés" in cells and cells["StdMots-clés"]["value"]) else [] #La croche-choeur et Moskovskié et Pievtchié : France - Russie 2010 : 
  except:
    subjects_tab = []
  min_year = "2222"
  max_year = ""

  if m and m.group(2):
    return title_date+'-'+cells["StdAnnée"]["value"]
  max_year = title_date if title_date is not None else "0000"
  any_change = title_date is not None

  for subject in subjects_tab:
    for element in subject.split('--'):
       if '-' in element: # two dates !!
        m2 = subject_regex.match(element)
        if m2:
          any_change = True
          first_date = m2.group(1).split('-')[0]
          second_date = m2.group(1).split('-')[1]

          if second_date == "...." or int(second_date) > int(max_year):# or m2.group(2):
            max_year = cells["StdAnnée"]["value"] if second_date == "...." else second_date
          if int(first_date) < int(min_year):
            min_year = first_date

  min_year = title_date if title_date is not None else min_year # force
  return (min_year + '-' + max_year) if any_change else None

import re

thesis_regex_onepoint = re.compile('([0-9]{4})-$')
thesis_regex_year = re.compile(r'([0-9]{3,4})\s?-\.?\s?([0-9]{4})')
thesis_regex_century = re.compile('([0-9]{2})-([0-9]{2})')
thesis_regex_singleyear = re.compile('([0-9]{4})$')

if cells["Theses_time studied"]["value"] is not None and (value is None or value == ""):
  start_year = "2222"
  end_year = "0000"
  for date in cells["Theses_time studied"]["value"].split('***'):
    m = thesis_regex_onepoint.match(date)
    if m:
      start_year = min([start_year, m.group(1)])
      end_year = cells["StdAnnée"]["value"]
    else:
      m = thesis_regex_year.match(date)
      if m:
        start_year = min([start_year, m.group(1) if len(m.group(1)) >= 4 else '0'+m.group(1)])
        end_year = max([end_year, m.group(2)])
      else:
          m = thesis_regex_century.match(date)
          if m:
            start_year = min([start_year, str(int(m.group(1))-1)+'00'])
            end_year = max([end_year, min([str(int(m.group(2))-1)+'99', cells["StdAnnée"]["value"]])])
          else:
            m = thesis_regex_singleyear.match(date)
            if m:
              start_year = min([start_year, m.group(1)])
              end_year = max([end_year, m.group(1)])
  return start_year+'-'+end_year if start_year != "2222" and end_year else 'BLI !'

##################################### 171 cells

import re

century_regex = re.compile(r'.*?([0-9]{2})(?:e siècle| s\.)')
#partial_regex = re.compile(r''
if cells["BNF_Ark"]["value"] is not None and (value is None or value == ""):

  subject_tab = []
  try:
    subjects_tab = cells["StdMots-clés"]["value"].split(' // ')# if ("StdMots-clés" in cells and cells["StdMots-clés"]["value"]) else [] #La croche-choeur et Moskovskié et Pievtchié : France - Russie 2010 : 
  except:
    subjects_tab = []
  min_cent = "20"
  max_cent = "00"
  cent = ""
  for subject in subjects_tab:
    for element in subject.split('--'):
      m = century_regex.match(element)
      if m:
        cent = str(int(m.group(1))-1)
        if min_cent > cent:
          min_cent = cent
        if max_cent < cent:
          max_cent = cent
  if min_cent <= max_cent:
    max_year = max_cent+'99' if max_cent+'99' < cells["StdAnnée"]["value"] else cells["StdAnnée"]["value"]
    return min_cent+'00-' + max_year
return value

######################## 19 cells :: 26
# Trains : voyages en chemin de fer au 19e siècle : exposition,
# a checker

import re

partial_regex = re.compile(r'.*?([0-9]{3,4})-')
if cells["BNF_Ark"]["value"] is not None and (value is None or value == ""):

  subject_tab = []
  try:
    subjects_tab = cells["StdMots-clés"]["value"].split(' // ')# if ("StdMots-clés" in cells and cells["StdMots-clés"]["value"]) else [] #La croche-choeur et Moskovskié et Pievtchié : France - Russie 2010 : 
  except:
    subjects_tab = []
  min_year = "2222"
  for subject in subjects_tab:
    for element in subject.split('--'):
      m = partial_regex.match(element)
      if m:
        if min_year > m.group(1):
          min_year = m.group(1)
  if min_year != "2222":
    return min_year + '-' + cells["StdAnnée"]["value"]
return value


############################ 3 cells

import re

partial_regex_v2 = re.compile(r'.*?([0-9]{2}[\.]{2}\s?-\s?[0-9]{3,4}).*')

if cells["BNF_Ark"]["value"] is not None and (value is None or value == ""):

  subject_tab = []
  try:
    subjects_tab = cells["StdMots-clés"]["value"].split(' // ')# if ("StdMots-clés" in cells and cells["StdMots-clés"]["value"]) else [] #La croche-choeur et Moskovskié et Pievtchié : France - Russie 2010 : 
  except:
    subjects_tab = []
  min_year = "2222"
  max_year = "0000"

  for subject in subjects_tab:
    for element in subject.split('--'):
      m = partial_regex_v2.match(element)
      if m:
        start_date = m.group(1).split('-')[0].strip()[0:2]+'00'
        end_date = m.group(1).split('-')[1].strip()
        if min_year > start_date:
          min_year = start_date
        if max_year < end_date:
          max_year = end_date

  if min_year != "2222":
    return min_year + '-' + max_year
return value

############################### 52 cells

import re

single_year_regex = re.compile(r'.*?([0-9]{3,4}).*')

if cells["BNF_Ark"]["value"] is not None and (value is None or value == ""):

  subject_tab = []
  try:
    subjects_tab = cells["StdMots-clés"]["value"].split(' // ')# if ("StdMots-clés" in cells and cells["StdMots-clés"]["value"]) else [] #La croche-choeur et Moskovskié et Pievtchié : France - Russie 2010 : 
  except:
    subjects_tab = []
  year = ""

  for subject in subjects_tab:
    for element in subject.split('--'):
      m = single_year_regex.match(element)
      if m:
        year = m.group(1)

  if year != "":
    return year + '-' + year
return value

# probleme avec:
# La hiérarchie des égaux : la noblesse russe d'Ancien régime, XVIe-XVIIe siècles
# La Grande-Duchesse Anastasia : l'histoire d'Anna Anderson
# sub: Avant 1700

# à checker: D'une perestroïka à l'autre : l'évolution économique de la Russie de 1860 à nos jours

############################## 88 cells

import re

def convert_century(century):
  letter_list = ['X', 'V', 'I']
  value_list = [10, 5, 1]
  numeric_century = 0
  old_value_index = 0
  for letter_index, letter in enumerate(century):
    current_value_index = letter_list.index(letter)
    
    # if letter is "lower" that its neighbours, substract, else add
    if current_value_index > old_value_index and\
    letter_index < len(century)-1 and\
    letter_list.index(century[letter_index+1]) < current_value_index:
      numeric_century -= value_list[current_value_index]
    else:
      numeric_century += value_list[current_value_index]
    
    old_value_index = current_value_index
  return numeric_century

letter_century_regex = re.compile(r'([XVI]+)(?:e|e?\ssiècle)(?:.*?(nos jours))?')

m = None

if cells["BNF_Ark"]["value"] is not None and (value is None or value == ""):

  m = letter_century_regex.findall(cells["StdTitre_v2"]["value"])
  min_century = 21
  max_century = 0
  max_year = False
  if m:
    for century in m:
      current_value = convert_century(century[0])
      if current_value < min_century:
        min_century = current_value
      if current_value > max_century and not max_year:
        if century[1] != '':
          max_year = cells["StdAnnée"]["value"]
        else:
          max_century = current_value
  min_year = str(min_century-1)+'00'
  max_year = str(max_century-1)+'99' if not max_year else max_year
#  if 'à nos jours'.encode('utf-8') in cells["StdTitre_v2"]["value"]:
#    max_year = str(cells["StdMots-clés"]["value"])

return min_year+'-'+max_year if m else value
