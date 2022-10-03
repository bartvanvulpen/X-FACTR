Typical usage of probing (the script should be called from the base folder):  
python .\scripts\probetest.py --pids "P36" --pred_dir experiment_results --log_dir experiment_results --lang en --num_mask 1   
useful arguments:  
pids - prompt ids connected with a , -> "P36,P20"   
pred_dir & log_dir - path to save the prediction and log files (jsonl and csv) -> experiment_results  
lang - language to use -> en   
num_mask - number of word to predict (starting from 1) -> 1  
prompts - path of the folder which contains prompts for the model to use -> "own_prompts_en"  
