#!/bin/bash

# Script to download precomputed metamodels
echo "BASE DIRECTORY IS $1"

export MODEL_URL=https://openstudio-metamodels.s3.amazonaws.com

check_and_download() {
	FILE_PATH=$1
	MODEL_NAME=$2

	echo $FILE_PATH
	echo $MODEL_NAME
	if [[ ! -e $FILE_PATH/$MODEL_NAME ]]; then
		mkdir -p $FILE_PATH
		curl -SL $MODEL_URL/$MODEL_NAME -o $FILE_PATH/$MODEL_NAME 
		unzip $FILE_PATH/$MODEL_NAME -d $FILE_PATH
	else
		echo "Model already downloaded: $MODEL_NAME"
	fi
}

check_and_download "$1/models/smoff_sweep_v2/RandomForest/models" "smoff_sweep_v2.zip"
check_and_download "$1/models/smoff_sweep_no_ets_v2/RandomForest/models" "smoff_sweep_no_ets_v2.zip"
check_and_download "$1/models/retail_sweep_v2/RandomForest/models" "retail_sweep_v2.zip"
check_and_download "$1/models/retail_sweep_no_ets_v2/RandomForest/models" "retail_sweep_no_ets_v2.zip"



