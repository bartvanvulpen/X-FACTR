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
#### Running Wikidata queries
```shell
python query_data.py
```

#### Create files using retrieved data
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
