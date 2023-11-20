#!/bin/bash

if [ "$#" -ne 1 ]; then
  echo "Provide DATA_GENERATION parameter"
  exit 1
fi

DATA_GENERATION=$1

data_dir="./data"

clusters_centers_f="clusters_centers_use_dg$DATA_GENERATION.pkl"
clusters_use_f="clusters_use_dg$DATA_GENERATION.json"
use_embeddings_f="use_embeddings_dg$DATA_GENERATION.pkl"
data_files=("$clusters_centers_f" "$clusters_use_f" "$use_embeddings_f")

if [ ! -d "$data_dir" ]; then
  echo "Dir '$data_dir' doesn't exists. Put your data in '$data_dir'"
  exit 1
fi

for f_name in "${data_files[@]}"; do
  if [ -e "$data_dir/$f_name" ]; then
    echo "$data_dir/$f_name exists"
  else
    echo "$data_dir/$f_name doesn't exist. Provide all data"
    exit 1
  fi
done

echo "All data exists. Preparing data..."

if python3 utils/prepare_data.py "$DATA_GENERATION"; then
    echo "Python script executed successfully"
else
    echo "Error: Python script encountered an issue"
    exit 1
fi

echo "Done! Prepared data is in /var/data directory"
