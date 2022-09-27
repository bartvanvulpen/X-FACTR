import sys
from os.path import dirname, abspath
import argparse
from probe import *

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='probe LMs with multilingual LAMA')
    parser.add_argument('--model', type=str, help='LM to probe file', default='mbert_base')
    parser.add_argument('--lm_layer_model', type=str,
                        help='LM from which the final lm layer is used', default=None)
    parser.add_argument('--lang', type=str, help='language to probe',
                        choices=['en', 'fr', 'nl', 'es', 'zh',
                                 'mr', 'vi', 'ko', 'he', 'yo',
                                 'el', 'tr', 'ru',
                                 'ja', 'hu', 'bn', 'war', 'tl', 'sw',
                                 'mg', 'pa', 'ilo', 'ceb'], default='en')
    parser.add_argument('--sent', type=str, help='actual sentence with [Y]', default=None)

    # dataset-related flags
    parser.add_argument('--probe', type=str, help='probe dataset',
                        choices=['lama', 'lama-uhn', 'mlama', 'mlamaf'], default='mlamaf')
    parser.add_argument('--pids', type=str, help='pids to run', default=None)
    parser.add_argument('--portion', type=str, choices=['all', 'trans', 'non'], default='trans',
                        help='which portion of facts to use')
    parser.add_argument('--facts', type=str, help='file path to facts', default=None)
    parser.add_argument('--prompts', type=str, default=None,
                        help='directory where multiple prompts are stored for each relation')
    parser.add_argument('--sub_obj_same_lang', action='store_true',
                        help='use the same language for sub and obj')
    parser.add_argument('--skip_multi_word', action='store_true',
                        help='skip objects with multiple words (not sub-words)')
    parser.add_argument('--skip_single_word', action='store_true',
                        help='skip objects with a single word')

    # inflection-related flags
    parser.add_argument('--prompt_model_lang', type=str, help='prompt model to use',
                        choices=['en', 'el', 'ru', 'es', 'mr'], default=None)
    parser.add_argument('--disable_inflection', type=str, choices=['x', 'y', 'xy'])
    parser.add_argument('--disable_article', action='store_true')

    # decoding-related flags
    parser.add_argument('--num_mask', type=int, help='the maximum number of masks to insert', default=5)
    parser.add_argument('--max_iter', type=int, help='the maximum number of iteration in decoding', default=1)
    parser.add_argument('--init_method', type=str, help='iteration method', default='all')
    parser.add_argument('--iter_method', type=str, help='iteration method', default='none')
    parser.add_argument('--no_len_norm', action='store_true', help='not use length normalization')
    parser.add_argument('--reprob', action='store_true', help='recompute the prob finally')
    parser.add_argument('--beam_size', type=int, help='beam search size', default=1)

    # others
    parser.add_argument('--use_gold', action='store_true', help='use gold objects')
    parser.add_argument('--dry_run', type=int, help='dry run the probe to show inflection results', default=None)
    parser.add_argument('--log_dir', type=str, help='directory to vis prediction results', default=None)
    parser.add_argument('--pred_dir', type=str, help='directory to store prediction results', default=None)
    parser.add_argument('--batch_size', type=int, help='the real batch size is this times num_mask', default=20)
    parser.add_argument('--no_cuda', action='store_true', help='not use cuda')
    args = parser.parse_args()

    LM = LM_NAME[args.model] if args.model in LM_NAME else args.model

    # load data
    print('load data')
    tokenizer = get_tokenizer(args.lang, LM)
    probe_iter = ProbeIterator(args, tokenizer)

    # load model
    print('load model')
    model = AutoModelWithLMHead.from_pretrained(LM)

    if args.lm_layer_model is not None:
        llm = LM_NAME[args.lm_layer_model] if args.lm_layer_model in LM_NAME else args.lm_layer_model

        llm = AutoModelWithLMHead.from_pretrained(llm)
        model.cls = llm.cls
    model.eval()
    if torch.cuda.is_available() and not args.no_cuda:
        model.to('cuda')

    probe_iter.iter(pids=set(args.pids.strip().split(',')) if args.pids is not None else None)


