"""Ingest corpus into Elasticsearch BM25 index (wiki-bm25).

Index mapping: text field only (no vectors).
Bulk chunk_size=500 (lightweight without vectors).
"""

import json
import os
from pathlib import Path

from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from tqdm import tqdm

load_dotenv()

INDEX_NAME = "wiki-bm25"
RAW_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "raw"

INDEX_MAPPINGS = {
    "properties": {
        "text": {"type": "text", "analyzer": "standard"},
    }
}


def get_es_client() -> Elasticsearch:
    return Elasticsearch(
        os.getenv("ELASTIC_ENDPOINT"),
        api_key=os.getenv("ELASTIC_API_KEY"),
        request_timeout=60,
    )


def _generate_actions(corpus_path: Path):
    with open(corpus_path, encoding="utf-8") as f:
        for line in f:
            doc = json.loads(line)
            yield {
                "_index": INDEX_NAME,
                "_id": doc["id"],
                "_source": {
                    "text": doc["text"],
                },
            }


def ingest(progress_callback=None):
    """Create BM25 index and bulk-ingest corpus into Elasticsearch.

    Args:
        progress_callback: Optional callback(count) called after completion.

    Returns:
        int: Number of documents indexed.

    Hints:
        - Use get_es_client() to get ES client
        - Delete existing index if it exists, then create with INDEX_MAPPINGS
        - Corpus is at RAW_DIR / "corpus.jsonl"
        - Use _generate_actions(corpus_path) for bulk data
        - Use elasticsearch.helpers.bulk() with chunk_size=500
        - Call es.indices.refresh() after bulk ingest
    """
    # 1. ES client 가져오기
    es = get_es_client()
    corpus_path = RAW_DIR / "corpus.jsonl"

    # 2. 기존 인덱스 있다면 삭제 (중복방지 및 초기화)
    if es.indices.exists(index=INDEX_NAME):
        es.indices.delete(index=INDEX_NAME)

    # 3. 새로운 인덱스 생성
    es.indices.create(index=INDEX_NAME, mappings=INDEX_MAPPINGS)

    # 4. 데이터 대량 적재
    success_count, _ = bulk(
        es,
        _generate_actions(corpus_path),
        chunk_size=500,
        stats_only=True
    )

    # 5. 인덱스 새로고침
    es.indices.refresh(index=INDEX_NAME)

    # 6. 진행 완료 알림 및 결과 반환
    if progress_callback:
        progress_callback(success_count)

    print(f"Successfully indexed {success_count} documents to {INDEX_NAME}.")
    return success_count



if __name__ == "__main__":
    ingest()
