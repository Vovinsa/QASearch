import faiss
import numpy as np

import json
import os
import shutil
import sys
from tqdm import tqdm


os.makedirs('/var/data/clusters', exist_ok=True)
os.makedirs('/var/data/indexes', exist_ok=True)
os.makedirs('/var/data/other', exist_ok=True)

DATA_GENERATION = sys.argv[1]

shutil.copy(
    f'./data/clusters_centers_use_dg{DATA_GENERATION}.pkl',
    f'/var/data/clusters/clusters_centers_use_dg{DATA_GENERATION}.pkl'
)

embeddings = np.load(f'data/use_embeddings_dg{DATA_GENERATION}.pkl', allow_pickle=True)

with open(f'data/clusters_use_dg{DATA_GENERATION}.json') as f:
    clusters = json.load(f)

for cluster, documents in clusters.items():
    print(f'Cluster {cluster}')
    documents_embeddings = []
    index_document = {}
    for i, document in enumerate(tqdm(documents)):
        documents_embeddings.append(embeddings[document])
        index_document[i] = document
    faiss_indexes = faiss.IndexFlatL2(512)
    faiss_indexes.add(np.vstack(documents_embeddings))
    faiss.write_index(faiss_indexes, f'/var/data/indexes/indexes_dg{DATA_GENERATION}_cluster{cluster}.faiss')
    with open(f'/var/data/other/index_document_cluster{cluster}.json', 'w') as f:
        json.dump(index_document, f)
