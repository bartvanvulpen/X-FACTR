from IPython.core.display import json
from qwikidata.linked_data_interface import get_entity_dict_from_api
import pickle
import os

def write_aliases(item):
    labels = []
    for lang in ['en', 'nl', 'hu']:

        if lang in item['aliases'].keys():
            aliases = item['aliases'][lang]
            alias_f = open(f"own_alias/{lang}.txt", "a", encoding='utf-8')
            alias_f.write(item['id'] + " ")
            for alias in aliases:
                alias_f.write(alias["value"])
                alias_f.write("    ")

            alias_f.write("\n")
            alias_f.close()

        if lang in item['labels'].keys():
            labels.append( f"\t{item['labels'][lang]['value']}@{lang}")
    uni_f = open("own_unicode_escape.txt", "a", encoding='utf-8')
    uni_f.write(f"{item['id']}\t{''.join(labels)}\n")
    uni_f.close()



        
multi_f = open(f"own_multi_rel.txt", "w", encoding='utf-8')
multi_f.write("")
multi_f.close()

uni_f = open(f"own_unicode_escape.txt", "w", encoding='utf-8')
uni_f.write("")
uni_f.close()

entity_ids = set()
with open("jsondict.p", 'rb') as f:
    jsondict = pickle.load(f)

    for lang in jsondict.keys():
        if lang != 'hu':
            alias_f = open(f"own_alias/{lang}.txt", "w", encoding='utf-8')
            alias_f.write("")
            alias_f.close()

            for predicate_id in jsondict[lang].keys():
            
                item = get_entity_dict_from_api(predicate_id)
                pred_label = item['labels'][lang]['value']

                c = 0

                multi_f = open(f"own_facts_{lang}/{predicate_id}.jsonl", "w", encoding='utf-8')
                multi_f.write("")
                multi_f.close()

                for identity in jsondict[lang][predicate_id]:

                    for result in identity["results"]["bindings"]:

                        item = result["item"]["value"].split("/")[-1]
                        item = get_entity_dict_from_api(item)

                        sub_uri = item["id"]
                        if lang in item["labels"].keys():
                            sub_label = item["labels"][lang]["value"]
                        else:
                            sub_label = item["labels"][list(item["labels"].keys())[0]]["value"]
                        objs = [i['mainsnak']['datavalue']['value']['id'] for i in item['claims'][predicate_id] if 'datavalue' in i['mainsnak'].keys()]

                        for obj_id in objs:
                            if obj_id not in entity_ids:
                                entity_ids.add(obj_id)
                                obj_dict = get_entity_dict_from_api(obj_id)

                                write_aliases(obj_dict)

                        multi_f = open(f"own_multi_rel.txt", "a", encoding='utf-8')
                        multi_f.write(
                            f"{sub_uri}\t{predicate_id}\t{' '.join(objs)}\n")
                        multi_f.close()

                        obj_dict = get_entity_dict_from_api(objs[0])

                        if lang in obj_dict["labels"].keys():
                            obj_label = obj_dict["labels"][lang]["value"]
                        else:
                            obj_label = obj_dict["labels"][list(obj_dict["labels"].keys())[0]]["value"]
                        



                        F_f = open(f"own_facts_{lang}/{predicate_id}.jsonl", "a", encoding='utf-8')

                        F_f.write(
                            "{" + f'"uuid": "{predicate_id}_{c}", "predicate_id": "{predicate_id}", "sub_uri": "{sub_uri}", "sub_label": "{sub_label}", "obj_uri": "{objs[0]}", "obj_label": "{obj_label}"' + "}\n")

                        F_f.close()

                        write_aliases(item)

                        c+=1

esc = {}
with open('own_unicode_escape.txt', 'r') as f:
    for line in f:
        ls = line.split()
        esc[int(ls[0][1:])]=line

with open('own_unicode_escape2.txt', 'w') as f:
    lines = [esc[i] for i in sorted(esc.keys())]
    f.writelines(lines)
