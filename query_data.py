from qwikidata.sparql import (get_subclasses_of_item,
                              return_sparql_query_results)
from copy import deepcopy
from collections import defaultdict
import pickle
jsondict = defaultdict(dict)
for lang in ['en', 'nl', 'hu']:
    if lang == 'en':
        countries = ['Q30', 'Q145']
        limit = 100
    elif lang == 'hu':
        countries = ['Q28']
        limit = 200
    else:
        countries = ['Q55']
        limit = 200
    
    jsons = []
    for country in countries:
        jsons.append(return_sparql_query_results( f"""
        SELECT DISTINCT ?item WHERE {{
        SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE]". }}
        {{
            SELECT DISTINCT ?item WHERE {{
            ?item p:P106 ?statement0.
            ?statement0 (ps:P106/(wdt:P279*)) wd:Q1278335.
            ?item p:P27 ?statement1.
            ?statement1 (ps:P27/(wdt:P279*)) wd:{'Q29999' if country =='Q55' else country}.
            ?item p:P1303 ?statement2.
            ?statement2 (ps:P1303/(wdt:P279*)) ?in.
            }}
            LIMIT {limit}
        }}
        }}"""))
    jsondict[lang]['P1303']=deepcopy(jsons)
    jsondict[lang]['P27']=deepcopy(jsons)

    jsons = []
    for country in countries:
        jsons.append(return_sparql_query_results( f"""
        SELECT DISTINCT ?item WHERE {{
        SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE]". }}
        {{
            SELECT DISTINCT ?item WHERE {{
            ?item p:P106 ?statement0.
            ?statement0 (ps:P106/(wdt:P279*)) wd:Q2066131.
            ?item p:P27 ?statement1.
            ?statement1 (ps:P27/(wdt:P279*)) wd:{'Q29999' if country =='Q55' else country}.
            ?item p:P54 ?statement2.
            ?statement2 (ps:P54/(wdt:P279*)) ?in.
            }}
            LIMIT {limit}
        }}
        }}"""))
    jsondict[lang]['P54']=deepcopy(jsons)
    jsondict[lang]['P27'].extend(deepcopy(jsons))

    jsons = []
    for country in countries:
        jsons.append(return_sparql_query_results( f"""
        SELECT DISTINCT ?item WHERE {{
        SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE]". }}
        {{
            SELECT DISTINCT ?item WHERE {{
            ?item p:P27 ?statement1.
            ?statement1 (ps:P27/(wdt:P279*)) wd:{'Q29999' if country =='Q55' else country}.
            ?item p:P102 ?statement2.
            ?statement2 (ps:P102) ?in.
            ?in p:P17 ?statement3.
            ?statement3 (ps:P17/(wdt:P279*)) wd:{country}.
            }}
            LIMIT {limit}
        }}
    }}"""))
    jsondict[lang]['P102']=deepcopy(jsons)
    jsondict[lang]['P27'].extend(deepcopy(jsons))

    jsons = []
    for country in countries:
        jsons.append(return_sparql_query_results( f"""
        SELECT DISTINCT ?item WHERE {{
        SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
        {{
            SELECT DISTINCT ?item WHERE {{
            ?item p:P31 ?statement0.
            ?statement0 (ps:P31/(wdt:P279*)) wd:Q15416.
            ?item p:P495 ?statement1.
            ?statement1 (ps:P495/(wdt:P279*)) wd:{country}.
            ?item p:P449 ?statement2.
            ?statement2 (ps:P449/(wdt:P279*)) ?in.
            ?item rdfs:label ?item_label filter (lang(?item_label) = "en" || lang(?item_label) = "nl" || lang(?item_label) = "hu") 
            }}
            LIMIT {limit}
        }}
        }}
        """))
    jsondict[lang]['P449']=deepcopy(jsons)
    jsondict[lang]['P495']=deepcopy(jsons)

    jsons = []
    for country in countries:
        jsons.append(return_sparql_query_results( f"""
        SELECT DISTINCT ?item ?itemLabel WHERE {{
        SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". 
                                ?in rdfs:label ?inLabel.
                                ?item rdfs:label ?itemLabel }}
        {{
            SELECT DISTINCT ?item WHERE {{
            ?item p:P31 ?statement0.
            ?statement0 (ps:P31/(wdt:P279*)) wd:Q4830453.
            ?item p:P17 ?statement1.
            ?statement1 (ps:P17/(wdt:P279*)) wd:{country}.
            ?item p:P159 ?statement2.
            ?statement2 (ps:P159) ?in.
            ?item p:P571 ?statement_3.
            ?statement_3 psv:P571 ?statementValue_3.
            ?statementValue_3 wikibase:timePrecision ?precision_3.
            hint:Prior hint:rangeSafe "true"^^xsd:boolean.
            FILTER(?precision_3 >= 9 )
            ?statementValue_3 wikibase:timeValue ?P571_3.
            hint:Prior hint:rangeSafe "true"^^xsd:boolean.
            MINUS {{
                ?item p:P576 ?statement_4.
                ?statement_4 psv:P576 ?statementValue_4.
                ?statementValue_4 wikibase:timeValue ?P576_4.
            }}
            }}
            LIMIT {limit}
        }}
        }} """))
    jsondict[lang]['P159']=deepcopy(jsons)
    jsondict[lang]['P17']=deepcopy(jsons)

pickle.dump(jsondict, open("jsondict.p", "wb"))