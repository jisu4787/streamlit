import streamlit as st
import uuid
import random
import pandas as pd
import time
from datetime import datetime
import urllib.parse
import gspread
import re

QUERY_KEYWORDS = ["수면", "학습", "기억", "영향"]  # 필요하면 수정


# from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2.service_account import Credentials
# =========================
# 페이지 설정
# =========================
st.set_page_config(page_title="ScholarSelect", layout="centered")


#사이드바 수정위한 시도 - 주석처리
st.markdown("""
<style>
    /* 사이드바 전체 레이아웃 설정 */
    section[data-testid="stSidebar"] > div:first-child {
        display: flex;
        flex-direction: column;
        height: 100vh;
    }

    /* 사이드바 리스트 영역 (스크롤 가능) */
    .sidebar-scroll-area {
        flex: 1;
        overflow-y: auto;
        padding-bottom: 20px;
    }

    /* 사이드바 하단 고정 영역 */
    .sidebar-fixed-footer {
        padding: 15px;
        border-top: 1px solid #e5e7eb;
        background-color: white;
    }

    /* 선택 취소 버튼: 얇고 빨간색 스타일 */
    .stButton > button.btn-cancel {
        width: 100% !important;
        height: 28px !important;
        background-color: #ff4d4f !important;
        color: white !important;
        border: none !important;
        font-size: 11px !important;
        border-radius: 4px !important;
        margin-top: 4px !important;
    }

    /* 안내 문구 스타일 */
    .sidebar-guide {
        font-size: 12px;
        color: #6b7280;
        text-align: center;
        margin-bottom: 10px;
        line-height: 1.4;
    }
</style>
""", unsafe_allow_html=True)


##style 합치기를 위해 주석처리
st.markdown("""
<style>
    /* 사이드바 내의 모든 버튼 스타일 수정 */
    section[data-testid="stSidebar"] .stButton button {
        white-space: normal !important;      /* 줄바꿈 허용 */
        height: auto !important;            /* 높이 자동 조절 */
        width: 100% !important;             /* 가로 꽉 차게 */
        text-align: left !important;        /* 왼쪽 정렬 */
        padding: 8px 12px !important;       /* 여백 조절 */
        line-height: 1.3 !important;        /* 줄간격 */
        font-size: 13px !important;         /* 폰트 크기 */
        margin-bottom: 5px !important;
        display: block !important;
    }
</style>
""", unsafe_allow_html=True)



# =========================
# 스타일
# =========================
###style합치기를 위한 주석처리 
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
    font-size: 18px;
    font-weight: 500;
    color: #202124;
    line-height: 1.45;
    margin-bottom: 6px;
}

.paper-title strong {
    font-weight: 600;
}            
            
# .paper-title {
#     font-size: 22px;
#     font-weight: 700;
#     color: #1f2937;
#     margin-top: 0;
#     margin-bottom: 6px;
#     line-height: 1.35;
# }

.paper-citation {
    font-size: 13px;
    color: #6b7280;
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

# /* XAI */

# .xai-content {
#     flex: 1;
#     font-size: 14px;
#     color: #374151;
#     line-height: 1.7;
# }

 
# .xai-box {
#     background: #f8fafc;
#     border: 1px solid #e5e7eb;
#     border-radius: 10px;
#     padding: 12px 16px;
#     margin-top: 6px;
#     margin-bottom: 12px;
# }
            
            
# /*xai수정하면서 새로운css*/
# .xai-box {
#     background-color: #f6f7fb;
#     border: 1px solid #d9deea;
#     border-radius: 10px;
#     padding: 14px 16px;
#     margin-top: 10px;
#     margin-bottom: 8px;
# }

# .xai-title {
#     font-size: 0.95rem;
#     font-weight: 600;
#     margin-bottom: 8px;
#     color: #2f3a56;
# }

# .xai-text {
#     font-size: 0.92rem;
#     line-height: 1.6;
#     color: #222;            

# ##xai추천근거 헤더-유지할지 고민##
# .xai-header {
#     font-size: 13px;
#     font-weight: 600;
#     color: #374151;
#     margin-bottom: 6px;
# }

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
            
            
            
/* 선택 버튼 전체 영역 */
.sidebar-select-btn button {
    height: 30px !important;
    font-size: 12px !important;
    padding: 2px 8px !important;
    border-radius: 6px !important;
}

/* 선택 안 된 상태 (secondary) */
.sidebar-select-btn button[kind="secondary"] {
    background-color: #f3f4f6 !important;
    color: #374151 !important;
    border: 1px solid #e5e7eb !important;
}

/* 선택된 상태 (primary) */
.sidebar-select-btn button[kind="primary"] {
    background-color: #2563eb !important;
    color: white !important;
}

/* 버튼 간 간격 */
.sidebar-select-btn {
    margin-top: 4px;
    margin-bottom: 8px;
}

/* --- XAI 통합 디자인 스타일 --- */
.xai-container {
    background-color: #f8faff !important;
    border: 1px solid #e0e6ed !important;
    border-radius: 12px !important;
    padding: 18px !important;
    margin: 15px 0 !important;
    box-shadow: 0 2px 4px rgba(0,0,0,0.02);
}
.xai-header-title {
    font-size: 16px !important;
    font-weight: 700 !important;
    color: #1a237e !important;
    margin-bottom: 12px !important;
    border-bottom: 2px solid #eef2f7;
    padding-bottom: 8px;
}
.xai-row {
    display: flex !important;
    padding: 10px 0 !important;
    align-items: flex-start !important;
}
.xai-label {
    flex: 0 0 150px !important; /* 라벨 너비 고정 */
    font-size: 13px !important;
    font-weight: 700 !important;
    color: #4a5568 !important;
}
.xai-body {
    flex: 1 !important;
    font-size: 14px !important;
    color: #2d3748 !important;
    line-height: 1.6 !important;
}
            
.chip-blue { background: #e0f2f1; color: #00796b; padding: 2px 8px; border-radius: 6px; font-weight: 600; font-size: 12px; }
.chip-purple { background: #ede7f6; color: #5e35b1; padding: 2px 8px; border-radius: 6px; font-weight: 600; font-size: 12px; }
.chip-red { background: #ffebee; color: #c62828; padding: 2px 8px; border-radius: 6px; font-weight: 600; font-size: 12px; }


</style>
""", unsafe_allow_html=True)





# =========================
# 논문 데이터
# =========================
# relevance_level은 임시 배정값이야. 나중에 다시 조정하면 됨.
papers = [
{
    "id": 1,
    "title": "수면 단계별 인간의 기억 공고화 및 학습 영향 분석",
    "author": "김민서 외",
    "year": 2025,
    "venue": "한국인지과학회",
    "if_score": 3.2,
    "citation_count": 48,
    "keywords": ["수면", "기억 공고화", "기억", "학습"],
    "abstract": "본 연구는 수면이 학습 이후 기억 공고화 과정에 미치는 영향을 실험적으로 검증하였다. 대학생 92명을 대상으로 단어쌍 학습 과제를 수행하게 한 후, 수면 집단과 수면 제한 집단으로 나누어 24시간 후 회상 및 재인 과제를 실시하였다. 분석 결과, 수면 집단은 수면 제한 집단에 비해 유의미하게 높은 회상 정확도와 재인 수행을 보였으며(p < .01), 특히 수면의 질이 높은 참가자일수록 기억 유지율이 더 높게 나타났다. 또한 수면 시간과 기억 수행 간에는 정적 상관관계가 확인되었다(r = .42). 이러한 결과는 수면이 단순한 휴식 상태를 넘어 학습된 정보의 안정화 및 재구성 과정에 적극적으로 기여함을 시사한다. 본 연구는 수면 조건이 기억 공고화의 핵심 변수로 작용함을 실험적으로 확인하였다는 점에서 의의를 가진다.",
    "xai_explanation": "시스템은 '최신성'과 '키워드 일치도'의 합산 점수에 따라 본 문헌을 2위로 판정하였습니다. 만약 <strong>실험 설계의 포괄성</strong> 이 더 넓었다면 순위는 1위로 ▲상승했을 것입니다.",
    "relevance_level": "high"
},

{
    "id": 2,
    "title": "학습과 기억의 근본 원리: 수면의 역할에 대한 신경인지적 메커니즘",
    "author": "박지훈 외",
    "year": 2015,
    "venue": "인지심리연구",
    "if_score": 2.8,
    "citation_count": 91,
    "keywords": ["수면", "학습", "기억", "신경인지"],
    "abstract": "본 연구는 학습과 기억 과정에서 수면이 수행하는 역할을 신경인지적 관점에서 분석하였다. 대학생 88명을 대상으로 학습 과제 수행 후 수면 데이터를 수집하고, 다음 날 기억 재인 및 개념 이해 과제를 실시하였다. 연구 결과, 수면 시간이 충분한 집단은 재인 정확도뿐만 아니라 개념 이해 수준에서도 유의미하게 높은 점수를 보였다(p < .05). 특히 REM 수면 비율이 높은 참가자일수록 추상적 개념 이해 과제에서 더 높은 수행을 보였다. 이는 수면이 단순한 기억 유지뿐 아니라 정보의 통합 및 재구성 과정에도 기여함을 의미한다. 본 연구는 수면이 기억의 질적 변화와 학습 내용의 심층 처리에 중요한 역할을 한다는 점을 실증적으로 제시하였다.",
    "xai_explanation": "본 문헌은 '최신성 가중치 감점' 규칙이 적용되어 4위에 배치되었습니다.만약 <strong>발행 연도가 최근 3년 이내(2023년 이후)였다면</strong>, 내용 적합도 평가에 의해 1위로 ▲상승했을 것입니다.",
    "relevance_level": "high"
},

{
    "id": 3,
    "title": "수면 유도 기억 공고화 기전 분석",
    "author": "이서연 외",
    "year": 2012,
    "venue": "학습과기억",
    "if_score": 3.6,
    "citation_count": 52,
    "keywords": ["수면", "기억 공고화", "학습 수행", "기억"],
    "abstract": "본 연구는 수면 의존적 기억 공고화가 학습 수행에 미치는 영향을 다각적으로 분석하였다. 참가자들은 읽기 학습과 연상 기억 과제를 수행한 후 수면 집단과 각성 유지 집단으로 구분되었으며, 이후 지연 회상 및 적용 과제를 수행하였다. 결과적으로 수면 집단은 단순 기억 과제뿐 아니라 학습 내용의 응용 능력에서도 유의미하게 높은 수행을 보였다(p < .01). 특히 수면 이후 수행된 과제에서 정보의 전이 및 일반화 능력이 향상되는 경향이 확인되었다. 이는 수면이 단순 저장이 아닌 기억 구조의 재조직화 과정에 관여함을 시사한다. 본 연구는 기억 공고화와 학습 수행 간의 연결성을 실험적으로 입증하였다.",
    "xai_explanation": "본 문헌은 '최신성 가중치 감점' 규칙에 의해 5위에 배치되었습니다.만약 <strong>발행 연도가 최근 3년 이내(2023년 이후)였다면</strong>, 주제 연관성 규칙에 의해 2위 이내로 ▲상승했을 것입니다.",
    "relevance_level": "high"
},

{
    "id": 4,
    "title": "수면 부족과 인지 수행: 학습 효율 및 기억력 저하 기전",
    "author": "정유진 외",
    "year": 2023,
    "venue": "행동과학연구",
    "if_score": 2.1,
    "citation_count": 37,
    "keywords": ["수면 부족", "주의집중", "인지 수행", "수행"],
    "abstract": "본 연구는 수면 부족이 주의집중과 인지 수행에 미치는 영향을 분석하였다. 대학생 104명을 대상으로 정상 수면 집단과 수면 부족 집단을 구성하고 선택적 주의 과제와 작업 수행 과제를 실시하였다. 분석 결과, 수면 부족 집단은 반응 시간 증가, 오류율 증가, 과제 지속력 감소를 보였으며(p < .01), 특히 장시간 집중이 요구되는 과제에서 수행 저하가 두드러졌다. 또한 주의 전환 과제에서 유의미한 성능 저하가 나타났다. 이러한 결과는 수면 부족이 단순 피로를 넘어 인지 자원의 효율적 분배에 영향을 미친다는 점을 시사한다. 본 연구는 수면 부족이 고차원적 인지 수행에 미치는 부정적 영향을 정량적으로 제시하였다.",
    "xai_explanation": "시스템은 '키워드 일치도' 규칙을 적용하여 본 문헌을 3위로 판정하였습니다. 만약 <strong>제목에서 '수면' 키워드가 제외되었다면</strong> 순위는 9위권으로 ▼하락했을 것입니다.",
    "relevance_level": "medium"
},

{
    "id": 5,
    "title": "수면과 인지 수행: 주의집중 및 실행기능에 미치는 영향",
    "author": "최다은 외",
    "year": 2021,
    "venue": "교육심리리뷰",
    "if_score": 4.0,
    "citation_count": 76,
    "keywords": ["수면", "인지 수행", "주의집중", "실행기능"],
    "abstract": "본 연구는 수면이 주의집중과 실행기능에 미치는 영향을 분석하였다. 대학생 96명을 대상으로 수면 시간과 수면의 질을 측정한 뒤, 과제 전환, 주의 통제, 계획 수행 과제를 수행하도록 하였다. 결과적으로 수면 시간이 충분한 집단은 실행기능 관련 과제에서 더 높은 정확도와 빠른 반응 속도를 보였다(p < .05). 특히 수면의 질이 낮은 경우 계획 수행 능력이 유의미하게 저하되는 것으로 나타났다. 이는 수면이 기억뿐 아니라 고차 인지 기능에도 중요한 영향을 미친다는 점을 시사한다. 본 연구는 수면과 실행기능 간의 관계를 실험적으로 확인하였다는 점에서 의의를 가진다.",
    "xai_explanation": "본 문헌은 '주제어 일치도' 규칙에 따라 중간 순위인 6위로 판정되었습니다. 만약 <strong>분석 변인에 '기억 공고화'가 포함되었다면</strong> 시스템의 우선순위 규칙에 의해 순위가 ▲상승되었을 것입니다.",
    "relevance_level": "medium"
},

{
    "id": 6,
    "title": "수면의 질이 과제 수행과 인지 효율에 미치는 영향",
    "author": "한지민 외",
    "year": 2022,
    "venue": "인지와학습",
    "if_score": 2.5,
    "citation_count": 29,
    "keywords": ["수면의 질", "과제 수행", "인지 효율", "수면"],
    "abstract": "본 연구는 수면의 질이 과제 수행과 인지 효율에 미치는 영향을 분석하였다. 대학생 112명을 대상으로 자기보고식 수면 질 척도와 수행 데이터를 수집하고, 정보 탐색 및 주의집중 과제를 수행하도록 하였다. 분석 결과, 수면의 질이 높은 집단은 과제 수행 속도와 정확도 모두에서 우수한 결과를 보였으며(p < .01), 오류 패턴 또한 더 안정적인 경향을 보였다. 특히 낮은 수면 질을 보인 참가자들은 수행 일관성이 떨어지고 반응 변동성이 증가하였다. 이러한 결과는 수면의 질이 인지 효율과 직접적으로 관련됨을 시사한다. 본 연구는 수면의 양뿐 아니라 질 역시 중요한 변수임을 강조한다.",
    "xai_explanation": "본 문헌은 '특정 변인(수면의 질)의 명시성' 규칙에 따라 7위에 배치되었습니다. 만약 <strong>분석 데이터가 더 다각화되었다면</strong> 시스템 내 순위는 ▲상승했을 것입니다.",
    "relevance_level": "medium"
},

{
    "id": 7,
    "title": "수면과 학습 과정에서의 수행 효율 변화",
    "author": "윤가영 외",
    "year": 2026,
    "venue": "학습행동연구",
    "if_score": 3.9,
    "citation_count": 14,
    "keywords": ["수면", "학습 과정", "수행 효율", "행동 과제"],
    "abstract": "본 연구는 수면과 학습 과정에서의 수행 효율 변화 간의 관계를 분석하였다. 대학생 84명을 대상으로 개념 학습 및 문제 해결 과제를 수행하게 한 후 수면 시간에 따른 수행 변화를 측정하였다. 결과적으로 충분한 수면을 취한 집단은 학습 속도와 문제 해결 정확도 모두에서 유의미하게 높은 수행을 보였다(p < .05). 특히 복잡한 문제 해결 과제에서 수면의 효과가 더 크게 나타났다. 이는 수면이 학습 과정에서의 정보 처리 효율을 향상시키는 역할을 한다는 점을 시사한다. 본 연구는 학습 과정에서 수면의 중요성을 행동적 지표를 통해 확인하였다.",
    "xai_explanation": "시스템은 '발행 연도의 최신성'을 우선 규칙으로 적용하여 본 문헌을 1위로 판정하였습니다. 만약 <strong>발행 연도가 5년 전이었다면</strong> 시스템 내 순위는 7위 이하로 ▼하락했을 것입니다.",
    "relevance_level": "medium"
},

{
    "id": 8,
    "title": "수면 조건에 따른 주의집중 및 수행 변화",
    "author": "오세린 외",
    "year": 2021,
    "venue": "기억연구",
    "if_score": 2.3,
    "citation_count": 41,
    "keywords": ["수면 조건", "주의집중", "수행 변화", "인지 수행"],
    "abstract": "본 연구는 수면 조건에 따른 주의집중 및 수행 변화를 분석하였다. 대학생 100명을 대상으로 수면 시간과 취침 일관성을 기준으로 집단을 나누고 집중 지속 과제를 수행하게 하였다. 결과적으로 수면이 불규칙한 집단은 반응 지연과 수행 변동성이 증가하는 경향을 보였으며(p < .05), 과제 지속 시간 또한 짧게 나타났다. 반면 일정한 수면 패턴을 유지한 집단은 안정적인 수행을 보였다. 이는 수면의 규칙성이 인지 수행 안정성에 중요한 역할을 한다는 점을 시사한다.",
    "xai_explanation": "본 문헌은 '단일 지표(주의집중) 분석' 규칙이 적용되어 8위로 판정되었습니다. 만약 <strong>종속 변인에 '학습 성취도'가 포함되었다면</strong> 시스템의 관련성 평가 규칙에 의해 순위가 ▲상승했을 것입니다.",
    "relevance_level": "medium"
},

{
    "id": 9,
    "title": "수면 제한 상황에서 반응시간 변동성 분석",
    "author": "송예린 외",
    "year": 2021,
    "venue": "정서심리학회지",
    "if_score": 1.8,
    "citation_count": 18,
    "keywords": ["수면 제한", "반응시간", "변동성", "수행"],
    "abstract": "본 연구는 수면 제한 상황에서 반응시간 변동성을 분석하였다. 대학생 90명을 대상으로 수면 제한 집단과 정상 수면 집단을 구성하고 반응 과제를 수행하게 하였다. 분석 결과, 평균 반응시간 자체보다 반응시간의 변동성이 수면 제한 조건에서 유의미하게 증가하였다(p < .01). 이는 수행의 일관성이 저하됨을 의미하며, 인지적 안정성이 감소했음을 시사한다. 본 연구는 수면 부족이 수행 품질의 미세한 변동성에도 영향을 미친다는 점을 강조한다.",
    "xai_explanation": "본 문헌은 '기초 지표(반응 시간) 위주의 데이터' 판정 규칙에 의해 9위로 배치되었습니다. 만약 <strong>'기억 형성' 데이터가 주요 변인으로 식별되었다면</strong> 순위가 ▲상승했을 것입니다.",
    "relevance_level": "low"
},

{
    "id": 10,
    "title": "수면 부족이 인간의 생리적 및 수행 능력에 미치는 영향",
    "author": "조현우 외",
    "year": 2021,
    "venue": "디지털행동연구",
    "if_score": 2.0,
    "citation_count": 24,
    "keywords": ["수면 부족", "생리 반응", "수행 능력", "수면"],
    "abstract": "본 연구는 수면 부족이 생리적 반응과 전반적 수행 능력에 미치는 영향을 분석하였다. 대학생 108명을 대상으로 수면 부족 조건과 정상 수면 조건을 비교하였다. 결과적으로 수면 부족 집단은 심박수 증가, 피로도 상승, 수행 정확도 감소를 보였으며(p < .01), 특히 장시간 과제에서 수행 저하가 크게 나타났다. 이는 수면 부족이 생리적 스트레스와 인지 수행 저하를 동시에 유발함을 시사한다. 본 연구는 수면 부족의 복합적 영향을 통합적으로 분석하였다.",
    "xai_explanation": "본 문헌은 '광범위한 일반 수행 능력' 판정 규칙에 따라 하위권인 10위로 배치되었습니다. 만약 <strong>인지 기제에 대한 상세 분석 규칙이 적용되었다면</strong> 순위는 ▲상향 조정되었을 것입니다.",
    "relevance_level": "low"
}

]




#####XAI설명을 줄이면서 주석처리 
# XAI_META = {
#     1: {
#         "query_match": "‘수면–학습–기억’ 세 개념을 모두 직접적으로 다룹니다.",
#         "focus": "학습 이후 수면이 기억 형성 과정에 어떤 영향을 미치는지를 중심으로 살펴봅니다.",
#         "contribution": "수면과 기억 형성 간 관계를 직접 분석",
#         "badges": ["핵심 키워드 직접 일치", "비교적 최근 연구"]
#     },
#     2: {
#         "query_match": "수면, 학습, 기억 간의 관계를 직접적으로 다룹니다.",
#         "focus": "기억 유지뿐 아니라 이해와 정보 처리 측면까지 함께 다룹니다.",
#         "contribution": "수면이 학습 전반에 미치는 영향 확장",
#         "badges": ["핵심 키워드 직접 일치", "인용수 높음"]
#     },
#     3: {
#         "query_match": "수면과 기억 공고화, 학습 수행을 모두 포함합니다.",
#         "focus": "수면 이후 학습 내용이 실제 수행에 어떻게 연결되는지를 살펴봅니다.",
#         "contribution": "수면 이후 학습 내용 활용 과정 탐색",
#         "badges": ["핵심 키워드 직접 일치", "비교적 최근 연구"]
#     },
#     4: {
#         "query_match": "수면과 인지 수행을 중심으로 다루며, 학습·기억과는 간접적으로 연결됩니다.",
#         "focus": "수면 부족이 집중력과 수행에 미치는 영향을 중심으로 분석합니다.",
#         "contribution": "수면 부족이 인지 수행에 미치는 영향 분석",
#         "badges": ["주제 간접 관련"]
#     },
#     5: {
#         "query_match": "수면과 인지 기능을 중심으로 다루며, 기억과는 일부 연결됩니다.",
#         "focus": "주의나 실행 기능 등 다양한 인지 요소를 함께 살펴봅니다.",
#         "contribution": "수면과 다양한 인지 기능 간 관계 제시",
#         "badges": ["인용수 높음"]
#     },
#     6: {
#         "query_match": "수면의 질과 수행 변화를 중심으로 다루며, 학습·기억과는 간접적으로 연결됩니다.",
#         "focus": "수면의 질이 전반적인 수행에 어떤 차이를 만드는지를 살펴봅니다.",
#         "contribution": "수면의 질과 수행 수준 간 연관성 분석",
#         "badges": ["주제 간접 관련"]
#     },
#     7: {
#         "query_match": "수면과 학습 과정의 관계를 직접적으로 다루며, 기억과도 일부 연결됩니다.",
#         "focus": "학습 속도와 문제 해결 과정에서 수면의 역할을 살펴봅니다.",
#         "contribution": "수면이 학습 과정에 미치는 영향 탐색",
#         "badges": ["최신 연구"]
#     },
#     8: {
#         "query_match": "수면 패턴과 수행 변화를 중심으로 다루며, 학습·기억과는 간접적으로 연결됩니다.",
#         "focus": "수면의 규칙성이 수행 안정성에 미치는 영향을 살펴봅니다.",
#         "contribution": "수면 패턴과 수행 안정성 간 관계 분석",
#         "badges": ["주제 간접 관련"]
#     },
#     9: {
#         "query_match": "수면 제한과 기초 수행을 중심으로 다루며, 학습·기억과는 거리가 있습니다.",
#         "focus": "수면 부족이 기본적인 수행 능력에 미치는 영향을 살펴봅니다.",
#         "contribution": "수면 부족과 기본 수행 저하 간 관계 분석",
#         "badges": ["주제 주변부 연구"]
#     },
#     10: {
#         "query_match": "수면 부족과 전반적 수행 변화를 중심으로 다룹니다.",
#         "focus": "수면 부족이 다양한 수행 요소에 미치는 영향을 함께 분석합니다.",
#         "contribution": "수면 부족이 전반적 수행에 미치는 영향 제시",
#         "badges": ["주제 확장 영역 연구"]
#     }
# }



def badge_style(label: str):
    styles = {
        "핵심 키워드 직접 일치": {"bg": "#eef2ff", "color": "#3730a3", "border": "#c7d2fe"},
        "비교적 최근 연구": {"bg": "#ecfdf5", "color": "#065f46", "border": "#a7f3d0"},
        "최신 연구": {"bg": "#dcfce7", "color": "#166534", "border": "#86efac"},
        "인용수 높음": {"bg": "#eff6ff", "color": "#1d4ed8", "border": "#bfdbfe"},
        "주제 간접 관련": {"bg": "#f3f4f6", "color": "#4b5563", "border": "#d1d5db"},
        "주제 주변부 연구": {"bg": "#fff7ed", "color": "#9a3412", "border": "#fdba74"},
        "주제 확장 영역 연구": {"bg": "#fef3c7", "color": "#92400e", "border": "#fcd34d"},
    }
    return styles.get(label, {"bg": "#f3f4f6", "color": "#374151", "border": "#d1d5db"})


def render_badges(badges):
    parts = []
    for badge in badges:
        s = badge_style(badge)
        parts.append(
            f"<span style='display:inline-block;"
            f"margin-right:6px;"
            f"margin-bottom:6px;"
            f"padding:4px 8px;"
            f"font-size:12px;"
            f"font-weight:600;"
            f"border-radius:999px;"
            f"background:{s['bg']};"
            f"color:{s['color']};"
            f"border:1px solid {s['border']};"
            f"'>{badge}</span>"
        )
    return "".join(parts)


def render_xai_explanation(paper):
    import re
    
    # 1. 데이터 가져오기
    explanation = paper.get("xai_explanation", "시스템이 본 문헌의 연관성을 분석 중입니다.")
    
    # 2. 텍스트 강조 처리 (칩 생성)
    explanation = re.sub(r"'(.*?)'", r"<span class='chip-blue'>\1</span>", explanation)
    explanation = re.sub(r"(\d+위권|\d+위)", r"<span class='chip-purple'>\1</span>", explanation)

    # 3. 맥락 분석 및 화살표 처리
    if "만약" in explanation:
        parts = explanation.split("만약")
        core_factor = parts[0].strip()
        what_if_text = "만약 " + parts[1].strip()
        
        # 키워드 검사 (하락/상승)
        if any(word in what_if_text for word in ["하락", "제외", "낮아", "떨어"]):
            arrow = "↓"
            arrow_color = "#c62828"  # 빨간색
        elif any(word in what_if_text for word in ["상승", "상향", "높아", "올라"]):
            arrow = "↑"
            arrow_color = "#2e7d32"  # 초록색
        else:
            arrow = ""
            arrow_color = "transparent"
            
        # 화살표가 포함된 최종 문구 생성
        final_what_if = f"{what_if_text} <span style='color:{arrow_color}; font-weight: bold; margin-left:4px;'>{arrow}</span>"
    else:
        core_factor = explanation
        final_what_if = "현재 조건에서 최적의 검색 결과로 분석되었습니다."

    # 4. 통합 HTML/CSS 생성
    html_content = f"""
    <style>
        .xai-card-final {{
            background-color: #f8faff !important;
            border: 1px solid #e0e6ed !important;
            border-radius: 12px !important;
            margin: 15px 0 !important;
            padding: 0 !important;
            overflow: hidden;
            font-family: 'Pretendard', -apple-system, sans-serif;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        }}
        .xai-card-header {{ background-color: #f1f4f9; padding: 12px 18px; font-size: 15px; font-weight: 700; color: #1a237e; border-bottom: 1px solid #e0e6ed; display: flex; align-items: center; gap: 10px; }}
        .xai-card-row {{ display: flex; border-bottom: 1px solid #eef2f7; align-items: stretch; }}
        .xai-card-label {{ flex: 0 0 160px; background-color: #fcfdfe; padding: 14px 18px; font-size: 13px; font-weight: 700; color: #4a5568; display: flex; align-items: center; border-right: 1px solid #eef2f7; }}
        .xai-card-body {{ flex: 1; padding: 14px 18px; font-size: 14px; color: #2d3748; line-height: 1.6; background-color: white; }}
        .chip-blue {{ background: #e0f2f1; color: #00796b; padding: 2px 8px; border-radius: 6px; font-weight: 600; font-size: 12px; margin: 0 2px; }}
        .chip-purple {{ background: #ede7f6; color: #5e35b1; padding: 2px 8px; border-radius: 6px; font-weight: 600; font-size: 12px; margin: 0 2px; }}
    </style>

    <div class="xai-card-final">
        <div class="xai-card-header">
            <span style="font-size: 18px;">⌘</span> AI 시스템의 판단 근거
        </div>
        <div class="xai-card-row">
            <div class="xai-card-label">✩ 핵심 요인 및 상태</div>
            <div class="xai-card-body">{core_factor}</div>
        </div>
        <div class="xai-card-row" style="border-bottom: none;">
            <div class="xai-card-label">⌱ 가정 상황 분석</div>
            <div class="xai-card-body">{final_what_if}</div>
        </div>
    </div>
    """
    return html_content


# def render_xai_explanation(paper):
#     explanation = paper.get("xai_explanation", "")
#     explanation = explanation.replace("만약에", "<strong>만약에</strong>")
#     explanation = explanation.replace("만약 ", "<strong>만약</strong> ")


#     if not explanation:
#         explanation = "시스템은 이 문헌이 검색 주제와 관련성이 있다고 판단하였습니다."

#     return (
#         "<div class='xai-box'>"
#             "<div class='xai-header'>AI 시스템의 판단 근거</div>" #xai header 때문에 추가한 라인 
#             "<div class='xai-content'>"
#                 f"{explanation}"
#             "</div>"
#         "</div>"
#     )



# def render_xai_explanation(paper):
#     meta = XAI_META.get(paper["id"])

#     if meta is None:
#         return (
#             "<div class='xai-box'>"
#             "<div class='xai-content'>이 문헌은 검색 주제와 관련된 내용을 다룹니다.</div>"
#             "</div>"
#         )

#     return (
#         "<div class='xai-box'>"
#             f"<div style='margin-bottom:8px;'>{render_badges(meta['badges'])}</div>"

#             "<div class='xai-item'>"
#                 "<div class='xai-icon'>🔎</div>"
#                 "<div class='xai-content'>"
#                     "<span class='xai-tag'>질의 일치</span>"
#                     f"{(meta['query_match'])}"
#                 "</div>"
#             "</div>"

#             "<div class='xai-item'>"
#                 "<div class='xai-icon'>📍</div>"
#                 "<div class='xai-content'>"
#                     "<span class='xai-tag'>초점</span>"
#                     f"{(meta['focus'])}"
#                 "</div>"
#             "</div>"

#             "<div class='xai-item'>"
#                 "<div class='xai-icon'>🧩</div>"
#                 "<div class='xai-content'>"
#                     "<span class='xai-tag'>기여</span>"
#                     f"{(meta['contribution'])}"
#                 "</div>"
#             "</div>"
#         "</div>"
#     )



## [수정후] 고정된 순서로 정렬
def build_balanced_paper_order(papers):
    paper_dict = {p["id"]: p for p in papers}

    # 사용할 고정 패턴 하나만 남깁니다 (예: Pattern A)
    fixed_pattern = [7, 1, 4, 2, 3, 5, 6, 8, 9, 10]

    # 고정된 순서대로 논문 리스트 생성
    ordered_papers = [paper_dict[i] for i in fixed_pattern]

    # selected_pattern도 고정값으로 반환 (기존 로직과의 호환성을 위해)
    return ordered_papers, fixed_pattern


def bold_keywords(text, keywords=QUERY_KEYWORDS):
    for kw in keywords:
        text = re.sub(
            f"({kw})",
            r"<strong>\1</strong>",
            text
        )
    return text




# =========================
# Preview 생성 함수
# =========================
def make_preview(text, limit=140):
    if len(text) <= limit:
        return text
    return text[:limit] + "..."


# 1. 함수의 '정의' 부분을 먼저 수정합니다.
def save_log(data_dict):
    """구글 시트에 행을 추가하는 함수 (A열~O열 순서)"""
    sheet = get_sheet()
    
    # 엑셀 시트의 왼쪽(A)부터 오른쪽(O) 순서와 일치함
    row = [
        data["user_id"],                    # 참가자 고유 ID
        data["condition"],                  # 실험 조건 (e.g., XAI vs No-XAI)
        data["timestamp"],                  # 응답 제출 시간

        data["selected_ids"],               # 최종 선택한 문헌 ID 목록 (2개)
        data["selected_scores"],            # 선택한 문헌들의 relevance 점수 목록
        data["selected_quality_score"],     # 선택 문헌 점수 평균 (선택의 질)

        data["unique_docs_viewed"],         # 서로 다른 문헌 몇 개를 열람했는지 (중복 제거)
        data["abstract_clicks_total"],      # 초록 열람 총 횟수 (메인 + 비교함 포함)
        data["abstract_click_log"],         # 초록 열람 순서 로그 (예: [1,2,3,2])

        data["revisit_count_total"],        # 재열람 총 횟수 (같은 문헌을 다시 본 횟수)
        data["revisit_count_direct"],       # 메인 화면에서의 재열람 횟수
        data["revisit_count_sidebar"],      # 비교함(사이드바)에서의 재열람 횟수

        data["comparison_basket_current"],  # 최종 비교함에 남아있는 문헌 ID 목록
        data["comparison_basket_history"],  # 비교함에 추가된 모든 문헌 기록 (히스토리)

        data["time_to_first_selection"],    # 첫 번째 문헌 선택까지 걸린 시간 (초)
        data["total_time_spent"],           # 전체 과제 수행 시간 (초)

        data["xai_open_count"],             # XAI 설명을 연 총 횟수
        data["xai_open_log"],               # XAI 설명 열람 로그 (문헌 ID 기준)
        data["xai_view_time_total"],        # XAI 설명을 보는 데 사용한 총 시간

        data["abstract_view_time_total"],   # 초록(abstract)을 읽는 데 사용한 총 시간

        data["ordered_paper_ids"],          # 참가자에게 제시된 문헌 순서 (position bias 분석용)
        data["click_sequence"]              # 전체 행동 로그 (모든 클릭 이벤트 순서 기록)
    ]

    
    sheet.append_row(row, value_input_option='RAW')



# @st.cache_resource
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

def get_existing_condition_counts():
    sheet = get_sheet()   # 👈 여기서 사용됨 (여기 안에 들어가는 거 아님)

    values = sheet.get_all_values()

    if len(values) <= 1:
        return 0, 0

    condition1_count = 0
    condition2_count = 0

    for row in values[1:]:
        if len(row) > 1:
            if row[1] == "condition1":
                condition1_count += 1
            elif row[1] == "condition2":
                condition2_count += 1

    return condition1_count, condition2_count


def assign_balanced_condition():
    try:
        c1, c2 = get_existing_condition_counts()
        # 데이터 확인용 로그 (콘솔에 출력됨)
        print(f"현재 시트 카운트 -> Cond1: {c1}, Cond2: {c2}")
        
        if c1 <= c2:
            return "condition1"
        else:
            return "condition2"
    except Exception as e:
        print(f"시트 읽기 실패: {e}")
        return random.choice(["condition1", "condition2"]) # 실패 시 랜덤 배정
    

# =========================
# 상태 초기화
# =========================
if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())[:8]

if "condition" not in st.session_state:
    st.session_state.condition = assign_balanced_condition()

# if "condition" not in st.session_state:
#     st.session_state.condition = random.choice(["condition1", "condition2"])

if "selected" not in st.session_state:
    st.session_state.selected = []

# if "open_paper_id" not in st.session_state:
#     st.session_state.open_paper_id = None

# 기존 open_paper_id 대신 팝업 관리를 위한 변수 생성
if "current_popup_id" not in st.session_state:
    st.session_state.current_popup_id = None

# XAI 펼치기 상태를 추적하기 위한 사전 (각 논문 ID별로 열림 여부 저장)
if "xai_open_state" not in st.session_state:
    st.session_state.xai_open_state = {}

# 비교 바구니 (선택된 논문 ID 저장)
if "comparison_basket" not in st.session_state:
    st.session_state.comparison_basket = []

if "comparison_basket_history" not in st.session_state:
    st.session_state.comparison_basket_history = []

if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

if "first_selection_time" not in st.session_state:
    st.session_state.first_selection_time = None

if "click_log" not in st.session_state:
    st.session_state.click_log = {"select": 0, "remove": 0}

if "viewed_docs" not in st.session_state:
    st.session_state.viewed_docs = set()

# if "abstract_clicks" not in st.session_state:
#     st.session_state.abstract_clicks = 0

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

# if "show_survey_link" not in st.session_state:
#     st.session_state.show_survey_link = False

if "click_sequence" not in st.session_state:
    st.session_state.click_sequence = []

# [상태 초기화 섹션]
if "abstract_clicks" not in st.session_state:
    st.session_state.abstract_clicks = 0  

if "abstract_popup_times" not in st.session_state:
    st.session_state.abstract_popup_times = []  # [("open", 시간), ("close", 시간)] 형태

if "xai_view_times" not in st.session_state:
    st.session_state.xai_view_times = []        # [(paper_id, 시작시간, 종료시간)]

if "abstract_popup_open_timestamps" not in st.session_state:
    st.session_state.abstract_popup_open_timestamps = []

if "abstract_review_durations" not in st.session_state:
    st.session_state.abstract_review_durations = []

if "temp_open_time" not in st.session_state:
    st.session_state.temp_open_time = 0

if "xai_view_timestamps" not in st.session_state:
    st.session_state.xai_view_timestamps = []


# 추가 로그 변수 초기화

if "comparison_basket_history" not in st.session_state:
    st.session_state.comparison_basket_history = []

if "revisit_count_direct" not in st.session_state:
    st.session_state.revisit_count_direct = 0

if "revisit_count_sidebar" not in st.session_state:
    st.session_state.revisit_count_sidebar = 0

if "direct_revisit_log" not in st.session_state:
    st.session_state.direct_revisit_log = []

if "sidebar_revisit_log" not in st.session_state:
    st.session_state.sidebar_revisit_log = []

if "xai_open_log" not in st.session_state:
    st.session_state.xai_open_log = []

if "xai_view_duration_log" not in st.session_state:
    st.session_state.xai_view_duration_log = []

if "xai_open_start_times" not in st.session_state:
    st.session_state.xai_open_start_times = {}

if "active_panel" not in st.session_state:
    st.session_state.active_panel = None

if "show_survey_link" not in st.session_state:
    st.session_state.show_survey_link = False


import random




# 선택 로직함수_본화면과 비교함 선택 모두 공통
# def handle_selection(paper_id):
#     if paper_id not in st.session_state.selected:
def handle_selection(paper_id):
    paper_id = int(paper_id)
    st.session_state.selected = [int(x) for x in st.session_state.selected]

    if paper_id not in st.session_state.selected:
        if len(st.session_state.selected) < 2:
            st.session_state.selected.append(paper_id)
            # 첫 선택 시간 기록
            if len(st.session_state.selected) == 1:
                st.session_state.first_selection_time = time.time() - st.session_state.start_time
            st.session_state.click_sequence.append(f"select_paper_{paper_id}")
        else:
            st.warning("이미 2편을 선택하셨습니다. 기존 선택을 취소하고 다시 선택해주세요.")
    else:
        st.info("이미 선택된 논문입니다.")


#공통해제함수
def handle_deselection(paper_id):
    paper_id = int(paper_id)
    st.session_state.selected = [int(x) for x in st.session_state.selected]
    st.session_state.selected = [x for x in st.session_state.selected if x != paper_id]
    st.session_state.click_sequence.append(f"deselect_{paper_id}")



#패널 강제 종료 함수 
def close_active_panel():
    active = st.session_state.active_panel
    if not active:
        return

    duration = round(time.time() - active["opened_at"], 2)

    if active["type"] == "abstract":
        st.session_state.abstract_review_durations.append(duration)
        st.session_state.click_sequence.append(f"abstract_close_{active['paper_id']}")

    elif active["type"] == "xai":
        st.session_state.xai_view_duration_log.append((active["paper_id"], duration))
        st.session_state.click_sequence.append(f"xai_close_{active['paper_id']}")

    st.session_state.active_panel = None


def open_panel(panel_type, paper_id):
    active = st.session_state.active_panel

    # 같은 패널 다시 클릭 → 닫기만 하고 종료
    if active and active["type"] == panel_type and active["paper_id"] == paper_id:
        close_active_panel()

        if panel_type == "abstract":
            st.session_state.current_popup_id = None
        elif panel_type == "xai":
            st.session_state.xai_open_state[paper_id] = False

        return "closed"

    # 다른 패널이 이미 열려 있으면 강제 종료
    if active:
        old_type = active["type"]
        old_paper_id = active["paper_id"]

        close_active_panel()

        if old_type == "abstract":
            st.session_state.current_popup_id = None
        elif old_type == "xai":
            st.session_state.xai_open_state[old_paper_id] = False

    # 새 패널 열기
    st.session_state.active_panel = {
        "type": panel_type,
        "paper_id": paper_id,
        "opened_at": time.time()
    }

    if panel_type == "abstract":
        st.session_state.current_popup_id = paper_id
        st.session_state.click_sequence.append(f"view_abstract_{paper_id}")

    elif panel_type == "xai":
        # 다른 XAI는 전부 닫힘 처리
        for pid in st.session_state.xai_open_state:
            st.session_state.xai_open_state[pid] = False

        st.session_state.xai_open_state[paper_id] = True
        st.session_state.xai_open_log.append(paper_id)
        st.session_state.click_sequence.append(f"xai_open_{paper_id}")

    return "opened"





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
    을 선택(select)하세요. 언제든 취소 후 재선택이 가능합니다.<br>
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
    1: 3,  # high
    2: 3,  # high
    3: 3,  # high
    4: 2,  # low
    5: 2,  # medium
    6: 2,  # medium
    7: 2,  # medium
    8: 3,  # medium
    9: 1,  # low
    10: 1, # low
}

st.markdown("""
<style>
.paper-title {
    font-weight: 400;
}

.paper-title strong {
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)



# =========================
# 논문 렌더링 함수
# =========================
def render_paper_semantic(paper, idx):
    paper_id = int(paper["id"])

    st.session_state.selected = [int(x) for x in st.session_state.selected]
    st.session_state.comparison_basket = [int(x) for x in st.session_state.comparison_basket]

    is_selected = paper_id in st.session_state.selected
    in_basket = paper_id in st.session_state.comparison_basket
# def render_paper_semantic(paper, idx):
#     paper_id = paper["id"]
#     is_selected = paper_id in st.session_state.selected
#     # 현재 이 논문이 바구니에 있는지 확인
#     in_basket = paper_id in st.session_state.comparison_basket

    # 논문 블록 시작
    st.markdown('<div class="paper-block">', unsafe_allow_html=True)

    # 1. 제목 및 기본 정보
    title = bold_keywords(paper["title"])
    st.markdown(f'<div class="paper-title">{title}</div>', unsafe_allow_html=True)
    # st.markdown(f'<div class="paper-title">{paper["title"]}</div>', unsafe_allow_html=True)

    st.markdown(
        f'<div class="paper-citation">{paper["author"]} · {paper["year"]} · {paper["venue"]} · 인용 {paper["citation_count"]}회</div>',
        unsafe_allow_html=True
    )

    # 2. 키워드 칩
    keyword_html = "".join([f'<span class="meta-chip">{kw}</span>' for kw in paper["keywords"]])
    st.markdown(keyword_html, unsafe_allow_html=True)


    # --- [추가 시작] 초록 미리보기 및 더보기 ---
    abstract_full = paper.get("abstract", "")
    # 100자 미리보기 (키워드 강조 포함)
    abstract_preview = bold_keywords(abstract_full[:100]) + "..." if len(abstract_full) > 100 else bold_keywords(abstract_full)
    
    st.markdown(f'<div style="color: #555; font-size: 0.95rem; margin: 10px 0 5px 0;">{abstract_preview}</div>', unsafe_allow_html=True)
    
    with st.expander("📄 초록 전체 읽기"):
        st.write(abstract_full)
        # 기존 상세초록 버튼의 로그 기록 기능을 유지하고 싶다면 여기에 넣을 수 있습니다.
        if paper_id not in st.session_state.viewed_docs:
            st.session_state.viewed_docs.add(paper_id)
            st.session_state.abstract_clicks += 1
    # --- [추가 끝] ---


# --- [수정] 버튼들을 초록 아래에 가로로 배치 ---
    # 버튼들을 담을 4개의 컬럼 생성 (간격 조절)
    btn_col1, btn_col2, btn_col3, btn_col4 = st.columns([1.5, 1.2, 1.2, 3])

    with btn_col1:
        # 1. AI 판단 근거 버튼 (기존 col_content에 있던 것)
        if st.session_state.condition == "condition1":
            is_xai_open = st.session_state.xai_open_state.get(paper_id, False)
            xai_label = "⚛️ AI 판단 근거" if not st.session_state.xai_open_state.get(paper_id, False) else "✖ 닫기"
            
            if st.button(xai_label, key=f"xai_toggle_{paper_id}", use_container_width=True):
                            open_panel("xai", paper_id) # <<<< 세션을 직접 안 건드리고 함수를 호출!
                            st.rerun()

            # if st.button(xai_label, key=f"xai_toggle_{paper_id}", use_container_width=True):
            #     st.session_state.xai_open_state[paper_id] = not st.session_state.xai_open_state.get(paper_id, False)
            #     st.rerun()

    with btn_col2:
        # 2. 비교함 담기 버튼
        if in_basket:
            if st.button("⎷ 담김", key=f"btn_basket_{paper_id}", use_container_width=True, type="secondary"):
                st.session_state.comparison_basket.remove(paper_id)
                st.rerun()
        else:
            if st.button("비교함 담기", key=f"btn_basket_{paper_id}", use_container_width=True):
                st.session_state.comparison_basket.append(paper_id)
                st.rerun()

    with btn_col3:
        # 3. 선택하기 버튼
        if paper_id in st.session_state.selected:
            if st.button("✗ 취소", key=f"main_sel_{paper_id}", use_container_width=True, type="primary"):
                st.session_state.selected = [x for x in st.session_state.selected if int(x) != paper_id]
                st.rerun()
        else:
            if st.button("선택", key=f"main_sel_{paper_id}", use_container_width=True):
                handle_selection(paper_id)
                st.rerun()

    # AI 판단 근거 출력 위치 (버튼들 바로 아래)
    if st.session_state.condition == "condition1" and st.session_state.xai_open_state.get(paper_id, False):
        st.markdown(render_xai_explanation(paper), unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True) # paper-block 닫기





    # # 3. 레이아웃 구성 (본문 상호작용)
    # col_content, col_action = st.columns([6, 1.8])

    # with col_content:
    #     if st.session_state.condition == "condition1":
    #         if paper_id not in st.session_state.xai_open_state:
    #             st.session_state.xai_open_state[paper_id] = False

    #         xai_btn_label = "✨ AI 판단 근거 확인하기" if not st.session_state.xai_open_state[paper_id] else "✖ AI 추천 근거 닫기"

    #         if st.button(xai_btn_label, key=f"xai_toggle_{paper_id}"):
    #             result = open_panel("xai", paper_id)
    #             st.rerun()

    #         if st.session_state.xai_open_state[paper_id]:
    #             st.markdown(render_xai_explanation(paper), unsafe_allow_html=True)

    #     else:
    #         st.write("상세 내용을 확인하려면 오른쪽 버튼을 클릭하세요.")



    # with col_action:
    #     # 1. 상세초록 보기 버튼
    #     # if st.button("📄 상세초록 보기", key=f"popup_btn_{paper_id}", use_container_width=True):

    #     #     already_viewed = paper_id in st.session_state.viewed_docs

    #     #     if already_viewed:
    #     #         st.session_state.revisit_count_direct += 1
    #     #         st.session_state.direct_revisit_log.append(paper_id)
    #     #         st.session_state.click_sequence.append(f"direct_revisit_{paper_id}")

    #     #     st.session_state.viewed_docs.add(paper_id)
    #     #     st.session_state.abstract_clicks += 1
    #     #     st.session_state.abstract_popup_open_timestamps.append(datetime.now().isoformat())

    #     #     result = open_panel("abstract", paper_id)
    #     #     st.rerun()


    #     # 2. 비교함 담기 버튼
    #     if in_basket:
    #         if st.button("✔️ 비교함 담김", key=f"btn_basket_{paper_id}", use_container_width=True, type="secondary"):
    #             if paper_id in st.session_state.comparison_basket:
    #                 st.session_state.comparison_basket.remove(paper_id)
    #             st.session_state.click_sequence.append(f"basket_remove_{paper_id}")
    #             st.rerun()
    #     else:
    #         if st.button("🧺 비교함 담기", key=f"btn_basket_{paper_id}", use_container_width=True):
    #             if paper_id not in st.session_state.comparison_basket:
    #                 st.session_state.comparison_basket.append(paper_id)

    #             if paper_id not in st.session_state.comparison_basket_history:
    #                 st.session_state.comparison_basket_history.append(paper_id)

    #             st.session_state.click_sequence.append(f"basket_add_{paper_id}")
    #             st.rerun()

    #     # 3. 선택하기 버튼
    #     if paper_id in st.session_state.selected:
    #         if st.button("✅ 선택 취소", key=f"main_sel_{paper_id}", use_container_width=True, type="primary"):
    #             # st.session_state.selected.remove(paper_id)
    #             st.session_state.selected = [x for x in st.session_state.selected if int(x) != paper_id]
    #             st.session_state.click_sequence.append(f"deselect_{paper_id}")
    #             st.rerun()
    #     else:
    #         if st.button("선택하기", key=f"main_sel_{paper_id}", use_container_width=True):
    #             handle_selection(paper_id)
    #             st.rerun()


    # # col_action 블록 밖으로 나와서 여백 추가
    # st.markdown("<br>", unsafe_allow_html=True)


# =========================
# 논문 출력
# =========================
for idx, paper in enumerate(st.session_state.ordered_papers):
    render_paper_semantic(paper, idx)

    # '설명보기' 버튼을 눌렀을 때만 나타나게 하는 코드 예시
    if st.session_state.get(f"show_xai_{paper['id']}", False):
        st.markdown(render_xai_explanation(paper), unsafe_allow_html=True)


# =========================
# [1] 사이드바 (비교함) 및 재방문 기록
# =========================
with st.sidebar:
    st.session_state.comparison_basket = list(dict.fromkeys(st.session_state.comparison_basket))
    st.markdown("### 🗃️ 문헌 비교함")
    
    if not st.session_state.comparison_basket:
        st.info("비교할 논문의 '비교함 담기'를 체크해 주세요.")
    else:
        st.write("담긴 논문 (클릭 시 초록 보기):")
        for p_id in st.session_state.comparison_basket:
            p_item = next((p for p in papers if p["id"] == p_id), None)
            if p_item:
                # 논문 제목 (초록 보기 버튼)
            
                #비교함 내리기 위한 주석처리 
                # 레이아웃을 쪼개서 [보기 버튼]과 [선택 버튼]을 나란히 배치
                col_view, col_sel = st.columns([3, 1.2])
                
                # 1. 기존의 '초록 보기' 버튼 (로깅 로직 유지)
                if col_view.button(f"🔍 {p_item['title']}", key=f"side_view_{p_id}", use_container_width=True):

                    st.session_state.revisit_count_sidebar += 1
                    st.session_state.sidebar_revisit_log.append(p_id)

                    st.session_state.abstract_clicks += 1
                    st.session_state.abstract_popup_open_timestamps.append(datetime.now().isoformat())
                    st.session_state.click_sequence.append(f"basket_revisit_{p_id}")

                    result = open_panel("abstract", p_id)
                    st.rerun()

                p_id = int(p_id)
                st.session_state.selected = [int(x) for x in st.session_state.selected]

                is_selected_in_sidebar = p_id in st.session_state.selected
                side_select_label = "선택 취소" if is_selected_in_sidebar else "선택"

                if col_sel.button(
                    side_select_label,
                    key=f"side_sel_{p_id}",
                    use_container_width=True,
                    type="primary" if is_selected_in_sidebar else "secondary"
                ):
                    if is_selected_in_sidebar:
                        handle_deselection(p_id)
                    else:
                        handle_selection(p_id)
                    st.rerun()

        # if len(st.session_state.selected) >= 2:
        #     st.divider() # 얇은 구분선
        #     st.success("✅ **2편 선택 완료!**")
            
            # # HTML 앵커 링크 (디자인 포함)
            # st.markdown(
            #     """
            #     <a href='#link_to_submit' style='text-decoration: none;'>
            #         <div style='background-color: #f0f2f6; border-radius: 8px; padding: 12px; 
            #                     text-align: center; color: #31333F; font-weight: bold; 
            #                     border: 1px solid #d1d5db; cursor: pointer;'>
            #             👇 하단으로 이동하여 제출하기
            #         </div>
            #     </a>
            #     """, 
            #     unsafe_allow_html=True
            # )


        st.divider()
        # 비교함 비우기 로직 유지
        if st.button("비교함 전체 비우기", type="secondary", use_container_width=True):
            st.session_state.comparison_basket = []
            st.session_state.click_sequence.append("basket_clear_all")
            st.rerun()


    if len(st.session_state.selected) >= 2:
            st.divider() 
            st.success("✅ **2편 선택 완료!**")
            
            st.markdown(
                """
                <a href='#link_to_submit' style='text-decoration: none;'>
                    <div style='background-color: #f0f2f6; border-radius: 8px; padding: 12px; 
                                text-align: center; color: #31333F; font-weight: bold; 
                                border: 1px solid #d1d5db; cursor: pointer;'>
                        👇 하단으로 이동하여 제출하기
                    </div>
                </a>
                """, 
                unsafe_allow_html=True
            )





    # --- 최종 선택 현황 및 취소 구역 ---
    st.divider()
    st.markdown("### ✔️ 최종 선택된 논문 (2편)")
    if not st.session_state.selected:
        st.caption("아직 선택된 논문이 없습니다.")
    else:
        for s_id in st.session_state.selected:
            s_item = next((p for p in papers if p["id"] == s_id), None)
            if s_item:
                st.markdown(
                    f"""
                    <div style="
                        background-color: #eeeeee; 
                        padding: 10px 15px; 
                        border-radius: 5px; 
                        border-left: 5px solid #9e9e9e; 
                        margin-bottom: 5px;
                        color: #31333F;
                        font-size: 0.9rem;
                        font-weight: bold;
                        line-height: 1.4;
                    ">
                        {s_item['title']}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # st.success(f"**{s_item['title']}**")
                if st.button(f"선택 취소", key=f"cancel_{s_id}", use_container_width=True):
                    st.session_state.selected.remove(s_id)
                    st.session_state.click_sequence.append(f"cancel_selection_{s_id}")
                    st.rerun()

#앵커(여기로 스크롤다운하게 할거)
# 1. 도착지점 설정 (HTML div 태그 활용)
# st.markdown("<div id='link_to_submit'></div>", unsafe_allow_html=True)

# 2. 기존의 제출하기 버튼 (이미 있는 버튼)
# if st.button("선택 제출하기"):
#     # 제출 로직 (설문 페이지 이동 등)
#     pass



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
    st.markdown("<div id='link_to_submit'></div>", unsafe_allow_html=True) #앵커
    if not st.session_state.show_survey_link:
        if st.button("선택 완료 및 설문시작", key="save_and_go_survey"):
            end_time = time.time()

            # 저장 직전 현재 열려 있는 패널이 있으면 강제 종료 후 시간 반영
            if st.session_state.active_panel is not None:
                close_active_panel()

                if st.session_state.current_popup_id is not None:
                    st.session_state.current_popup_id = None

                for pid in st.session_state.xai_open_state:
                    st.session_state.xai_open_state[pid] = False


            # 클릭 로그 기반으로 실제 열람 문헌 계산
            viewed_ids = []
            abstract_only_ids = []

            for log in st.session_state.click_sequence:
                try:
                    if log.startswith("view_abstract_"):
                        p_id = int(log.split("_")[-1])
                        viewed_ids.append(p_id)
                        abstract_only_ids.append(p_id)

                    elif log.startswith("xai_open_"):
                        p_id = int(log.split("_")[-1])
                        viewed_ids.append(p_id)
                except Exception:
                    continue



    #계산블록 
            unique_viewed_list = sorted(list(set(viewed_ids)))
            abstract_unique_list = sorted(list(set(abstract_only_ids)))

            sel_scores = [relevance_score_map.get(pid, 0) for pid in st.session_state.selected]
            quality_avg = sum(sel_scores) / len(sel_scores) if sel_scores else 0

            total_time = end_time - st.session_state.start_time
            time_to_first = round(st.session_state.first_selection_time, 2) if st.session_state.first_selection_time else ""

            revisit_count_total = (
                st.session_state.revisit_count_direct +
                st.session_state.revisit_count_sidebar
            )

            abstract_view_time_total = round(sum(st.session_state.abstract_review_durations), 2) \
                if st.session_state.abstract_review_durations else 0

            xai_view_time_total = round(
                sum(duration for _, duration in st.session_state.xai_view_duration_log), 2
            ) if st.session_state.xai_view_duration_log else 0

            xai_open_count = len(st.session_state.xai_open_log)

            # ---------------------------
            # abstract 전체 로그 재계산
            # ---------------------------
            abstract_all_ids = []

            for log in st.session_state.click_sequence:
                try:
                    if log.startswith("view_abstract_"):
                        p_id = int(log.split("_")[-1])
                        abstract_all_ids.append(p_id)

                except Exception:
                    continue

            abstract_clicks_total = len(abstract_all_ids)
            abstract_unique_list = list(dict.fromkeys(abstract_all_ids))
            unique_docs_viewed = len(abstract_unique_list)


            data = {
                "user_id": st.session_state.user_id,
                "condition": st.session_state.condition,
                "timestamp": datetime.now().isoformat(),

                "selected_ids": str(st.session_state.selected),
                "selected_scores": str(sel_scores),
                "selected_quality_score": round(quality_avg, 2),

                "unique_docs_viewed": unique_docs_viewed,
                "abstract_clicks_total": abstract_clicks_total,
                "abstract_click_log": str(abstract_all_ids),

                "revisit_count_total": revisit_count_total,
                "revisit_count_direct": st.session_state.revisit_count_direct,
                "revisit_count_sidebar": st.session_state.revisit_count_sidebar,

                "comparison_basket_current": str(st.session_state.comparison_basket),
                "comparison_basket_history": str(st.session_state.comparison_basket_history),

                "time_to_first_selection": time_to_first,
                "total_time_spent": round(total_time, 2),

                "xai_open_count": xai_open_count,
                "xai_open_log": str(st.session_state.xai_open_log),
                "xai_view_time_total": xai_view_time_total,
                "abstract_view_time_total": abstract_view_time_total,

                "ordered_paper_ids": str([p["id"] for p in st.session_state.ordered_papers]),
                "click_sequence": str(st.session_state.click_sequence)
            }


            
            try:
                with st.spinner("응답을 저장하고 있습니다..."):
                    save_log(data)

                st.session_state.survey_saved = True
                st.session_state.show_survey_link = True
                # st.success("데이터가 성공적으로 기록되었습니다.")
                st.rerun()

            except Exception as e:
                st.error(f"저장 실패: {e}")

    
    else:
        # st.session_state.show_survey_link:
        st.success("선택 결과가 저장되었습니다. 아래 버튼을 눌러 설문으로 이동해주세요.")

        st.markdown("### Next Step")
        st.markdown("다음의 설문을 완료해주세요. (예상 소요시간 5분)")

        st.link_button("👉 Go to Survey", form_url)



# =========================
# [3] 상세초록 팝업 (가장 중요: 파일 최하단)
# =========================
if st.session_state.current_popup_id:
    curr_id = st.session_state.current_popup_id
    paper_to_show = next((p for p in papers if p["id"] == curr_id), None)
    
    if paper_to_show:
        @st.dialog("📄 문헌 상세 정보", width="large")
        def show_abstract_dialog(p):
            st.subheader(p["title"])
            st.caption(f"{p['author']} ({p['year']}) · {p['venue']}")
            st.write("---")
            st.markdown("**Abstract**")
            st.write(p["abstract"])
            st.write("---")
            
            # [닫기 버튼 클릭 시 데이터 기록]
            if st.button("닫기", use_container_width=True):
                close_active_panel()
                st.session_state.current_popup_id = None
                st.rerun()

        # 정의 후 즉시 호출 (노란 줄 사라짐)
        show_abstract_dialog(paper_to_show)






