from ana import load_result, compute_acc
from probe import tokenizer_wrap, LamaPredictions, EvalContext, CsvLogFileContext, load_entity_lang, \
    DATASET, PROMPT_LANG_PATH
import argparse
import os
import json
import numpy as np
import pandas as pd
def get_top_five_preds(json_file):

    data = [json.loads(line) for line in open(json_file,'r')]

    for d in data:
        print('----------')
        print('Gold:', d['obj_label'])
        for i, p in enumerate(d['pred']):
            print
            print(f'Prediction {i+1}:', ' '.join(p))
        print('----------')





if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Analysis')
    parser.add_argument('--task', type=str,
                        choices=['accuracy', 'MCR', 'visualization'],
                        default='accuracy')
    parser.add_argument('--lang', type=str, help='language', default='en')
    parser.add_argument('--probe', type=str, help='probe dataset',
                        choices=['lama', 'lama-uhn', 'mlama', 'mlamaf', 'own'], default='own')
    parser.add_argument('--model', type=str, help='LM to probe file', default='mbert_base')
    parser.add_argument('--norm', action='store_true')
    parser.add_argument('--multi_lang', type=str, help='use additional language in evaluation', default=None)
    parser.add_argument('--skip_cate', action='store_true')
    parser.add_argument('--gold_len', action='store_true', help='use the number of tokens in ground truth')
    parser.add_argument('--only_count', action='store_true')
    parser.add_argument('--inp', type=str, help='input')
    parser.add_argument('--out', type=str, help='output')
    # parser.add_argument('--root_folder', type=str, default="./experiment_results_en/en/")
    args = parser.parse_args()

    print('Reading result files...')

    res_dict = {}
    for lang in ['en', 'nl', 'hu']:
        res_dict[lang] = {}
        for lang2 in ['en', 'nl', 'hu']:

            root_folder = f"./experiment_results_{lang}/{lang2}/"

            files = os.listdir(root_folder)

            eval = EvalContext(args)

            res_dict[lang][lang2] = {}
            accs = []
            single_accs = []
            multi_accs = []
            for result_file_name in files:
                if '.jsonl' not in result_file_name:
                    continue

                pid_num = result_file_name.split(".")[0]
                acc, acc_single, acc_multi, total, total_single, total_multi = compute_acc(root_folder + result_file_name, eval,
                                                                                        prettify_out_file='test_{}'.format(pid_num),
                                                                                        only_count=args.only_count)
                accs.append(acc)
                single_accs.append(acc_single)
                multi_accs.append(acc_multi)
            

                # print('-', pid_num, '-', '\nOverall accuracy', acc, '\nSingle word accuracy:', acc_single, '\nMultiword accuracy:', acc_multi)

                # print('- #1 predictions for M 1-M -')
                #
                # get_top_five_preds(root_folder + result_file_name)
            res_dict[lang][lang2]['overall'] = np.mean(accs)
            res_dict[lang][lang2]['single_word'] = np.mean(single_accs)
            res_dict[lang][lang2]['multi_word'] = np.mean(multi_accs)

            df = pd.DataFrame.from_dict({(i,j): res_dict[i][j] 
                           for i in res_dict.keys() 
                           for j in res_dict[i].keys()},
                       orient='index')
    print(df)

















    # TODO: specifiy our own, custom task/metrics to evaluate on and write evaluation code

