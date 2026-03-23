import streamlit as st
import uuid
import random
import pandas as pd
import time
from datetime import datetime
import urllib.parse
import gspread
# from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2.service_account import Credentials
# =========================
# 페이지 설정
# =========================
st.set_page_config(page_title="ScholarSelect", layout="centered")


# =========================
# 스타일
# =========================
st.markdown("""
<style>
/* 전체 여백 */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 820px;
}

/* 상단 브랜드 */
.top-brand {
    font-size: 34px;
    font-weight: 700;
    line-height: 1.2;
    margin-top: 4px;
    margin-bottom: 16px;
    color: #1f2937;
    letter-spacing: -0.5px;
    display: flex;
    align-items: flex-start;
    gap: 8px;
}

.ai-inline {
    font-size: 11px;
    color: #9ca3af;
    font-weight: 700;
    letter-spacing: 1px;
    margin-top: 6px;
}

.title {
    font-size: 34px;
    font-weight: 700;
    line-height: 1.2;
    margin-top: 4px;
    margin-bottom: 16px;
    color: #1f2937;
    letter-spacing: -0.5px;
    display: flex;
    align-items: flex-start;
    gap: 8px;
}

.brand-accent {
    color: #6b7280;
    margin-left: 2px;
}

.top-status {
    text-align: right;
    font-size: 14px;
    color: #6b7280;
    margin-top: 14px;
}

.ai-label {
    font-size: 12px;
    color: #6b7280;
    font-weight: 600;
    letter-spacing: 1px;
    margin-bottom: -6px;
}            

            
.search-subtitle {
    font-size: 12px;
    color: #8a93a0;
    margin-bottom: 12px;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

/* 논문 블록 */
.paper-block {
    padding: 16px 0 22px 0;
    border-bottom: 1px solid #d9dde3;
    margin-bottom: 6px;
}

.paper-title {
    font-size: 22px;
    font-weight: 700;
    color: #1f2937;
    margin-top: 0;
    margin-bottom: 6px;
    line-height: 1.35;
}

.paper-citation {
    font-size: 14px;
    color: #5f6b7a;
    margin-bottom: 10px;
    line-height: 1.5;
}

.abstract-row {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    margin-bottom: 10px;
}

.abstract-label {
    min-width: 58px;
    font-size: 13px;
    font-weight: 700;
    color: #4b5563;
    padding-top: 2px;
}

.abstract-text {
    flex: 1;
    font-size: 15px;
    color: #374151;
    line-height: 1.65;
}

.meta-chip {
    display: inline-block;
    font-size: 12px;
    color: #6b7280;
    background: #f3f4f6;
    padding: 4px 8px;
    border-radius: 999px;
    margin-right: 6px;
    margin-bottom: 10px;
}

/* 버튼 */
.stButton > button {
    padding: 1px 8px;
    font-size: 11px;
    height: 26px;
    border-radius: 999px;
}

/* XAI */
.xai-item {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    margin-top: 8px;
}

.xai-item:first-child {
    margin-top: 0;
}

.xai-icon {
    width: 20px;
    flex-shrink: 0;
    font-size: 14px;
    line-height: 1.6;
}

.xai-content {
    flex: 1;
    font-size: 14px;
    color: #4b5563;
    line-height: 1.6;
}

.xai-tag {
    font-weight: 700;
    color: #374151;
    margin-right: 6px;
}

.xai-title {
    font-size: 13px;
    font-weight: 700;
    color: #374151;
    margin-top: 8px;
    margin-bottom: 4px;
}

.xai-box {
    background: #f8fafc;
    border: 1px solid #e5e7eb;
    border-radius: 10px;
    padding: 10px 14px;
    margin-top: 2px;
    margin-bottom: 12px;
}

/* footer */
.footer-meta {
    font-size: 11px;
    color: #b0b8c1;
    opacity: 0.8;
    text-align: center;
    margin-top: 8px;
}
            
.instruction-text {
    font-size: 14px;
    color: #4b5563;
    margin-top: 6px;
    margin-bottom: 16px;
    line-height: 1.6;
}

.search-box {
    border: 1px solid #d1d5db;
    border-radius: 24px;
    padding: 10px 16px;
    display: flex;
    align-items: center;
    gap: 8px;
    background-color: #ffffff;
    margin-bottom: 14px;
}

.search-icon {
    color: #9ca3af;
    font-size: 14px;
}

.search-text {
    font-size: 15px;
    color: #111827;
}

</style>
""", unsafe_allow_html=True)





# =========================
# 논문 데이터
# =========================
# relevance_level은 임시 배정값이야. 나중에 다시 조정하면 됨.
papers = [
{
    "id": 1,
    "title": "수면이 인간의 기억 공고화에 미치는 영향",
    "author": "김민서 외",
    "year": 2023,
    "venue": "한국인지과학회",
    "keywords": ["수면", "기억 공고화", "기억", "학습"],
    "abstract": "본 연구는 수면이 학습 이후 기억 공고화 과정에 미치는 영향을 실험적으로 검증하였다. 대학생 92명을 대상으로 단어쌍 학습 과제를 수행하게 한 후, 수면 집단과 수면 제한 집단으로 나누어 24시간 후 회상 및 재인 과제를 실시하였다. 분석 결과, 수면 집단은 수면 제한 집단에 비해 유의미하게 높은 회상 정확도와 재인 수행을 보였으며(p < .01), 특히 수면의 질이 높은 참가자일수록 기억 유지율이 더 높게 나타났다. 또한 수면 시간과 기억 수행 간에는 정적 상관관계가 확인되었다(r = .42). 이러한 결과는 수면이 단순한 휴식 상태를 넘어 학습된 정보의 안정화 및 재구성 과정에 적극적으로 기여함을 시사한다. 본 연구는 수면 조건이 기억 공고화의 핵심 변수로 작용함을 실험적으로 확인하였다는 점에서 의의를 가진다.",
    "xai_query": "수면과 기억 형성의 관계를 다루는 연구",
    "xai_position": "학습 이후 기억 변화에 초점을 둔 연구 흐름에 위치하며, 비교적 최근에 발표된 연구",
    "xai_contribution": "학습 이후 수면 여부와 수면 조건에 따른 기억 수행을 비교하도록 설계된 연구",
    "relevance_level": "high"
},

{
    "id": 2,
    "title": "학습과 기억에서 수면의 역할: 신경인지적 관점",
    "author": "박지훈 외",
    "year": 2021,
    "venue": "인지심리연구",
    "keywords": ["수면", "학습", "기억", "신경인지"],
    "abstract": "본 연구는 학습과 기억 과정에서 수면이 수행하는 역할을 신경인지적 관점에서 분석하였다. 대학생 88명을 대상으로 학습 과제 수행 후 수면 데이터를 수집하고, 다음 날 기억 재인 및 개념 이해 과제를 실시하였다. 연구 결과, 수면 시간이 충분한 집단은 재인 정확도뿐만 아니라 개념 이해 수준에서도 유의미하게 높은 점수를 보였다(p < .05). 특히 REM 수면 비율이 높은 참가자일수록 추상적 개념 이해 과제에서 더 높은 수행을 보였다. 이는 수면이 단순한 기억 유지뿐 아니라 정보의 통합 및 재구성 과정에도 기여함을 의미한다. 본 연구는 수면이 기억의 질적 변화와 학습 내용의 심층 처리에 중요한 역할을 한다는 점을 실증적으로 제시하였다.",
    "xai_query": "수면과 학습 및 기억의 관계를 직접 다루는 연구",
    "xai_position": "기억 유지뿐 아니라 학습된 정보의 처리 과정까지 함께 다루는 연구 흐름에 위치",
    "xai_contribution": "수면 기록과 학습 이후 수행을 함께 비교하도록 설계된 연구",
    "relevance_level": "high"
},

{
    "id": 3,
    "title": "수면 의존적 기억 공고화와 학습 수행에 미치는 영향",
    "author": "이서연 외",
    "year": 2023,
    "venue": "학습과기억",
    "keywords": ["수면", "기억 공고화", "학습 수행", "기억"],
    "abstract": "본 연구는 수면 의존적 기억 공고화가 학습 수행에 미치는 영향을 다각적으로 분석하였다. 참가자들은 읽기 학습과 연상 기억 과제를 수행한 후 수면 집단과 각성 유지 집단으로 구분되었으며, 이후 지연 회상 및 적용 과제를 수행하였다. 결과적으로 수면 집단은 단순 기억 과제뿐 아니라 학습 내용의 응용 능력에서도 유의미하게 높은 수행을 보였다(p < .01). 특히 수면 이후 수행된 과제에서 정보의 전이 및 일반화 능력이 향상되는 경향이 확인되었다. 이는 수면이 단순 저장이 아닌 기억 구조의 재조직화 과정에 관여함을 시사한다. 본 연구는 기억 공고화와 학습 수행 간의 연결성을 실험적으로 입증하였다.",
    "xai_query": "수면과 기억 공고화 및 학습 수행의 관계를 직접 다루는 연구",
    "xai_position": "기억 변화와 학습 수행을 함께 고려하는 연구 흐름에 위치하며, 비교적 최근에 발표된 연구",
    "xai_contribution": "수면 이후 기억 유지와 학습 수행 양상을 함께 비교하도록 설계된 연구",
    "relevance_level": "high"
},

{
    "id": 4,
    "title": "수면 부족이 주의집중과 인지 수행에 미치는 영향",
    "author": "정유진 외",
    "year": 2022,
    "venue": "행동과학연구",
    "keywords": ["수면 부족", "주의집중", "인지 수행", "수행"],
    "abstract": "본 연구는 수면 부족이 주의집중과 인지 수행에 미치는 영향을 분석하였다. 대학생 104명을 대상으로 정상 수면 집단과 수면 부족 집단을 구성하고 선택적 주의 과제와 작업 수행 과제를 실시하였다. 분석 결과, 수면 부족 집단은 반응 시간 증가, 오류율 증가, 과제 지속력 감소를 보였으며(p < .01), 특히 장시간 집중이 요구되는 과제에서 수행 저하가 두드러졌다. 또한 주의 전환 과제에서 유의미한 성능 저하가 나타났다. 이러한 결과는 수면 부족이 단순 피로를 넘어 인지 자원의 효율적 분배에 영향을 미친다는 점을 시사한다. 본 연구는 수면 부족이 고차원적 인지 수행에 미치는 부정적 영향을 정량적으로 제시하였다.",
    "xai_query": "수면 상태와 인지 수행의 관계를 다루는 연구",
    "xai_position": "학습 및 기억과 간접적으로 연결되는 주의집중과 인지 수행 변화에 초점을 둔 연구",
    "xai_contribution": "수면 부족 여부에 따른 주의집중 및 수행 양상을 비교하도록 설계된 연구",
    "relevance_level": "medium"
},

{
    "id": 5,
    "title": "수면과 인지 수행: 주의집중 및 실행기능에 미치는 영향",
    "author": "최다은 외",
    "year": 2021,
    "venue": "교육심리리뷰",
    "keywords": ["수면", "인지 수행", "주의집중", "실행기능"],
    "abstract": "본 연구는 수면이 주의집중과 실행기능에 미치는 영향을 분석하였다. 대학생 96명을 대상으로 수면 시간과 수면의 질을 측정한 뒤, 과제 전환, 주의 통제, 계획 수행 과제를 수행하도록 하였다. 결과적으로 수면 시간이 충분한 집단은 실행기능 관련 과제에서 더 높은 정확도와 빠른 반응 속도를 보였다(p < .05). 특히 수면의 질이 낮은 경우 계획 수행 능력이 유의미하게 저하되는 것으로 나타났다. 이는 수면이 기억뿐 아니라 고차 인지 기능에도 중요한 영향을 미친다는 점을 시사한다. 본 연구는 수면과 실행기능 간의 관계를 실험적으로 확인하였다는 점에서 의의를 가진다.",
    "xai_query": "수면과 인지 수행의 관계를 다루는 연구",
    "xai_position": "기억 자체보다 주의집중과 실행기능 같은 인지 수행 변화에 초점을 둔 연구",
    "xai_contribution": "수면 조건에 따라 여러 인지 기능의 수행 양상을 비교하도록 설계된 연구",
    "relevance_level": "medium"
},

{
    "id": 6,
    "title": "수면의 질이 과제 수행과 인지 효율에 미치는 영향",
    "author": "한지민 외",
    "year": 2022,
    "venue": "인지와학습",
    "keywords": ["수면의 질", "과제 수행", "인지 효율", "수면"],
    "abstract": "본 연구는 수면의 질이 과제 수행과 인지 효율에 미치는 영향을 분석하였다. 대학생 112명을 대상으로 자기보고식 수면 질 척도와 수행 데이터를 수집하고, 정보 탐색 및 주의집중 과제를 수행하도록 하였다. 분석 결과, 수면의 질이 높은 집단은 과제 수행 속도와 정확도 모두에서 우수한 결과를 보였으며(p < .01), 오류 패턴 또한 더 안정적인 경향을 보였다. 특히 낮은 수면 질을 보인 참가자들은 수행 일관성이 떨어지고 반응 변동성이 증가하였다. 이러한 결과는 수면의 질이 인지 효율과 직접적으로 관련됨을 시사한다. 본 연구는 수면의 양뿐 아니라 질 역시 중요한 변수임을 강조한다.",
    "xai_query": "수면의 질과 수행 변화의 관계를 다루는 연구",
    "xai_position": "학습 및 기억 자체보다 과제 수행 효율과 인지적 작업 환경에 초점을 둔 연구",
    "xai_contribution": "수면의 질 수준에 따른 수행 효율과 오류 양상을 비교하도록 설계된 연구",
    "relevance_level": "medium"
},

{
    "id": 7,
    "title": "수면과 학습 과정에서의 수행 효율 변화",
    "author": "윤가영 외",
    "year": 2024,
    "venue": "학습행동연구",
    "keywords": ["수면", "학습 과정", "수행 효율", "행동 과제"],
    "abstract": "본 연구는 수면과 학습 과정에서의 수행 효율 변화 간의 관계를 분석하였다. 대학생 84명을 대상으로 개념 학습 및 문제 해결 과제를 수행하게 한 후 수면 시간에 따른 수행 변화를 측정하였다. 결과적으로 충분한 수면을 취한 집단은 학습 속도와 문제 해결 정확도 모두에서 유의미하게 높은 수행을 보였다(p < .05). 특히 복잡한 문제 해결 과제에서 수면의 효과가 더 크게 나타났다. 이는 수면이 학습 과정에서의 정보 처리 효율을 향상시키는 역할을 한다는 점을 시사한다. 본 연구는 학습 과정에서 수면의 중요성을 행동적 지표를 통해 확인하였다.",
    "xai_query": "수면과 학습 과정의 관계를 다루는 연구",
    "xai_position": "기억 유지보다 학습 과정에서 나타나는 수행 효율 변화에 초점을 뒀으며 비교적 최근에 발표된 연구",
    "xai_contribution": "수면 조건에 따라 학습 과제 수행의 속도와 정확도를 비교하도록 설계된 연구",
    "relevance_level": "medium"
},

{
    "id": 8,
    "title": "수면 조건에 따른 주의집중 및 수행 변화",
    "author": "오세린 외",
    "year": 2021,
    "venue": "기억연구",
    "keywords": ["수면 조건", "주의집중", "수행 변화", "인지 수행"],
    "abstract": "본 연구는 수면 조건에 따른 주의집중 및 수행 변화를 분석하였다. 대학생 100명을 대상으로 수면 시간과 취침 일관성을 기준으로 집단을 나누고 집중 지속 과제를 수행하게 하였다. 결과적으로 수면이 불규칙한 집단은 반응 지연과 수행 변동성이 증가하는 경향을 보였으며(p < .05), 과제 지속 시간 또한 짧게 나타났다. 반면 일정한 수면 패턴을 유지한 집단은 안정적인 수행을 보였다. 이는 수면의 규칙성이 인지 수행 안정성에 중요한 역할을 한다는 점을 시사한다.",
    "xai_query": "수면 조건과 인지 수행의 관계를 다루는 연구",
    "xai_position": "학습 및 기억과 간접적으로 연결되는 주의집중과 수행 안정성 변화에 초점을 둔 연구",
    "xai_contribution": "수면 조건에 따라 정확도와 수행 안정성 양상을 비교하도록 설계된 연구",
    "relevance_level": "medium"
},

{
    "id": 9,
    "title": "수면 제한 상황에서 반응시간 변동성 분석",
    "author": "송예린 외",
    "year": 2021,
    "venue": "정서심리학회지",
    "keywords": ["수면 제한", "반응시간", "변동성", "수행"],
    "abstract": "본 연구는 수면 제한 상황에서 반응시간 변동성을 분석하였다. 대학생 90명을 대상으로 수면 제한 집단과 정상 수면 집단을 구성하고 반응 과제를 수행하게 하였다. 분석 결과, 평균 반응시간 자체보다 반응시간의 변동성이 수면 제한 조건에서 유의미하게 증가하였다(p < .01). 이는 수행의 일관성이 저하됨을 의미하며, 인지적 안정성이 감소했음을 시사한다. 본 연구는 수면 부족이 수행 품질의 미세한 변동성에도 영향을 미친다는 점을 강조한다.",
    "xai_query": "수면 제한과 기초 수행 지표의 관계를 다루는 연구",
    "xai_position": "학습 및 기억보다 반응시간 같은 기초 수행 변화에 초점을 둔 연구이며, 이 주제의 주변부에 위치한 연구",
    "xai_contribution": "수면 제한 조건에서 반응시간의 변동성과 일관성을 비교하도록 설계된 연구",
    "relevance_level": "low"
},

{
    "id": 10,
    "title": "수면 부족이 인간의 생리적 및 수행 능력에 미치는 영향",
    "author": "조현우 외",
    "year": 2021,
    "venue": "디지털행동연구",
    "keywords": ["수면 부족", "생리 반응", "수행 능력", "수면"],
    "abstract": "본 연구는 수면 부족이 생리적 반응과 전반적 수행 능력에 미치는 영향을 분석하였다. 대학생 108명을 대상으로 수면 부족 조건과 정상 수면 조건을 비교하였다. 결과적으로 수면 부족 집단은 심박수 증가, 피로도 상승, 수행 정확도 감소를 보였으며(p < .01), 특히 장시간 과제에서 수행 저하가 크게 나타났다. 이는 수면 부족이 생리적 스트레스와 인지 수행 저하를 동시에 유발함을 시사한다. 본 연구는 수면 부족의 복합적 영향을 통합적으로 분석하였다.",
    "xai_query": "수면 부족과 전반적 신체 및 수행 변화의 관계를 다루는 연구",
    "xai_position": "학습 및 기억보다 생리적 반응과 일반 수행 능력 변화에 초점을 둔 연구이며, 상대적으로 넓은 범주의 수행 연구에 위치",
    "xai_contribution": "수면 부족 조건에서 생리 반응과 수행 능력 양상을 함께 비교하도록 설계된 연구",
    "relevance_level": "low"
}

]


def highlight_keywords(text, keywords=["수면", "학습", "기억"]):
    for kw in keywords:
        text = text.replace(
            kw,
            f"<span style='background-color:#e5e7eb; padding:1px 3px; border-radius:4px; font-weight:500;'>{kw}</span>"
        )
    return text



##정해진 패턴이 랜덤으로 
def build_balanced_paper_order(papers):
    paper_dict = {p["id"]: p for p in papers}

    patterns = [
        [7, 1, 4, 9, 5, 2, 6, 10, 8, 3],   # Pattern A
        [4, 7, 9, 1, 5, 2, 10, 6, 3, 8],   # Pattern B
        [5, 1, 7, 9, 4, 2, 10, 8, 6, 3],   # Pattern C
    ]

    selected_pattern = random.choice(patterns)
    ordered_papers = [paper_dict[i] for i in selected_pattern]

    return ordered_papers, selected_pattern










# =========================
# Preview 생성 함수
# =========================
def make_preview(text, limit=140):
    if len(text) <= limit:
        return text
    return text[:limit] + "..."

def save_log(data_dict):
    sheet = get_sheet()
    row = [
        str(data_dict.get("user_id", "")),
        str(data_dict.get("condition", "")),
        str(data_dict.get("selected", "")),
        str(data_dict.get("unique_docs_viewed", "")),
        str(data_dict.get("abstract_views", "")),
        str(data_dict.get("abstract_click_log", "")),
        str(data_dict.get("abstract_click_total", "")),
        str(data_dict.get("selected_viewed_status", "")),
        str(data_dict.get("revisit_count", "")),
        str(data_dict.get("time_to_first_selection", "")),
        str(data_dict.get("total_time_spent", "")),
        str(data_dict.get("selected_quality_score", "")),
        str(data_dict.get("selected_scores", "")),
        str(data_dict.get("pattern_used", "")),
        str(data_dict.get("ordered_paper_ids", "")),
        str(data_dict.get("timestamp", "")),
        str(data_dict.get("ui_version", "")),
        str(data_dict.get("click_sequence", "")),
    ]
    sheet.append_row(row)


@st.cache_resource
def get_sheet():
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=scope
    )

    client = gspread.authorize(creds)

    return client.open_by_key(
        st.secrets["sheets"]["spreadsheet_key"]
    ).sheet1

# @st.cache_resource
# def get_sheet():
#     scope = [
#         "https://spreadsheets.google.com/feeds",
#         "https://www.googleapis.com/auth/drive"
#     ]
#     creds = ServiceAccountCredentials.from_json_keyfile_name(
#         "credentials.json", scope
#     )
#     client = gspread.authorize(creds)
#     return client.open_by_key("1mdOw0fGQlVljpoleaAbNIbCRMSZVlzaJDswPDw2asQ0").sheet1

# def save_log(data_dict):
#     row = [str(v) for v in data_dict.values()]
#     sheet.append_row(row)

# =========================
# 상태 초기화
# =========================
if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())[:8]

if "condition" not in st.session_state:
    st.session_state.condition = random.choice(["condition1", "condition2"])

if "selected" not in st.session_state:
    st.session_state.selected = []

if "open_paper_id" not in st.session_state:
    st.session_state.open_paper_id = None

if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

if "first_selection_time" not in st.session_state:
    st.session_state.first_selection_time = None

if "click_log" not in st.session_state:
    st.session_state.click_log = {"select": 0, "remove": 0}

if "viewed_docs" not in st.session_state:
    st.session_state.viewed_docs = set()

if "abstract_clicks" not in st.session_state:
    st.session_state.abstract_clicks = 0

if "abstract_click_log" not in st.session_state:
    st.session_state.abstract_click_log = {}


if "revisit_count" not in st.session_state:
    st.session_state.revisit_count = 0

if "view_history" not in st.session_state:
    st.session_state.view_history = []

if "ordered_papers" not in st.session_state:
    ordered_papers, selected_pattern = build_balanced_paper_order(papers)
    st.session_state.ordered_papers = ordered_papers
    st.session_state.selected_pattern = selected_pattern

if "show_survey_link" not in st.session_state:
    st.session_state.show_survey_link = False

if "click_sequence" not in st.session_state:
    st.session_state.click_sequence = []



# =========================
# Google Sheets 연결
# =========================
# scope = [
#     "https://spreadsheets.google.com/feeds",
#     "https://www.googleapis.com/auth/drive"
# ]

# creds = ServiceAccountCredentials.from_json_keyfile_name(
#     "credentials.json", scope
# )

# client = gspread.authorize(creds)
# # sheet = client.open("streamlit_logs").sheet1


# =========================
# 상단
# =========================
topic_text = "수면이 학습 및 기억에 미치는 영향"

col1, col2 = st.columns([4, 1])

with col1:
    st.markdown("""
    <div class="top-brand">
        Scholar<span class="brand-accent">Select</span>
        <span class="ai-inline">AI</span>
    </div>
    """, unsafe_allow_html=True)




with col2:
    st.markdown(
        f"""
        <div class="top-status">
            선택 완료: <strong>{len(st.session_state.selected)} / 2</strong>
        </div>
        """,
        unsafe_allow_html=True
    )




# 지시사항
st.markdown("""
<div style="font-size:13px; color:#6b7280; line-height:1.65; margin-top:6px; margin-bottom:26px;">
    AI가 질의와의 관련성을 바탕으로 추천한 검색결과입니다.<br>
    아래 문헌 중 검색어와 가장 관련성이 높다고 판단되는 
    <span style="background-color:#fef3c7; padding:2px 6px; border-radius:6px; font-weight:600;">
        논문 2편
    </span>
    을 선택(select)하세요.<br>
    <span style="color:#9ca3af;">
        선택 후 간단한 설문이 가장 아래에 위치해있습니다.
    </span>
</div>
""", unsafe_allow_html=True)

# 검색어 박스
st.markdown(f"""
<div style="
    border: 1px solid #d1d5db;
    border-radius: 24px;
    padding: 10px 16px;
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 18px;
    background-color: #ffffff;
">
    <span style="color:#9ca3af; font-size:14px;">🔍</span>
    <span style="font-size:15px; color:#111827;">
        {topic_text}
    </span>
</div>
""", unsafe_allow_html=True)

# 구분선 + SEARCH RESULTS
st.markdown("""
<div style="border-top:1px solid #e5e7eb; margin-top:2px; margin-bottom:14px;"></div>
<div class="search-subtitle" style="margin-bottom:0px;">Search results</div>
""", unsafe_allow_html=True)

# =========================
# 선택 질 점수용 relevance 사전
# =========================
relevance_score_map = {
    1: 2,  # medium
    2: 2,  # medium
    3: 3,  # high
    4: 1,  # low
    5: 2,  # medium
    6: 2,  # medium
    7: 2,  # medium
    8: 3,  # high
    9: 1,  # low
    10: 3, # high
}

# =========================
# 논문 렌더링 함수
# =========================
def render_paper_semantic(paper, idx):
    is_selected = paper["id"] in st.session_state.selected
    is_open = st.session_state.open_paper_id == paper["id"]

    st.markdown('<div class="paper-block">', unsafe_allow_html=True)

    st.markdown(f'<div class="paper-title">{paper["title"]}</div>', unsafe_allow_html=True)

    st.markdown(
        f'<div class="paper-citation">{paper["author"]} · {paper["year"]} · {paper["venue"]}</div>',
        unsafe_allow_html=True
    )

    keyword_html = ""
    for kw in paper["keywords"]:
        keyword_html += f'<span class="meta-chip">{kw}</span>'
    st.markdown(keyword_html, unsafe_allow_html=True)

    preview_abs = make_preview(paper["abstract"], limit=140)
    display_abs = paper["abstract"] if is_open else preview_abs

    abs_col1, abs_col2 = st.columns([8, 1])

    with abs_col1:
        st.markdown(
            f"""
            <div class="abstract-row">
                <div class="abstract-label">Abstract</div>
                <div class="abstract-text">{display_abs}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with abs_col2:
        if st.button(
            "More" if not is_open else "Less",
            key=f"abs_btn_{paper['id']}"
        ):
            if is_open:
                st.session_state.open_paper_id = None
            else:
                paper_id = paper["id"]
                st.session_state.open_paper_id = paper_id
                st.session_state.abstract_clicks += 1

                # 논문별 abstract 클릭 로그
                if paper_id not in st.session_state.abstract_click_log:
                    st.session_state.abstract_click_log[paper_id] = 0
                st.session_state.abstract_click_log[paper_id] += 1

                # #로그 
                # save_log({
                #     "user_id": st.session_state.user_id,
                #     "action": "abstract_click",
                #     "paper_id": paper_id,
                #     "timestamp": datetime.now()
                # })

                if paper_id in st.session_state.view_history:
                    st.session_state.revisit_count += 1

                st.session_state.view_history.append(paper_id)
                st.session_state.viewed_docs.add(paper_id)

            st.rerun()

    if st.session_state.condition == "condition1":
        st.markdown(
            '<div class="xai-title">AI 추천 근거</div>',
            unsafe_allow_html=True
        )

        xai_html = (
            '<div class="xai-box">'
            '<div class="xai-item">'
            '<div class="xai-icon">🔎</div>'
            '<div class="xai-content">'
            '<span class="xai-tag">검색어 관련</span>'
            f'{highlight_keywords(paper["xai_query"])}'
            # f'{paper["xai_query"]}'
            '</div>'
            '</div>'

            '<div class="xai-item">'
            '<div class="xai-icon">📍</div>'
            '<div class="xai-content">'
            '<span class="xai-tag">연구 위치</span>'
            f'{highlight_keywords(paper["xai_position"])}'
            '</div>'
            '</div>'

            '<div class="xai-item">'
            '<div class="xai-icon">🧩</div>'
            '<div class="xai-content">'
            '<span class="xai-tag">연구 특징</span>'
            f'{highlight_keywords(paper["xai_contribution"])}'
            '</div>'
            '</div>'
            '</div>'
        )

        st.markdown(xai_html, unsafe_allow_html=True)

    select_label = "✓ Selected" if is_selected else "Select"
    if st.button(
        select_label,
        key=f"select_{paper['id']}",
        use_container_width=False,
        type="secondary"
    ):
        st.session_state.show_survey_link = False

        if is_selected:
            st.session_state.click_log["remove"] += 1
            st.session_state.selected.remove(paper["id"])
        else:
            if len(st.session_state.selected) < 2:
                if st.session_state.first_selection_time is None:
                    st.session_state.first_selection_time = time.time()

                st.session_state.click_log["select"] += 1
                st.session_state.selected.append(paper["id"])
                st.session_state.click_sequence.append(paper["id"])

        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
    # select_label = "✓ Selected" if is_selected else "Select"
    # if st.button(
    #     select_label,
    #     key=f"select_{paper['id']}",
    #     use_container_width=False,
    #     type="secondary"
    # ):
    #     st.session_state.show_survey_link = False

    #     if is_selected:
    #         st.session_state.click_log["remove"] += 1
    #         st.session_state.selected.remove(paper["id"])
    #     else:
    #         if len(st.session_state.selected) < 2:
    #             if st.session_state.first_selection_time is None:
    #                 st.session_state.first_selection_time = time.time()

    #             st.session_state.click_log["select"] += 1
    #             st.session_state.selected.append(paper["id"])

    #     st.rerun()

    # st.markdown('</div>', unsafe_allow_html=True)

# =========================
# 논문 출력
# =========================
for i, paper in enumerate(st.session_state.ordered_papers):
    render_paper_semantic(paper, i)


# =========================
# Next Step (Google Form 연결)
# =========================

# 최초 1회 초기화
if "show_survey_link" not in st.session_state:
    st.session_state.show_survey_link = False

if "survey_saved" not in st.session_state:
    st.session_state.survey_saved = False

user_id = st.session_state.user_id
condition = st.session_state.condition

if condition == "condition1":
    condition_value = "condition1"
else:
    condition_value = "condition2"

condition_value = urllib.parse.quote(condition_value)
user_id_encoded = urllib.parse.quote(user_id)

form_url = (
    "https://docs.google.com/forms/d/e/1FAIpQLSeA6iffUfXBeiyMlmLNNEqynSWUWzd2GXd02i1Biypj0Lgq-w/viewform"
    f"?usp=pp_url&entry.5305845={user_id_encoded}"
    f"&entry.897886053={condition_value}"
)

selection_status_text = f"선택 완료: {len(st.session_state.selected)} / 2"

st.markdown(
    f"""
    <div style="font-size:14px; color:#374151; margin-top:18px; margin-bottom:8px; font-weight:600;">
        {selection_status_text}
    </div>
    """,
    unsafe_allow_html=True
)

if len(st.session_state.selected) < 2:
    st.markdown(
        """
        <div style="font-size:13px; color:#b45309; margin-bottom:10px;">
            설문으로 이동하기 전에 논문 2편을 선택해주세요.
        </div>
        """,
        unsafe_allow_html=True
    )

else:
    # 아직 저장 안 된 경우에만 저장 버튼 표시
    if not st.session_state.survey_saved:
        if st.button("설문 응답 저장 후 이동", key="save_and_go_survey"):
            end_time = time.time()

            time_to_first_selection = None
            if st.session_state.first_selection_time is not None:
                time_to_first_selection = (
                    st.session_state.first_selection_time - st.session_state.start_time
                )

            selected_scores = [relevance_score_map[p] for p in st.session_state.selected]
            selected_quality_score = (
                sum(selected_scores) / len(selected_scores) if selected_scores else None
            )

            data = {
                "user_id": st.session_state.user_id,
                "condition": st.session_state.condition,
                "selected": str(st.session_state.selected),
                "unique_docs_viewed": len(st.session_state.viewed_docs),
                "abstract_views": st.session_state.abstract_clicks,
                "abstract_click_log": str(st.session_state.abstract_click_log),
                "abstract_click_total": sum(st.session_state.abstract_click_log.values()),
                "selected_viewed_status": str({
                    pid: (pid in st.session_state.viewed_docs)
                    for pid in st.session_state.selected
                }),
                "revisit_count": st.session_state.revisit_count,
                "time_to_first_selection": time_to_first_selection,
                "total_time_spent": end_time - st.session_state.start_time,
                "selected_quality_score": selected_quality_score,
                "selected_scores": str(selected_scores),
                "pattern_used": str(st.session_state.selected_pattern),
                "ordered_paper_ids": str([p["id"] for p in st.session_state.ordered_papers]),
                "timestamp": datetime.now(),
                "ui_version": "semantic_single_open_balanced_order",
                "click_sequence": str(st.session_state.click_sequence)
            }

            df = pd.DataFrame([data])

            try:
                existing = pd.read_csv("results_semantic.csv")
                df = pd.concat([existing, df], ignore_index=True)
            except Exception:
                pass

            df.to_csv("results_semantic.csv", index=False)

            # Google Sheets에도 저장
            try:
                save_log(data)
                st.success("Google Sheets 저장 성공")
            except Exception as e:
                st.error(f"Google Sheets 저장 실패: {e}")

            # 저장 완료 표시
            st.session_state.survey_saved = True
            st.session_state.show_survey_link = True
            st.rerun()

    # 저장 완료 후에는 링크 버튼만 보여주기
    if st.session_state.show_survey_link:
        st.success("선택 결과가 저장되었습니다. 아래 버튼을 눌러 설문으로 이동해주세요.")

        st.markdown("### Next Step")
        st.markdown("다음의 설문을 완료해주세요. (예상 소요시간 5분)")

        st.link_button("👉 Go to Survey", form_url)









