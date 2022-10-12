from ana import load_result, compute_acc
from probe import tokenizer_wrap, LamaPredictions, EvalContext, CsvLogFileContext, load_entity_lang, \
    DATASET, PROMPT_LANG_PATH
import argparse
import os
import json
import numpy as np
import pandas as pd
from typing import List, Dict, Tuple, Set

def get_top_five_preds(json_file):

    data = [json.loads(line) for line in open(json_file,'r')]

    for d in data:
        print('----------')
        print('Gold:', d['obj_label'])
        for i, p in enumerate(d['pred']):
            print
            print(f'Prediction {i+1}:', ' '.join(p))
        print('----------')


def compute_precision(in_file: str, eval: EvalContext, prettify_out_file: str=None, only_count: bool=False) \
        -> Tuple[float, float, float, int, int, int]:
    headers = ['sentence', 'prediction', 'gold', 'is_same', 'confidence', 'is_single_word', 'sub_uri', 'obj_uri']
    result: List[LamaPredictions] = load_result(in_file)
    correct = total = 0
    correct_single = total_single = 0
    correct_multi = total_mutli = 0
    with CsvLogFileContext(prettify_out_file, headers=headers) as csv_file:
        for r in result:
            for i in range(len(r.result['pred'])):
                r.result['pred_log_prob'] = [[0]]*len(r.result['pred'])
                r.result['pred_log_prob'][i] = [1]
                if eval.skip_cate and r.is_cate(eval.entity2iscate):
                    continue
                right = 0
                if not only_count:
                    right = int(r.eval(eval))
                    if csv_file:
                        r.prettify(csv_file, eval)
                correct += right
                total += 1
                if r.is_single_word:
                    correct_single += right
                    total_single += 1
                else:
                    correct_multi += right
                    total_mutli += 1
    return correct / (total or 1)/ len(r.result['pred']), \
           correct_single / (total_single or 1)/ len(r.result['pred']), \
           correct_multi / (total_mutli or 1)/ len(r.result['pred']), \
           total, total_single, total_mutli


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
    parser.add_argument('--metric', type=str,choices=['accuracy', 'precision'],
                        default='accuracy')
    # parser.add_argument('--root_folder', type=str, default="./experiment_results_en/en/")
    args = parser.parse_args()

    print('Reading result files...')

    if args.metric == 'accuracy':
        metric = compute_acc
    elif args.metric == 'precision':
        metric = compute_precision
    else:
        raise NotImplementedError

    res_dict = {}
    for lang in ['en', 'nl', 'hu']:
    # for lang in ['en']:
        res_dict[lang] = {}
        for lang2 in ['en', 'nl', 'hu']:
            res_dict[lang][lang2] = {}
            for model in ["mbert_base"]:
                res_dict[lang][lang2][model] = {}
                for init_method in ['all']:
                    res_dict[lang][lang2][model][init_method] = {}
                    for iter_method in ['none']:

                        root_folder = f"./experiment_results_multi_{lang}/{lang2}/{model}/{init_method}/{iter_method}/"

                        files = os.listdir(root_folder)

                        eval = EvalContext(args)

                        res_dict[lang][lang2][model][init_method][iter_method] = {}
                        accs = []
                        single_accs = []
                        multi_accs = []
                        acc_explicit = []
                        acc_non_explicit = []
                        for result_file_name in files:
                            if '.jsonl' not in result_file_name:
                                continue

                            pid_num = result_file_name.split(".")[0]
                            acc, acc_single, acc_multi, total, total_single, total_multi = metric(root_folder + result_file_name, eval,
                                                                                                    prettify_out_file='test_{}'.format(pid_num),
                                                                                                    only_count=args.only_count)
                            accs.append(acc)
                            single_accs.append(acc_single)
                            multi_accs.append(acc_multi)
                            if pid_num in ['P17','P27','P495']:
                                acc_explicit.append(acc)
                            else:
                                acc_non_explicit.append(acc)
                            # print('-', pid_num, '-', '\nOverall accuracy', acc, '\nSingle word accuracy:', acc_single, '\nMultiword accuracy:', acc_multi)

                            # print('- #1 predictions for M 1-M -')
                            #
                            # get_top_five_preds(root_folder + result_file_name)

                        res_dict[lang][lang2][model][init_method][iter_method]['overall'] = np.mean(accs)
                        res_dict[lang][lang2][model][init_method][iter_method]['single_word'] = np.mean(single_accs)
                        res_dict[lang][lang2][model][init_method][iter_method]['multi_word'] = np.mean(multi_accs)
                        res_dict[lang][lang2][model][init_method][iter_method]['explicit'] = np.mean(acc_explicit)
                        res_dict[lang][lang2][model][init_method][iter_method]['non_explicit'] = np.mean(acc_non_explicit)

                        df = pd.DataFrame.from_dict({(i,j,k,l,m): res_dict[i][j][k][l][m]
                                       for i in res_dict.keys()
                                       for j in res_dict[i].keys()
                                       for k in res_dict[i][j].keys()
                                       for l in res_dict[i][j][k].keys()
                                       for m in res_dict[i][j][k][l].keys()},
                                   orient='index')
    print(df)
    df.to_csv(f'results_df_multi_{args.metric}.csv',index_label= ['model lang', 'fact lang', 'model', 'init method', 'iter method'])

















    # TODO: specifiy our own, custom task/metrics to evaluate on and write evaluation code

