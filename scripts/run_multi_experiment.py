import subprocess
import platform
import os

if __name__ == '__main__':

    langs = ["en", "hu", "nl"]
    models = ["mbert_base", "xlm_base"]
    init_methods = ['all', 'left', 'confidence']
    iter_methods = ['none', 'left', 'confidence', 'confidence-multi']

    OS = platform.system()
    if OS == 'Darwin' or OS == 'Linux':
        use_shell = False
    else:
        use_shell = True


    for mlang in langs: #model language

        #loading dataset
        files = os.listdir('own_facts_' + mlang )
        pids = [file.split('.')[0] for file in files]
        num_mask = (5 if mlang != "hu" else 10)

        for plang in langs: #prompt language
            pid_num = 0
            for model in models:
                print(f"Probing with model language {mlang},prompt language {plang},model {model}")
                for init_method in init_methods:
                    for iter_method in iter_methods:
                        for pid in pids: #pid number

                            experiment = subprocess.run(["python", "scripts/probe_multi_pred.py",
                                                         "--model", model,
                                                         "--pids", pid,
                                                         "--log_dir", f"testexperiment_results_{mlang}/{plang}/{model}/{init_method}/{iter_method}",
                                                         "--pred_dir", f"testexperiment_results_{mlang}/{plang}/{model}/{init_method}/{iter_method}",
                                                         "--lang", mlang,
                                                         "--num_mask", str(num_mask),
                                                         "--portion", "all",
                                                         "--init_method", init_method,
                                                         "--iter_method", iter_method,
                                                         "--max_iter", str(num_mask),
                                                        "--custom_facts", "own_facts_"+plang+"/"+pid+".jsonl"],
                                                        shell=use_shell)

                            if experiment.returncode != 0 : raise RuntimeError("Experiment failed - Subprocess exit code 1")

                            pid_num += 1
                            print(f"Prompt {pid} done, {pid_num} out of {len(pids)} prompts.")

                print(f"{model} model done.")
            print(f"Prompt language {plang} done.")

        print(f"Model language {mlang} done.")




