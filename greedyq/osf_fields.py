"""Field identifiers for the official OSF Preregistration offline form.

Verified 2026-09-10 against the document linked by OSF Support.
Labels are concise independent descriptions; no template prose is copied.
"""

SOURCE = "https://docs.google.com/document/d/1gkN0Jp6Gu7GIA4Ne4YCDZ61nCLQRgt32moRdUg9AnVg/edit"
CHECKED = "2026-09-10"
FIELDS = [
    ("title", "Study title", "연구 제목"),
    ("description", "Study summary", "연구 요약"),
    ("contributors", "Research contributors", "연구 참여 저자"),
    ("license", "Registration license", "등록 문서 라이선스"),
    ("subject", "Research subjects / disciplines", "연구 분야"),
    ("tags", "Discovery keywords", "검색 키워드"),
    ("research_questions", "Questions and hypotheses", "연구 질문과 가설"),
    ("foreknowledge", "Prior access to study data", "연구 데이터 사전 접근·열람 여부"),
    ("foreknowledge_explanation", "Prior-knowledge safeguards (optional)", "사전 지식과 영향 방지 조치 (선택)"),
    ("study_type", "Type of investigation", "연구 유형"),
    ("causal_interpretation", "Intended causal claims (optional)", "의도한 인과 해석 (선택)"),
    ("blinding", "Treatment awareness", "처치 정보 눈가림"),
    ("additional_blinding", "Other masking procedures (optional)", "추가 눈가림 절차 (선택)"),
    ("study_design", "Design and comparisons", "연구 설계와 비교"),
    ("randomization", "Assignment and ordering methods (optional)", "무작위 배정·순서 방법 (선택)"),
    ("data_collection", "Recruitment and collection procedures", "모집과 수집 절차"),
    ("sample_size", "Planned sample counts", "계획 표본 수"),
    ("sample_size_rationale", "Basis for sample counts (optional)", "표본 수 근거 (선택)"),
    ("starting_stopping_rules", "Pilot, collection start and stop rules", "파일럿·본조사 시작·종료 기준"),
    ("manipulated_variables", "Experimental factors", "조작 변수"),
    ("measured_variables", "Recorded measures", "측정 변수"),
    ("indices", "Composite and derived measures", "합성·파생 변수"),
    ("statistical_models", "Models and hypothesis tests", "통계 모형과 가설 검정"),
    ("transformations", "Coding and transformations", "코딩과 변환"),
    ("inference_criteria", "Evidence thresholds and multiplicity", "판단 기준과 다중 검정"),
    ("data_inclusion_exclusion", "Inclusion, exclusions and outliers", "포함·제외·이상치 처리"),
    ("missing_data", "Handling incomplete observations", "결측치 처리"),
    ("other_planned_analysis", "Additional analyses (optional)", "추가 분석 (선택)"),
    ("context", "Additional context", "추가 맥락"),
]
