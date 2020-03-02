#!/usr/bin/env bash

#set -e

models=$1  # a list of models joined by ","
langs=$2  # a list of languages joined by ","
out_dir=$3  # dir to save output
args="${@:4}"

mkdir -p ${out_dir}

IFS=','
read -ra MODELS <<< "${models}"
read -ra LANGS <<< "${langs}"

for m in "${MODELS[@]}"; do # access each element of array
    for l in "${LANGS[@]}"; do
        echo "==========" $m $l ${args} "=========="
        filename=${out_dir}/${m}__${l}.out
        echo "python scripts/probe.py --model $m --lang $l ${args} &> $filename" > $filename
        python scripts/probe.py --model $m --lang $l "${@:4}" &>> $filename
        tail -n 1 $filename
    done
done