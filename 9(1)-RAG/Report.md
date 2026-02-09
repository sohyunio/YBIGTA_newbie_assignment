# 9(1)-RAG 과제 분석 리포트
</br>

## 1. 실험 개요
본 실험은 동일한 질문에 대해 검색 지표(Metric)를 변경하며 벡터 검색의 특성을 분석하고, 전통적인 키워드 검색(BM25)과의 차이점을 비교한 결과입니다.

- **테스트 질문**: "What was the advice Lincoln received about his face?"
- **사용 모델**: solar-embedding-1-large-passage

---
</br>

## 2. 벡터 검색 지표(Metric)별 상위 5개 결과 비교

| 순위 | Cosine (유사도) | 내적 (Dot Product) | L2 Norm (거리) |
| :--- | :--- | :--- | :--- |
| **#1** | **0.4116** | **0.4114** | **1.1764** |
| **#2** | 0.3699 | 0.3701 | 1.2598 |
| **#3** | 0.3506 | 0.3511 | 1.2983 |
| **#4** | 0.3488 | 0.3491 | 1.3017 |
| **#5** | 0.3481 | 0.3481 | 1.3032 |

### [벡터 검색 분석 결과]

1. **벡터 정규화(Normalization) 및 일관성 확인**
- **현상 분석**: 실험 결과 Cosine 유사도와 내적 점수가 소수점 셋째 자리까지 거의 일치함이 관찰되었습니다.
- **수학적 근거**: 이는 solar-embedding-1-large 모델이 출력 벡터를 $L2\ Norm = 1$인 단위 벡터로 정규화하여 생성함을 의미합니다. 
단위 벡터 간의 내적값은 수학적으로 코사인 유사도 값과 동일하기 때문에, 지표 변경 시에도 Top-5 결과 순위가 흔들림 없이 일관되게 유지되는 **검색 안정성(Robustness)**을 확인하였습니다.
2. **지표별 점수 체계 및 변별력(Discriminative Power) 비교**
- **유사도 지표(Cosine/내적)**: 약 $0.41 \sim 0.34$ 사이의 좁은 구간에 점수가 밀집되어 있습니다. 이는 문서 간의 맥락적 유사성을 직관적인 비율로 보여주지만, 상위권 문서들 사이의 수치적 차이는 미세하게 나타납니다.
- **거리 지표(L2 Norm)**: 약 $1.17 \sim 1.30$ 사이의 분포를 보이며, 유사도 지표에 비해 문서 간 점수 간격(Score Gap)이 상대적으로 더 크게 나타납니다.
- **분석 결론**: 4096차원의 고차원 공간을 사용하는 Solar 모델 특성상, L2 Norm은 벡터 간의 절대적 거리 차이를 더 민감하게 반영합니다. 따라서 코사인 유사도보다 문서 간의 변별력을 수치적으로 뚜렷하게 확인하는 데 유리하며, 두 지표를 상호보완적으로 활용할 때 검색 신뢰도를 높일 수 있음을 확인하였습니다.


---
</br>

## 3. 키워드 검색(BM25) vs 벡터 검색(Vector) 비교

### [BM25 검색 결과 분석]
키워드 검색 결과, 질문의 핵심 의도와 상관없는 문서들이 상위권에 배치되었습니다.
- **#1 (13.0253)**: 과학적 견해에 대한 편지 내용
- **#2 (12.6614)**: 여성 참정권 및 투표권 관련 내용
- **#3 (12.2576)**: 북극곰 보호 및 해양 포유류 보호법



### [방식별 장단점 및 차이점]

| 구분 | 키워드 검색 (BM25) | 벡터 검색 (Semantic) |
| :--- | :--- | :--- |
| **작동 원리** | 'do', 'you', 'what' 등 단어의 단순 일치 | 질문의 의미 파악 |
| **검색 품질** | 질문의 단어는 포함하나 맥락이 전혀 다름 | 단어 매칭을 넘어 의미적으로 정확한 정보 추출 |
| **장점** | 고유 명사나 특정 키워드 매칭에 강함 | 유의어 처리 및 복잡한 의도 파악에 탁월 |
| **단점** | 단어 간의 관계를 이해하지 못함 | 대규모 데이터에서 계산 리소스가 필요함 |

**최종 결론**: 본 실험에서 BM25는 질문에 쓰인 일반 단어들이 포함된 엉뚱한 문서를 가져온 반면, 벡터 검색은 질문의 의미적 맥락을 파악해 링컨의 수염 조언 문서를 정확히 검색했습니다. RAG 시스템 구축 시 두 방식의 장점을 합친 **Hybrid 방식**이 가장 이상적임을 확인하였습니다.

---
## 참고
<details>
<summary>🔍 [클릭] 키워드 검색 (BM25) 결과 보기</summary>

#1 (score: 13.0253)
"If you would cause your view ... to be acknowledged by scientific men; you would do a great service to science..."
#2 (score: 12.6614)
Until Wilson announced his support for suffrage, a group of women calling themselves Silent Sentinels protested in front of the White House...
#3 (score: 12.2576)
Because many marine mammal populations had plummeted due to over-hunting, the United States passed the federal Marine Mammal Protection Act...
#4 (score: 11.0493)
A common myth about the kangaroo's English name is that it came from the Aboriginal words for "I don't understand you."...
#5 (score: 9.4082)
When the real Great White Fleet sailed into Yokahama, Japan, the Japanese went to extraordinary lengths to show that their country desired peace...

</details>

<details>
<summary>🔍 [클릭] Cosine 유사도 결과 보기</summary>

#1 (score: 0.4116)
While Lincoln is usually portrayed bearded, he first grew a beard in 1860 at the suggestion of 11-year-old Grace Bedell
#2 (score: 0.3699)
Warned by his law partner, William Herndon, that the damage was mounting and irreparable...
#3 (score: 0.3506)
Abraham Lincoln's official White House portrait
#4 (score: 0.3488)
Lincoln wrote a series of anonymous letters, published in 1842 in the Sangamon Journal...
#5 (score: 0.3481)
Lincoln, in top hat, with Allan Pinkerton and Gen. John Alexander McClernand at Antietam.

</details>

<details>
<summary>🔍 [클릭] 내적 (Dot Product) 결과 보기</summary>

#1 (score: 0.4114)
While Lincoln is usually portrayed bearded, he first grew a beard in 1860 at the suggestion of 11-year-old Grace Bedell
#2 (score: 0.3701)
Warned by his law partner, William Herndon, that the damage was mounting and irreparable...
#3 (score: 0.3511)
Abraham Lincoln's official White House portrait
#4 (score: 0.3491)
Lincoln wrote a series of anonymous letters, published in 1842 in the Sangamon Journal...
#5 (score: 0.3481)
Lincoln, in top hat, with Allan Pinkerton and Gen. John Alexander McClernand at Antietam.

</details>

<details>
<summary>🔍 [클릭] L2 Norm (Euclidean) 결과 보기</summary>

#1 (score: 1.1764)
While Lincoln is usually portrayed bearded, he first grew a beard in 1860 at the suggestion of 11-year-old Grace Bedell
#2 (score: 1.2598)
Warned by his law partner, William Herndon, that the damage was mounting and irreparable...
#3 (score: 1.2983)
Abraham Lincoln's official White House portrait
#4 (score: 1.3017)
Lincoln wrote a series of anonymous letters, published in 1842 in the Sangamon Journal...
#5 (score: 1.3032)
Lincoln, in top hat, with Allan Pinkerton and Gen. John Alexander McClernand at Antietam.

</details>