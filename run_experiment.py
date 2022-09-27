import subprocess

log_dir = "experiment_results"
langs = ["en","hu"]

if __name__ == '__main__':

    for lang in langs:
        subprocess.call(["python", "scripts/probe.py", "--pids", "P36", "--log_dir", log_dir+"_"+lang,
                         "--pred_dir", log_dir+"_"+lang, "--lang", lang],shell=True)
