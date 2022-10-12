import pandas as pd
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.max_colwidth', 1000)
pd.set_option('display.width', 1000)

# tablecsv = pd.read_csv('exp_res/P36.csv')
# print(tablecsv.head(10))
# tablejson = pd.read_json('exp_res/P36.jsonl', lines=True)
# print("\n",tablejson.head(30))
results = pd.read_csv('results_df.csv',index_col=['model lang', 'fact lang', 'model', 'init method', 'iter method'])
print(results,'\n')
best_iter = results['overall'].groupby('iter method').sum().sort_values(ascending=False)
best_init = results['overall'].groupby('init method').sum().sort_values(ascending=False)
best_model = results['overall'].groupby('model').sum().sort_values(ascending=False)
print('BEST PARAMS:\n',best_iter,'\n',best_init,'\n',best_model)
idx = pd.IndexSlice
best_results = results.loc[idx[:,:,best_model.index[0],best_init.index[0],best_iter.index[0]], :]
print(best_results)
print(best_results.reset_index(level=['model','init method', 'iter method'],drop=True).to_latex())
# best_init.apply(print)
