"""Ingest embeddings into Pinecone vector index.

Batch upsert: 100 vectors per call.
Metadata: text truncated to 1000 chars (40KB limit).
"""

import json
import os
from pathlib import Path

import numpy as np
from dotenv import load_dotenv
from pinecone import Pinecone
from tqdm import tqdm

load_dotenv()

RAW_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "raw"
PROCESSED_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "processed"

BATCH_SIZE = 100
TEXT_LIMIT = 1000  # metadata text truncation


def ingest(progress_callback=None):
    """Batch upsert embeddings into Pinecone vector index.

    Args:
        progress_callback: Optional callback(current, total) for progress updates.

    Returns:
        int: Number of vectors upserted.

    Hints:
        - Load embeddings from PROCESSED_DIR / "embeddings.npy"
        - Load IDs from PROCESSED_DIR / "embedding_ids.json"
        - Load texts from RAW_DIR / "corpus.jsonl" for metadata
        - Connect: Pinecone(api_key=...) → pc.Index(index_name)
        - Upsert format: {"id": ..., "values": [...], "metadata": {"text": ...}}
        - Batch size: BATCH_SIZE (100), truncate text to TEXT_LIMIT (1000) chars
    """
    # 1. Pinecone 연결 및 인덱스 설정
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    index_name = os.getenv("PINECONE_INDEX_NAME", "wiki-index")
    index = pc.Index(index_name)

    # 2. 캐시된 임베딩 데이터 불러오기
    embeddings = np.load(PROCESSED_DIR / "embeddings.npy")
    with open(PROCESSED_DIR / "embedding_ids.json", "r") as f:
        ids = json.load(f)
    
    # 3. 메타데이터용 텍스트 원문 불러오기
    texts = []
    with open(RAW_DIR / "corpus.jsonl", "r", encoding="utf-8") as f:
        for line in f:
            texts.append(json.loads(line)["text"])

    total_count = len(ids)

    # 4. 데이터 적재 (Batch 처리)
    for i in tqdm(range(0, total_count, BATCH_SIZE), desc="Upserting to Pinecone"):
        end = min(i + BATCH_SIZE, total_count)
        
        records = []
        for j in range(i, end):
            records.append({
                "id": ids[j],
                "values": embeddings[j].tolist(),
                "metadata": {
                    "text": texts[j][:TEXT_LIMIT] # 글자 수 제한 준수
                }
            })
        
        index.upsert(vectors=records)
        
        if progress_callback:
            progress_callback(end, total_count)

    print(f"Successfully upserted {total_count} vectors to Pinecone.")
    return total_count


if __name__ == "__main__":
    ingest()
