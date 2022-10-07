import subprocess
import platform
import os

if __name__ == '__main__':

    langs = ["en", "hu", "nl"]

    OS = platform.system()
    if OS == 'Darwin' or OS == 'Linux':
        use_shell = False
    else:
        use_shell = True

    for mlang in langs:

        #loading dataset
        files = os.listdir('own_facts_' + mlang )
        pids = [file.split('.')[0] for file in files]
        num_mask = (5 if mlang != "hu" else 10)

        for plang in langs:
            pid_num = 0
            for pid in pids:

                experiment = subprocess.run(["python", "scripts/probe.py",
                                             "--pids", pid,
                                             "--log_dir", "experiment_results_"+mlang+"/"+plang,
                                             "--pred_dir", "experiment_results_"+mlang+"/"+plang,
                                             "--lang", mlang,
                                             "--num_mask", str(num_mask),
                                             "--portion", "all",
                                            "--custom_facts", "own_facts_"+plang+"/"+pid+".jsonl"],
                                            shell=use_shell)

                if experiment.returncode != 0: raise RuntimeError("Experiment failed - Subprocess exit code 1")

                pid_num += 1
                print(f"Prompt {pid} done, {pid_num} out of {len(pids)} prompts.")

            print(f"Prompt language {plang} done.")

        print(f"Model language {mlang} done.")


