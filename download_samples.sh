#!/bin/bash

BASE_URL='https://archive.org/download/stackexchange/'
DATA_PATH='data/'

for sample in workplace.meta.stackexchange.com.7z unix.meta.stackexchange.com.7z
do 
    if [[ $sample == *".meta"* ]]; then
       base_name=$(echo $sample | sed 's/.meta.stackexchange.com.7z//')
    else
       base_name=$(echo $sample | sed 's/.stackexchange.com.7z//')
    fi
    full_url=$BASE_URL$sample
    echo $full_url
    echo $base_name
    mkdir -p $DATA_PATH/$base_name
    curl -L $full_url -o $DATA_PATH/$base_name/$sample
    7za e  -o$DATA_PATH$base_name/ $DATA_PATH$base_name/$sample
done