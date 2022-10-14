import pandas as pd
import json
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.max_colwidth', 1000)
pd.set_option('display.width', 1000)

def bold_extreme_values(data, format_string="%.2f\%%"):
    extrema = data != data.max()
    bolded = data.apply(lambda x : "\\textbf{%s}" % format_string % x)
    formatted = data.apply(lambda x : format_string % x)
    return formatted.where(extrema, bolded)

def format_values(data, format_string="%.3f\%%"):
    formatted = data.apply(lambda x : format_string % x)
    return formatted

def df_to_latex(dataframe, bold):
    dataframe = dataframe.multiply(100)
    if bold:
        dataframe = dataframe.apply(lambda data : bold_extreme_values(data))
    else:
        dataframe = dataframe.apply(lambda data : format_values(data))
    print(dataframe.to_latex(escape=False))


#load data
results_single = pd.read_csv('results_df.csv',index_col=['model lang', 'fact lang', 'model', 'init method', 'iter method'])
results_acc = pd.read_csv('results_df_multi_accuracy.csv',index_col=['model lang', 'fact lang', 'model', 'init method', 'iter method'])
results_prec = pd.read_csv('results_df_multi_precision.csv',index_col=['model lang', 'fact lang', 'model', 'init method', 'iter method'])

#get best paremeters
best_iter = results_single['overall'].groupby('iter method').sum().sort_values(ascending=False)
best_init = results_single['overall'].groupby('init method').sum().sort_values(ascending=False)
best_model = results_single['overall'].groupby('model').sum().sort_values(ascending=False)
# print('BEST PARAMS:\n',best_iter,'\n',best_init,'\n',best_model)
idx = pd.IndexSlice
best_results_single = results_single.loc[idx[:,:,best_model.index[0],best_init.index[0],best_iter.index[0]], :]

#print dataframes in a latex format
# df_to_latex(best_results_single.reset_index(level=['model','init method', 'iter method'],drop=True),bold=True)
# df_to_latex(results_acc.reset_index(level=['model','init method', 'iter method'],drop=True),bold=True)
# df_to_latex(results_prec.reset_index(level=['model','init method', 'iter method'],drop=True),bold=True)

#ranking of probe and fact langs
# print(results_single['overall'].groupby('model lang').sum().sort_values(ascending=False))
# print(results_single['overall'].groupby('fact lang').sum().sort_values(ascending=False))
# print(results_acc['overall'].groupby('model lang').sum().sort_values(ascending=False))
# print(results_acc['overall'].groupby('fact lang').sum().sort_values(ascending=False))

#grid search results
# print(df_to_latex(results_single),bold=False)

#error table
#problems : semantical,grammatical (article)
#semantical P54
#grammatical p27

root = "experiment_results_multi_en/en/mbert_base/all/none/"
df_dict = {}

#region semantical
df_dict['problem type'] = ['semantical']
prompts = []
with open(root+"P54.jsonl", encoding="utf-8") as file:
    for line in file:
        prompts.append(json.loads(line))
    file.close()

for prompt in prompts:
    # if prompt['tokenized_obj_label'] == pred:
    if len(prompt['tokenized_obj_label']) == 1:
        df_dict['prompt'] = [prompt['prompt'].replace('[X]', prompt['sub_label'])]
        df_dict['gold label'] = [prompt['obj_label']]
        df_dict['predictions'] = [sorted(prompt['pred'],key=len)[:5]]
        break
        # print(prompt['prompt'].replace('[X]', prompt['sub_label']),prompt['obj_label'])
        # print(prompt['sentence'],prompt['tokenized_obj_label'],sorted(prompt['pred'],key=len)[:5])
#endregion

#region grammatical
df_dict['problem type'].append('grammatical')

prompts = []
with open(root+"P27.jsonl", encoding="utf-8") as file:
    for line in file:
        prompts.append(json.loads(line))
    file.close()

#prints examples
# for prompt in prompts:
#     for pred in prompt['pred']:
#         if len(prompt['tokenized_obj_label']) == len(pred):
#             print(prompt['prompt'].replace('[X]', prompt['sub_label']), prompt['obj_label'], pred)
df_dict['prompt'].append('Sheryl Crow is [Y] citizen'); df_dict['gold label'].append('United States of America');
df_dict['predictions'].append(['an', '.', 'United', 'States'])
#endregion


# print(pd.DataFrame.from_dict(df_dict).set_index('problem type').to_latex())

# print(best_init.to_latex())
# print(best_iter.to_latex())
# print(best_model.to_latex())
