import subprocess
import platform




log_dir = "experiment_results"
# langs = ["en","hu","nl"]
langs = ["en"] #for testing
pids = ["P36","P39"]
pids_arg = ",".join(pids)
# TODO : Dynamic pid reading from external file







if __name__ == '__main__':

    OS = platform.system()
    if OS == 'Darwin' or OS == 'Linux':
        use_shell = False
    else:
        use_shell = True

    for lang in langs:
        experiment = subprocess.run(["python", "scripts/probe.py", "--pids", pids_arg, "--log_dir", log_dir+"_"+lang,
                         "--pred_dir", log_dir+"_"+lang, "--lang", lang], shell=use_shell)

        if experiment.returncode != 0 : raise RuntimeError("Experiment failed - Subprocess exit code 1")
