# Investigating language bias in pretrained multilingual language models

In this repo, you will find the modified and expanded code of: 
> [X-FACTR: Multilingual Factual Knowledge Retrieval from Pretrained Language Models](https://arxiv.org/abs/2010.06189)
>
> Zhengbao Jiang, Antonios Anastasopoulos, Jun Araki, Haibo Ding, Graham Neubig

for investigating language bias in pretrained multilingual language models

### Files added

```scripts/run_experiment.py```: script to run the single prediction experiments for a specific prompt language

```scripts/run_multi_experiment.py```: script to run the multi prediction experiments for a specific prompt language

```query_data.py```: script to run wikidata queries, creates jsondict.p

```formatting.py```: script to create all the data files using jsondict.p

```scripts/evaluate_experiments_table.py```: script to create a results table for the single prediction results

```scripts/evaluate_experiments_table_multi.py```: script to create a results table for the multi prediction results

```evaluate_results.py```: script to evaluate the result tables for our experiments and to create summarized and example
tables for our paper

### Environment setup
Run the following bash script (some libraries might have to be installed manually via pip, depending on the OS):
```shell
bash setup.sh
```
### Running the data creation scripts
#### Running wikidata queries
```shell
python query_data.py
```

#### create files using retrieved data
```shell
python formatting.py
```

### Running the experiments
#### Single prediction (```--lang``` can be ```en```, ```nl```, ```hu```)
```shell
python scripts/run_experiment.py --lang=en
```
#### Multi prediction (```--lang``` can be ```en```, ```nl```, ```hu```)
```shell
python scripts/run_experiment.py --lang=en
```
### Evaluation scripts
#### Single predicition accuracy
```shell
python scripts/evaluate_experiment_table.py
```

#### Multi prediction top n accuracy
```shell
python scripts/evaluate_experiment_table_multi.py
```

#### Multi prediction precision at k
```shell
python scripts/evaluate_experiment_table_multi.py --metric precision
```






[//]: # (Typical usage of probing &#40;the script should be called from the base folder&#41;:  )

[//]: # (python .\scripts\probe.py --pids "P36" --pred_dir experiment_results --log_dir experiment_results --lang en --num_mask 1   )

[//]: # (useful arguments:  )

[//]: # (pids - prompt ids connected with a , -> "P36,P20"   )

[//]: # (pred_dir & log_dir - path to save the prediction and log files &#40;jsonl and csv&#41; -> experiment_results  )

[//]: # (lang - language to use -> en   )

[//]: # (num_mask - number of word to predict &#40;starting from 1&#41; -> 1  )

[//]: # (prompts - path of the folder which contains prompts for the model to use -> "own_prompts_en" )