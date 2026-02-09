"""Vector retriever using Pinecone (cosine similarity)."""

import os

from dotenv import load_dotenv
from pinecone import Pinecone

from ingest.embedding import embed_query

load_dotenv()


def search(query: str, top_k: int = 10) -> list[dict]:
    """Vector cosine similarity search.

    Args:
        query: Search query string.
        top_k: Number of results to return.

    Returns:
        list[dict], each dict has keys: "id", "text", "score", "method".
        "method" should be "Vector".

    Hints:
        - Use embed_query(query) to get the query embedding vector
        - Connect: Pinecone(api_key=...) → pc.Index(index_name)
        - Use index.query(vector=..., top_k=..., include_metadata=True)
        - Text is in match["metadata"]["text"]
    """
    # 1. 질문을 벡터(4096차원)로 변환
    query_embedding = embed_query(query)

    # 2. Pinecone 인덱스 연결
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    index_name = os.getenv("PINECONE_INDEX")
    index = pc.Index(index_name)

    # 3. 벡터 유사도 검색 수행
    response = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True
    )

    # 4. 결과 포맷팅
    results = []
    for match in response["matches"]:
        results.append({
            "id": match["id"],
            "text": match["metadata"]["text"], # 메타데이터에서 텍스트 추출
            "score": match["score"],           # 코사인 유사도 점수
            "method": "Vector"
        })

    return results
