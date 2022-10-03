from IPython.core.display import json
from qwikidata.linked_data_interface import get_entity_dict_from_api
import pickle
import os


with open("jsondict.p", 'rb') as f:
    jsondict = pickle.load(f)

    for lang in jsondict.keys():
        alias_f = open(f"own_alias/{lang}.txt", "w")
        alias_f.write("")
        alias_f.close()

        for predicate_id in jsondict[lang].keys():

            item = get_entity_dict_from_api(predicate_id)
            obj_label = item['labels'][lang]['value']

            for identity in jsondict[lang][predicate_id]:

                for result in identity["results"]["bindings"]:

                    item = result["item"]["value"].split("/")[-1]
                    item = get_entity_dict_from_api(item)

                    sub_uri = item["id"]
                    sub_label = item["labels"][lang]["value"]\

                    F_f = open(f"own_facts_{lang}/{predicate_id}.jsonl", "a")

                    F_f.write(
                        "{" + f'"uuid": xD, "predicate_id": "{predicate_id}", "sub_uri": "{sub_uri}", "sub_label": "{sub_label}", "obj_label": "{obj_label}", "count": xD' + "}\n")

                    F_f.close()

                    try:
                        aliases = item["aliases"][lang]
                    except:
                        continue

                    alias_f = open(f"own_alias/{lang}.txt", "a")
                    alias_f.write(sub_uri + " ")
                    for alias in aliases:
                        alias_f.write(alias["value"])
                        alias_f.write("    ")

                    alias_f.write("\n")
                    alias_f.close()
