from ana import load_result, compute_acc
from probe import tokenizer_wrap, LamaPredictions, EvalContext, CsvLogFileContext, load_entity_lang, \
    DATASET, PROMPT_LANG_PATH
import argparse
import os


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Analysis')
    parser.add_argument('--task', type=str,
                        choices=['accuracy', 'MCR', 'visualization'],
                        default='accuracy')
    parser.add_argument('--lang', type=str, help='language', default='en')
    parser.add_argument('--probe', type=str, help='probe dataset',
                        choices=['lama', 'lama-uhn', 'mlama', 'mlamaf'], default='mlamaf')
    parser.add_argument('--model', type=str, help='LM to probe file', default='mbert_base')
    parser.add_argument('--norm', action='store_true')
    parser.add_argument('--multi_lang', type=str, help='use additional language in evaluation', default=None)
    parser.add_argument('--skip_cate', action='store_true')
    parser.add_argument('--gold_len', action='store_true', help='use the number of tokens in ground truth')
    parser.add_argument('--only_count', action='store_true')
    parser.add_argument('--inp', type=str, help='input')
    parser.add_argument('--out', type=str, help='output')
    args = parser.parse_args()

    print('Reading result files...')

    root_folder = "./experiment_results_en/"

    files = os.listdir(root_folder)

    eval = EvalContext(args)
    for result_file_name in files:
        if '.jsonl' not in result_file_name:
            continue

        pid_num = result_file_name.split(".")[0]
        acc, acc_single, acc_multi, total, total_single, total_multi = compute_acc(root_folder + result_file_name, eval,
                                                                                   prettify_out_file='test_{}'.format(pid_num),
                                                                                   only_count=args.only_count)

        print('-', pid_num, '-', '\nOverall accuracy', acc, '\nSingle word accuracy:', acc_single, '\nMultiword accuracy:', acc_multi)




















    # TODO: specifiy our own, custom task/metrics to evaluate on and write evaluation code

