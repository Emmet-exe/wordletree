import json

cdict = {}
with open('combination_dict.json', 'r') as combo_file:
    cdict = json.loads(combo_file.read())

print(cdict["TUVXZ"])e