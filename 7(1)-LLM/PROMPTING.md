# Prompting Method Performance Report

## 1. 정답률 비교 결과 (Accuracy Comparison)

본 실험은 **Llama-3.1-8B-instant** 모델을 사용하였으며,  
**GSM8K 테스트 데이터셋** 중 50개 샘플을 무작위 추출하여 수행되었습니다.

| Prompting Method | 0-shot Accuracy | 3-shot Accuracy | 5-shot Accuracy |
|------------------|----------------|----------------|----------------|
| Direct Prompting | 0.80 | 0.78 | 0.80 |
| CoT Prompting | 0.80 | 0.82 | 0.82 |
| My Prompting | 0.80 | 0.84 | 0.88 |

---

## 2. CoT Prompting이 Direct Prompting보다 우수한 이유

- 사고 과정의 명시화: "thinking step-by-step" 지시어를 통해 모델이 중간 추론 과정을 생략하지 않고 논리적으로 전개하도록 유도했습니다.

- 추론 가독성 증대: "Show your work clearly"라는 지시를 통해 모델이 복잡한 연산 과정을 체계적으로 나열하게 함으로써, 정답 도출의 근거를 명확히 하였습니다.

- Few-shot의 시너지: Direct 방식과 달리 CoT 방식은 예시(Shot)를 통해 단계별 풀이 스타일을 모방할 수 있어, 샷 수가 늘어날수록 정답률이 상승하는 경향을 보였습니다.

---

## 3. My Prompting이 CoT Prompting에 비해 우수한 이유

- 프롬프트 구조의 최적화: My Prompting에서는 지시사항을 불릿 포인트(-) 형식으로 나열하여 모델이 지시 사항을 더 직관적으로 파악할 수 있도록 구조화했습니다.

- 출력 가이드의 명확성: CoT에서는 "provide the final answer"라고 명시한 반면, My Prompting에서는 "You must end with 'Final Answer: #### ...'"라고 명시하여 정답 추출의 정확도와 안정성을 극대화했습니다.

- 논리적 단계의 명시성: "Show clear logical steps"라는 표현을 사용하여 모델이 단순한 수식 나열을 넘어 인과관계가 명확한 추론을 수행하도록 압박하였으며, 이것이 5-shot에서 0.88이라는 최고 성능을 달성한 주요 원인으로 분석됩니다.
