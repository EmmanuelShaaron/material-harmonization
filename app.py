import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import json







# ============================================================
# CHART THEME
# ============================================================

CHART_BG = "#111A2B"
CHART_GRID = "#263650"
TEXT_MAIN = "#F4F7FC"
TEXT_MUTED = "#8D9AAF"

COLOR_BLUE = "#4F7CFF"
COLOR_CYAN = "#38BDF8"
COLOR_GREEN = "#35C98B"
COLOR_AMBER = "#F2B84B"
COLOR_RED = "#E45B5B"
COLOR_PURPLE = "#9B8AFB"


def style_chart(fig, height=340):

    fig.update_layout(
        height=height,

        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",

        font=dict(
            color=TEXT_MUTED,
            family="Inter, sans-serif"
        ),

        margin=dict(
            l=20,
            r=20,
            t=35,
            b=20
        ),

        hoverlabel=dict(
            bgcolor=CHART_BG,
            font_color=TEXT_MAIN
        ),

        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(color=TEXT_MUTED)
        )
    )

    fig.update_xaxes(
        gridcolor=CHART_GRID,
        zeroline=False
    )

    fig.update_yaxes(
        gridcolor=CHART_GRID,
        zeroline=False
    )

    return fig



# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="National Material Harmonization",
    page_icon="🏭",
    layout="wide"
)

# ============================================================
# CUSTOM UI STYLING
# ============================================================

st.html(
    """
    <style>
    /* ============================================================
   GLOBAL
   ============================================================ */

.stApp {
    background: #0B1220 !important;
    color: #E8EDF7;
}

.main .block-container {
    padding-top: 1.4rem;
    padding-bottom: 2rem;
    max-width: 1450px;
}

h1, h2, h3, h4 {
    color: #F4F7FC !important;
    letter-spacing: -0.025em;
}

p {
    color: #A8B3C7;
}

/* Reduce excessive Streamlit vertical spacing */

[data-testid="stVerticalBlock"] {
    gap: 0.55rem;
}

hr {
    border-color: #26344A !important;
    margin: 12px 0 !important;
}


/* ============================================================
   SIDEBAR
   ============================================================ */

section[data-testid="stSidebar"] {
    background: #09111F !important;
    border-right: 1px solid #1E2A3D;
}

section[data-testid="stSidebar"] * {
    color: #E8EDF5;
}

.sidebar-brand {
    padding: 8px 8px 20px 8px;
    border-bottom: 1px solid #26344A;
    margin-bottom: 15px;
}

.sidebar-logo {
    font-size: 32px;
    margin-bottom: 8px;
}

.sidebar-title {
    font-size: 21px;
    font-weight: 750;
    line-height: 1.2;
    color: #F4F7FC;
}

.sidebar-subtitle {
    margin-top: 8px;
    font-size: 12px;
    line-height: 1.5;
    color: #8996AA;
}

.sidebar-section {
    font-size: 10px;
    font-weight: 750;
    letter-spacing: 0.16em;
    color: #66758D;
    margin: 16px 8px 7px 8px;
}

.sidebar-system {
    margin-top: 22px;
    padding: 14px;
    border: 1px solid #263650;
    border-radius: 12px;
    background: #111C2E;
}

.sidebar-system-title {
    font-size: 10px;
    font-weight: 750;
    letter-spacing: 0.12em;
    color: #8290A6;
}

.sidebar-system-status {
    margin-top: 8px;
    font-size: 11px;
    font-weight: 700;
    color: #55D6A0;
}

.sidebar-system-text {
    margin-top: 7px;
    font-size: 10px;
    line-height: 1.5;
    color: #96A3B7;
}


/* ============================================================
   PAGE HEADER
   ============================================================ */

.page-kicker {
    font-size: 11px;
    font-weight: 750;
    letter-spacing: 0.17em;
    color: #5C85FF;
    margin-bottom: 6px;
}

.page-title {
    font-size: 44px;
    font-weight: 800;
    color: #F4F7FC;
    line-height: 1.08;
}

.page-subtitle {
    margin-top: 8px;
    color: #93A0B5;
    font-size: 15px;
    max-width: 850px;
    line-height: 1.55;
}

.demo-pill {
    display: inline-flex;
    align-items: center;
    margin-top: 12px;
    padding: 6px 12px;
    border-radius: 999px;

    background: #152541;
    border: 1px solid #294574;

    color: #75A0FF;

    font-size: 10px;
    font-weight: 750;
    letter-spacing: 0.09em;
}


/* ============================================================
   SECTION HEADINGS
   ============================================================ */

.section-wrap {
    margin-top: 20px;
    margin-bottom: 10px;
}

.section-kicker {
    font-size: 10px;
    font-weight: 750;
    letter-spacing: 0.15em;
    color: #65758E;
    margin-bottom: 3px;
}

.section-title {
    font-size: 24px;
    font-weight: 750;
    color: #F4F7FC;
}

.section-description {
    margin-top: 3px;
    font-size: 14px;
    color: #8996AA;
}


/* ============================================================
   KPI CARDS
   ============================================================ */

.kpi-card {
    width: 100%;
    min-height: 125px;
    height: 130px;
    box-sizing: border-box;

    background: #111A2B;

    border: 1px solid #263650;
    border-radius: 30px;

    padding: 17px 18px;

    box-shadow:
        0 5px 20px rgba(0, 0, 0, 0.20);

    transition:
        transform 0.18s ease,
        border-color 0.18s ease,
        box-shadow 0.18s ease;
}

.kpi-card:hover {
    transform: translateY(-3px);
    border-color: #3B527A;

    box-shadow:
        0 10px 28px rgba(0, 0, 0, 0.28);
}

.kpi-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.kpi-label {
    font-size: 9px;
    font-weight: 800;
    color: #F4F7FC;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.kpi-dot {
    width: 8px;
    height: 8px;
    flex-shrink: 0;
    border-radius: 50%;
    background: #4F7CFF;
    box-shadow: 0 0 10px rgba(79,124,255,0.55);
}

.kpi-value {
    margin-top: 7px;
    font-size: 35px;
    line-height: 1.05;
    font-weight: 950;
    color: #F4F7FC;
}

.kpi-help {
    margin-top: 5px;
    font-size: 11px;
    color: #718097;
}


/* ============================================================
   PANELS
   ============================================================ */

.panel {
    background: #111A2B;
    border: 1px solid #263650;
    border-radius: 15px;
    padding: 17px;

    box-shadow:
        0 5px 20px rgba(0, 0, 0, 0.16);
}


/* ============================================================
   PIPELINE
   ============================================================ */

.pipeline {
    display: flex;
    align-items: center;
    gap: 10px;

    margin: 8px 0 16px 0;

    padding: 18px 16px;

    background: #101A2B;
    border: 1px solid #263650;
    border-radius: 15px;

    overflow-x: auto;

    box-shadow:
        0 5px 18px rgba(0, 0, 0, 0.14);
}

.pipeline-step {
    min-width: 120px;
    text-align: center;
    flex: 1;
}

.pipeline-circle {
    width: 46px;
    height: 46px;

    margin: auto;

    border-radius: 50%;

    background: #172744;
    border: 1px solid #3A5D99;

    color: #79A0FF;

    display: flex;
    align-items: center;
    justify-content: center;

    font-size: 16px;
    font-weight: 800;

    box-shadow:
        0 0 0 4px rgba(79,124,255,0.05);
}

.pipeline-name {
    margin-top: 9px;

    font-size: 14px;
    font-weight: 900;

    color: #D7E0EE;

    letter-spacing: 0.04em;
}

.pipeline-status {
    margin-top: 4px;

    font-size: 10px;
    font-weight: 700;

    color: #718097;
}

.pipeline-arrow {
    color: #50627E;
    font-size: 20px;
    font-weight: 900;
    flex-shrink: 0;
}


/* ============================================================
   MATERIAL CARDS
   ============================================================ */

.material-card {
    background: #111A2B;

    border: 1px solid #263650;
    border-radius: 15px;

    padding: 19px;

    min-height: 135px;

    box-shadow:
        0 5px 20px rgba(0, 0, 0, 0.16);
}

.material-card.legacy {
    border-left: 4px solid #64748B;
}

.material-card.national {
    border-left: 4px solid #4F7CFF;
}

.material-label {
    font-size: 10px;
    font-weight: 750;

    letter-spacing: 0.12em;

    color: #8290A6;
}

.material-code {
    margin-top: 9px;

    font-size: 18px;
    font-weight: 800;

    color: #F4F7FC;
}

.material-description {
    margin-top: 7px;

    font-size: 14px;
    color: #8D9AAF;

    line-height: 1.5;
}


/* ============================================================
   DECISION
   ============================================================ */

.decision-panel {
    margin-top: 14px;

    background: #111A2B;

    border: 1px solid #263650;
    border-radius: 15px;

    padding: 17px;
}

.decision-heading {
    font-size: 10px;
    font-weight: 750;

    letter-spacing: 0.12em;

    color: #8290A6;
}

.decision-text {
    margin-top: 6px;

    font-size: 20px;
    font-weight: 800;

    color: #F4F7FC;
}


/* ============================================================
   TABLE
   ============================================================ */

[data-testid="stDataFrame"] {
    border: 1px solid #263650;
    border-radius: 11px;
    overflow: hidden;
}


/* ============================================================
   INPUTS
   ============================================================ */

.stTextInput input {
    min-height: 44px;

    border-radius: 10px;

    border: 1px solid #2A3A55 !important;

    background: #111A2B !important;
    color: #E8EDF7 !important;

    font-size: 14px !important;
}

.stTextInput input::placeholder {
    color: #65758E !important;
}

.stSelectbox [data-baseweb="select"] > div {
    min-height: 44px;

    border-radius: 10px;

    border: 1px solid #2A3A55 !important;

    background: #111A2B !important;
    color: #E8EDF7 !important;
}


/* ============================================================
   BUTTONS
   ============================================================ */

.stButton > button {
    min-height: 40px;

    border-radius: 9px;

    font-weight: 700;

    border: 1px solid #2A3A55 !important;

    background: #17243A !important;
    color: #DCE4F2 !important;

    transition:
        background 0.18s ease,
        border-color 0.18s ease,
        transform 0.18s ease;
}

.stButton > button:hover {
    background: #203250 !important;
    border-color: #42618F !important;
    color: #FFFFFF !important;

    transform: translateY(-1px);
}


/* ============================================================
   STREAMLIT HEADER
   ============================================================ */

[data-testid="stHeader"] {
    background: #0B1220 !important;
}


/* ============================================================
   FOOTER
   ============================================================ */

.footer {
    margin-top: 28px;
    padding-top: 12px;

    border-top: 1px solid #26344A;

    font-size: 10px;
    color: #66758D;

    text-align: center;
}

 /* =========================================================
       SYSTEM OVERVIEW
       ========================================================= */

    .overview-status-card {
        display: flex;
        align-items: center;
        gap: 14px;

        min-height: 78px;

        padding: 15px 18px;
        margin-bottom: 12px;

        border-radius: 12px;

        background: #111A2B;

        border: 1px solid #263650;

        transition: all 0.2s ease;
    }

    .overview-status-card:hover {
        transform: translateY(-2px);
        border-color: #3A4D6A;
    }

    .overview-status-icon {
        width: 38px;
        height: 38px;
        min-width: 38px;

        display: flex;
        align-items: center;
        justify-content: center;

        border-radius: 10px;

        font-size: 20px;
        font-weight: 800;
    }

    .overview-status-card.ready .overview-status-icon {
        background: rgba(53, 201, 139, 0.15);
        color: #35C98B;
    }

    .overview-status-card.review .overview-status-icon {
        background: rgba(242, 184, 75, 0.15);
        color: #F2B84B;
    }

    .overview-status-card.blocked .overview-status-icon {
        background: rgba(228, 91, 91, 0.15);
        color: #E45B5B;
    }

    .overview-status-content {
        flex: 1;
    }

    .overview-status-title {
        font-size: 15px;
        font-weight: 700;
        color: #F4F7FC;
        margin-bottom: 3px;
    }

    .overview-status-sub {
        font-size: 12px;
        color: #8D9AAF;
    }

    .overview-status-number {
        text-align: right;
        font-size: 25px;
        font-weight: 800;
        color: #F4F7FC;
    }

    .overview-status-number span {
        display: block;
        margin-top: 1px;
        font-size: 11px;
        font-weight: 600;
        color: #8D9AAF;
    }

    .overview-total {
        display: flex;
        align-items: center;
        justify-content: space-between;

        margin-top: 16px;
        padding: 17px 20px;

        border-radius: 12px;

        background:
            linear-gradient(
                135deg,
                rgba(79,124,255,0.16),
                rgba(56,189,248,0.07)
            );

        border: 1px solid rgba(79,124,255,0.30);
    }

    .overview-total-label {
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 1px;
        color: #8D9AAF;
    }

    .overview-total-value {
        margin-top: 3px;
        font-size: 25px;
        font-weight: 800;
        color: #F4F7FC;
    }

    .overview-total-badge {
        padding: 6px 10px;

        border-radius: 6px;

        background: rgba(79,124,255,0.15);

        color: #7EA2FF;

        font-size: 9px;
        font-weight: 800;

        letter-spacing: 0.8px;
    }
    /* =========================================================
   MATERIAL INTELLIGENCE PREVIEW
   ========================================================= */

.material-source-card,
.recommendation-card {
    min-height: 285px;

    padding: 22px;

    border-radius: 14px;

    background: #111A2B;

    border: 1px solid #263650;

    box-sizing: border-box;
}


/* ---------------------------------------------------------
   SOURCE HEADER
   --------------------------------------------------------- */

.source-header,
.recommendation-header {
    display: flex;
    align-items: center;
    justify-content: space-between;

    margin-bottom: 18px;
}

.source-label {
    font-size: 10px;
    font-weight: 800;

    letter-spacing: 1.2px;

    color: #71809A;

    margin-bottom: 5px;
}

.source-cpse {
    font-size: 17px;
    font-weight: 750;

    color: #F4F7FC;
}

.source-badge {
    padding: 6px 10px;

    border-radius: 6px;

    background: rgba(148,163,184,0.12);

    border: 1px solid rgba(148,163,184,0.20);

    color: #94A3B8;

    font-size: 9px;
    font-weight: 800;

    letter-spacing: 0.8px;
}


/* ---------------------------------------------------------
   LEGACY CODE
   --------------------------------------------------------- */

.material-code-box {
    padding: 13px 15px;

    border-radius: 9px;

    background: #0B1220;

    border: 1px solid #202D43;

    margin-bottom: 15px;
}

.field-label {
    font-size: 9px;
    font-weight: 800;

    letter-spacing: 1px;

    color: #71809A;

    margin-bottom: 5px;
}

.legacy-code {
    font-family: monospace;

    font-size: 17px;
    font-weight: 700;

    color: #AAB8CC;
}


/* ---------------------------------------------------------
   DESCRIPTION
   --------------------------------------------------------- */

.material-description {
    font-size: 16px;
    line-height: 1.5;

    font-weight: 600;

    color: #E2E8F0;

    margin-bottom: 20px;
}

.standard-description {
    padding: 14px 16px;

    border-radius: 9px;

    background: #0B1220;

    border: 1px solid #202D43;

    margin-bottom: 14px;
}

.standard-text {
    font-size: 15px;
    line-height: 1.45;

    font-weight: 600;

    color: #E2E8F0;
}


/* ---------------------------------------------------------
   SOURCE DETAILS
   --------------------------------------------------------- */

.source-details {
    display: flex;
    gap: 35px;
}

.source-detail span,
.recommendation-category span {
    display: block;

    font-size: 9px;
    font-weight: 800;

    letter-spacing: 1px;

    color: #71809A;

    margin-bottom: 4px;
}

.source-detail strong,
.recommendation-category strong {
    font-size: 13px;

    color: #B8C4D6;
}


/* ---------------------------------------------------------
   NATIONAL CODE
   --------------------------------------------------------- */

.national-code {
    font-family: monospace;

    font-size: 18px;
    font-weight: 800;

    color: #38BDF8;

    letter-spacing: 0.3px;
}

.recommendation-card {
    border-color: rgba(56,189,248,0.25);

    background:
        linear-gradient(
            145deg,
            #111A2B,
            #101C30
        );
}


/* ---------------------------------------------------------
   DECISION PILL
   --------------------------------------------------------- */

.decision-pill {
    padding: 6px 11px;

    border-radius: 20px;

    font-size: 10px;
    font-weight: 800;

    letter-spacing: 0.8px;
}

.decision-pill.match {
    color: #35C98B;
    background: rgba(53,201,139,0.13);
    border: 1px solid rgba(53,201,139,0.25);
}

.decision-pill.review {
    color: #F2B84B;
    background: rgba(242,184,75,0.13);
    border: 1px solid rgba(242,184,75,0.25);
}

.decision-pill.blocked {
    color: #E45B5B;
    background: rgba(228,91,91,0.13);
    border: 1px solid rgba(228,91,91,0.25);
}


/* ---------------------------------------------------------
   CATEGORY
   --------------------------------------------------------- */

.recommendation-category {
    margin-bottom: 16px;
}


/* ---------------------------------------------------------
   CONFIDENCE PANEL
   --------------------------------------------------------- */

.confidence-panel {
    display: flex;
    align-items: center;

    justify-content: space-between;

    gap: 20px;

    padding: 14px 16px;

    border-radius: 10px;
}

.confidence-panel.high {
    background: rgba(53,201,139,0.10);
    border: 1px solid rgba(53,201,139,0.20);
}

.confidence-panel.medium {
    background: rgba(242,184,75,0.10);
    border: 1px solid rgba(242,184,75,0.20);
}

.confidence-panel.low {
    background: rgba(228,91,91,0.10);
    border: 1px solid rgba(228,91,91,0.20);
}

.confidence-label {
    font-size: 9px;
    font-weight: 800;

    letter-spacing: 1px;

    color: #71809A;
}

.confidence-value {
    font-size: 27px;
    font-weight: 800;

    color: #F4F7FC;
}

.confidence-right {
    flex: 1;
}

.confidence-status {
    text-align: right;

    font-size: 9px;
    font-weight: 800;

    letter-spacing: 0.8px;

    color: #8D9AAF;

    margin-bottom: 7px;
}

.confidence-bar {
    height: 7px;

    width: 100%;

    border-radius: 10px;

    background: #263650;

    overflow: hidden;
}

.confidence-fill {
    height: 100%;

    border-radius: 10px;

    background: #35C98B;
}


/* ---------------------------------------------------------
   EVIDENCE CARDS
   --------------------------------------------------------- */

.evidence-card {
    min-height: 125px;

    padding: 17px;

    border-radius: 12px;

    background: #111A2B;

    border: 1px solid #263650;

    position: relative;
}

.evidence-icon {
    width: 30px;
    height: 30px;

    display: flex;
    align-items: center;
    justify-content: center;

    border-radius: 8px;

    margin-bottom: 11px;

    font-size: 16px;
    font-weight: 800;
}

.confidence-card .evidence-icon {
    color: #35C98B;
    background: rgba(53,201,139,0.13);
}

.gap-card .evidence-icon {
    color: #38BDF8;
    background: rgba(56,189,248,0.13);
}

.conflict-clear .evidence-icon {
    color: #35C98B;
    background: rgba(53,201,139,0.13);
}

.conflict-danger .evidence-icon {
    color: #E45B5B;
    background: rgba(228,91,91,0.13);
}

.evidence-label {
    font-size: 9px;
    font-weight: 800;

    letter-spacing: 1px;

    color: #71809A;
}

.evidence-value {
    font-size: 25px;
    font-weight: 800;

    color: #F4F7FC;

    margin-top: 3px;
}

.evidence-sub {
    font-size: 11px;

    color: #7F8DA3;

    margin-top: 2px;
}


/* ---------------------------------------------------------
   DECISION EXPLANATION
   --------------------------------------------------------- */

.decision-explanation {
    display: flex;

    align-items: center;
    justify-content: space-between;

    margin-top: 14px;

    padding: 15px 18px;

    border-radius: 11px;
}

.decision-explanation.match {
    background: rgba(53,201,139,0.11);
    border: 1px solid rgba(53,201,139,0.22);
}

.decision-explanation.review {
    background: rgba(242,184,75,0.11);
    border: 1px solid rgba(242,184,75,0.22);
}

.decision-explanation.blocked {
    background: rgba(228,91,91,0.11);
    border: 1px solid rgba(228,91,91,0.22);
}

.decision-main {
    display: flex;
    align-items: center;

    gap: 12px;
}

.decision-symbol {
    font-size: 20px;
    font-weight: 800;
}

.match .decision-symbol {
    color: #35C98B;
}

.review .decision-symbol {
    color: #F2B84B;
}

.blocked .decision-symbol {
    color: #E45B5B;
}

.decision-title {
    font-size: 13px;
    font-weight: 800;

    color: #F4F7FC;

    margin-bottom: 2px;
}

.decision-text {
    font-size: 12px;

    color: #8D9AAF;
}

.decision-next {
    text-align: right;

    font-size: 8px;
    font-weight: 800;

    letter-spacing: 1px;

    color: #71809A;
}

.decision-next span {
    display: block;

    margin-top: 3px;

    font-size: 11px;

    letter-spacing: 0;

    color: #9AA8BC;
}
/* ============================================================
   MATERIAL MATCHING — PREMIUM UI
   ============================================================ */

/* ---------- Page intro ---------- */

.matching-intro {
    background: linear-gradient(
        135deg,
        #14233D 0%,
        #172B4D 55%,
        #182F52 100%
    );
    border: 1px solid #29466F;
    border-radius: 14px;
    padding: 18px 22px;
    margin: 4px 0 22px 0;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.16);
}

.matching-intro-title {
    color: #F4F7FC;
    font-size: 17px;
    font-weight: 650;
    margin-bottom: 5px;
}

.matching-intro-text {
    color: #AAB7CA;
    font-size: 14px;
    line-height: 1.55;
}


/* ---------- Search area ---------- */

.matching-search-label {
    color: #CBD5E5;
    font-size: 13px;
    font-weight: 600;
    margin-bottom: 6px;
}

.matching-count {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    margin-top: 7px;
    padding: 6px 11px;
    border-radius: 20px;
    background: #111A2B;
    border: 1px solid #263650;
    color: #AAB7CA;
    font-size: 13px;
}

.matching-count strong {
    color: #38BDF8;
}


/* ---------- Main harmonization shell ---------- */

.harmonization-shell {
    background: #0F192A;
    border: 1px solid #263650;
    border-radius: 18px;
    padding: 22px;
    margin-top: 6px;
    margin-bottom: 24px;
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.18);
}

.harmonization-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}

.harmonization-title {
    color: #F4F7FC;
    font-size: 20px;
    font-weight: 750;
}

.harmonization-subtitle {
    color: #7F8EA6;
    font-size: 12px;
    margin-top: 3px;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}


/* ---------- Decision badge ---------- */

.decision-badge {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    padding: 8px 13px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 750;
    letter-spacing: 0.04em;
}

.decision-match {
    background: rgba(53, 201, 139, 0.14);
    color: #5FE0A6;
    border: 1px solid rgba(53, 201, 139, 0.35);
}

.decision-review {
    background: rgba(242, 184, 75, 0.14);
    color: #F5C86A;
    border: 1px solid rgba(242, 184, 75, 0.35);
}

.decision-no-match {
    background: rgba(228, 91, 91, 0.14);
    color: #F07878;
    border: 1px solid rgba(228, 91, 91, 0.35);
}


/* ---------- Material comparison cards ---------- */

.material-card {
    background: #111A2B;
    border: 1px solid #263650;
    border-radius: 14px;
    padding: 20px;
    min-height: 190px;
}

.material-card.legacy {
    border-top: 3px solid #9B8AFB;
}

.material-card.national {
    border-top: 3px solid #38BDF8;
}

.material-card-title {
    color: #CBD5E5;
    font-size: 12px;
    font-weight: 750;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 14px;
}

.material-card-code {
    color: #F4F7FC;
    font-size: 17px;
    font-weight: 700;
    margin-bottom: 10px;
    word-break: break-word;
}

.material-card-description {
    color: #D3DCEB;
    font-size: 14px;
    line-height: 1.5;
    margin-bottom: 14px;
}

.material-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}

.material-tag {
    background: #172238;
    border: 1px solid #2A3B58;
    color: #9FAFC5;
    padding: 5px 9px;
    border-radius: 7px;
    font-size: 11px;
}

.material-tag strong {
    color: #D9E2F0;
}


/* ---------- AI connection ---------- */

.ai-connection {
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 13px 0;
    color: #4F7CFF;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
}

.ai-connection::before,
.ai-connection::after {
    content: "";
    height: 1px;
    background: linear-gradient(
        90deg,
        transparent,
        #33496B
    );
    flex: 1;
    margin: 0 12px;
}

.ai-connection::after {
    background: linear-gradient(
        90deg,
        #33496B,
        transparent
    );
}


/* ---------- National code ---------- */

.national-code {
    background: linear-gradient(
        135deg,
        #102D2A,
        #123A34
    );
    border: 1px solid rgba(53, 201, 139, 0.28);
    border-radius: 10px;
    padding: 13px 15px;
    color: #61E2AC;
    font-family: monospace;
    font-size: 15px;
    font-weight: 700;
    margin-bottom: 14px;
}


/* ---------- AI evidence ---------- */

.evidence-shell {
    background: #0F192A;
    border: 1px solid #263650;
    border-radius: 16px;
    padding: 21px;
    margin-bottom: 24px;
}

.evidence-header {
    color: #F4F7FC;
    font-size: 20px;
    font-weight: 750;
    margin-bottom: 17px;
}

.evidence-header span {
    color: #38BDF8;
}


/* ---------- Evidence metric cards ---------- */

.evidence-metric {
    background: #111A2B;
    border: 1px solid #263650;
    border-radius: 12px;
    padding: 15px 17px;
    min-height: 105px;
}

.evidence-metric.confidence {
    border-left: 3px solid #35C98B;
}

.evidence-metric.gap {
    border-left: 3px solid #4F7CFF;
}

.evidence-metric.conflicts {
    border-left: 3px solid #E45B5B;
}

.evidence-label {
    color: #8291A8;
    font-size: 11px;
    font-weight: 650;
    text-transform: uppercase;
    letter-spacing: 0.07em;
}

.evidence-value {
    color: #F4F7FC;
    font-size: 27px;
    font-weight: 750;
    margin-top: 7px;
}

.evidence-value.green {
    color: #5FE0A6;
}

.evidence-value.blue {
    color: #65BFFF;
}

.evidence-value.red {
    color: #F07878;
}


/* ---------- Evidence status ---------- */

.evidence-status {
    border-radius: 10px;
    padding: 12px 15px;
    margin-top: 12px;
    font-size: 13px;
    font-weight: 550;
}

.evidence-status.good {
    background: rgba(53, 201, 139, 0.10);
    border: 1px solid rgba(53, 201, 139, 0.25);
    color: #A9EBCB;
}

.evidence-status.warn {
    background: rgba(242, 184, 75, 0.10);
    border: 1px solid rgba(242, 184, 75, 0.25);
    color: #F3D28C;
}

.evidence-status.bad {
    background: rgba(228, 91, 91, 0.10);
    border: 1px solid rgba(228, 91, 91, 0.25);
    color: #F3A2A2;
}


/* ---------- Attribute evidence ---------- */

.attribute-shell {
    background: #111A2B;
    border: 1px solid #263650;
    border-radius: 12px;
    overflow: hidden;
    margin-top: 12px;
}

.attribute-row {
    display: grid;
    grid-template-columns: 1.2fr 1fr 1fr 80px;
    align-items: center;
    padding: 12px 15px;
    border-bottom: 1px solid #202E45;
    font-size: 13px;
}

.attribute-row:last-child {
    border-bottom: none;
}

.attribute-header {
    background: #172238;
    color: #8291A8;
    font-size: 10px;
    font-weight: 750;
    text-transform: uppercase;
    letter-spacing: 0.07em;
}

.attribute-name {
    color: #D7E0EE;
    font-weight: 650;
}

.attribute-value {
    color: #AAB7CA;
    font-family: monospace;
}

.attribute-value.match {
    color: #5FE0A6;
}

.attribute-result {
    color: #5FE0A6;
    font-weight: 700;
    text-align: right;
}

.attribute-result.conflict {
    color: #F07878;
}


/* ---------- Evidence summary pills ---------- */

.evidence-pills {
    display: flex;
    gap: 10px;
    margin-bottom: 13px;
    flex-wrap: wrap;
}

.evidence-pill {
    padding: 7px 11px;
    border-radius: 8px;
    font-size: 11px;
    font-weight: 650;
}

.evidence-pill.matched {
    background: rgba(53, 201, 139, 0.10);
    color: #5FE0A6;
    border: 1px solid rgba(53, 201, 139, 0.25);
}

.evidence-pill.conflict {
    background: rgba(228, 91, 91, 0.10);
    color: #F07878;
    border: 1px solid rgba(228, 91, 91, 0.25);
}

.evidence-pill.unavailable {
    background: rgba(79, 124, 255, 0.10);
    color: #8FB0FF;
    border: 1px solid rgba(79, 124, 255, 0.25);
}


/* ---------- Decision ---------- */

.decision-shell {
    background: #0F192A;
    border: 1px solid #263650;
    border-radius: 16px;
    padding: 21px;
    margin-bottom: 24px;
}

.decision-header {
    color: #F4F7FC;
    font-size: 20px;
    font-weight: 750;
    margin-bottom: 16px;
}

.decision-main {
    border-radius: 13px;
    padding: 18px;
}

.decision-main.match {
    background: linear-gradient(
        135deg,
        rgba(53, 201, 139, 0.15),
        rgba(53, 201, 139, 0.06)
    );
    border: 1px solid rgba(53, 201, 139, 0.28);
}

.decision-main.review {
    background: linear-gradient(
        135deg,
        rgba(242, 184, 75, 0.15),
        rgba(242, 184, 75, 0.06)
    );
    border: 1px solid rgba(242, 184, 75, 0.28);
}

.decision-main.no-match {
    background: linear-gradient(
        135deg,
        rgba(228, 91, 91, 0.15),
        rgba(228, 91, 91, 0.06)
    );
    border: 1px solid rgba(228, 91, 91, 0.28);
}

.decision-label {
    color: #8291A8;
    font-size: 10px;
    font-weight: 750;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

.decision-value {
    color: #F4F7FC;
    font-size: 24px;
    font-weight: 800;
    margin-top: 5px;
}

.decision-explanation {
    color: #AAB7CA;
    font-size: 13px;
    margin-top: 7px;
}

.national-code-large {
    background: #111A2B;
    border: 1px solid #263650;
    border-radius: 12px;
    padding: 18px;
}

.national-code-label {
    color: #8291A8;
    font-size: 10px;
    font-weight: 750;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 8px;
}

.national-code-value {
    color: #38D0FF;
    font-family: monospace;
    font-size: 18px;
    font-weight: 750;
}


/* ---------- Interpretation ---------- */

.interpretation-box {
    background: #111A2B;
    border: 1px solid #263650;
    border-left: 3px solid #9B8AFB;
    border-radius: 10px;
    padding: 15px 17px;
    margin-top: 12px;
}

.interpretation-title {
    color: #DCE5F2;
    font-size: 13px;
    font-weight: 700;
    margin-bottom: 7px;
}

.interpretation-text {
    color: #AAB7CA;
    font-size: 13px;
    line-height: 1.6;
}


/* ---------- Details expander ---------- */

.details-label {
    color: #AAB7CA;
    font-size: 12px;
}

/* ============================================================
   ANALYTICS — PREMIUM DASHBOARD
   ============================================================ */

.analytics-hero {
    background: linear-gradient(
        135deg,
        #14233D 0%,
        #172B4D 55%,
        #182F52 100%
    );
    border: 1px solid #29466F;
    border-radius: 16px;
    padding: 20px 22px;
    margin: 4px 0 24px 0;
}

.analytics-hero-title {
    color: #F4F7FC;
    font-size: 19px;
    font-weight: 750;
    margin-bottom: 5px;
}

.analytics-hero-text {
    color: #AAB7CA;
    font-size: 13px;
    line-height: 1.55;
}

.analytics-section {
    color: #F4F7FC;
    font-size: 19px;
    font-weight: 750;
    margin-top: 25px;
    margin-bottom: 14px;
}

.analytics-section-sub {
    color: #8291A8;
    font-size: 12px;
    margin-top: -7px;
    margin-bottom: 15px;
}

.analytics-insight {
    background: #111A2B;
    border: 1px solid #263650;
    border-left: 3px solid #38BDF8;
    border-radius: 11px;
    padding: 13px 16px;
    color: #AAB7CA;
    font-size: 13px;
    line-height: 1.55;
    margin: 10px 0 18px 0;
}

.analytics-insight strong {
    color: #F4F7FC;
}

.analytics-warning {
    background: rgba(242, 184, 75, 0.08);
    border: 1px solid rgba(242, 184, 75, 0.25);
    border-left: 3px solid #F2B84B;
    border-radius: 10px;
    padding: 13px 16px;
    color: #D8C28E;
    font-size: 12px;
    line-height: 1.5;
    margin-top: 15px;
}

.analytics-stat {
    background: #111A2B;
    border: 1px solid #263650;
    border-radius: 12px;
    padding: 16px;
    min-height: 105px;
}

.analytics-stat-label {
    color: #8291A8;
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.07em;
}

.analytics-stat-value {
    color: #F4F7FC;
    font-size: 25px;
    font-weight: 750;
    margin-top: 7px;
}

.analytics-stat-help {
    color: #71819A;
    font-size: 11px;
    margin-top: 4px;
}

.analytics-stat.blue {
    border-top: 2px solid #4F7CFF;
}

.analytics-stat.green {
    border-top: 2px solid #35C98B;
}

.analytics-stat.amber {
    border-top: 2px solid #F2B84B;
}

.analytics-stat.purple {
    border-top: 2px solid #9B8AFB;
}

.analytics-card {
    background: #111A2B;
    border: 1px solid #263650;
    border-radius: 14px;
    padding: 17px;
    margin-bottom: 15px;
}

.analytics-card-title {
    color: #DCE5F2;
    font-size: 14px;
    font-weight: 700;
    margin-bottom: 3px;
}

.analytics-card-subtitle {
    color: #71819A;
    font-size: 11px;
    margin-bottom: 12px;
}

.procurement-card {
    background: linear-gradient(
        135deg,
        #111A2B,
        #132239
    );
    border: 1px solid #29466F;
    border-radius: 14px;
    padding: 18px;
    min-height: 145px;
}

.procurement-icon {
    font-size: 22px;
    margin-bottom: 8px;
}

.procurement-title {
    color: #E8EDF7;
    font-size: 14px;
    font-weight: 700;
    margin-bottom: 6px;
}

.procurement-text {
    color: #8999B0;
    font-size: 12px;
    line-height: 1.5;
}

.readiness-badge {
    display: inline-block;
    padding: 5px 9px;
    border-radius: 7px;
    font-size: 10px;
    font-weight: 700;
    background: rgba(53, 201, 139, 0.12);
    color: #5FE0A6;
    border: 1px solid rgba(53, 201, 139, 0.25);
}
/* ============================================================
   PREMIUM SIDEBAR
   ============================================================ */

/* Sidebar width */
section[data-testid="stSidebar"] {
    width: 310px !important;
    min-width: 310px !important;
    background: #091220 !important;
    border-right: 1px solid #22324A !important;
}

section[data-testid="stSidebar"] > div {
    width: 310px !important;
}


/* Sidebar spacing */
section[data-testid="stSidebar"] .block-container {
    padding: 1.35rem 1rem 1rem 1rem !important;
}


/* ============================================================
   BRAND
   ============================================================ */

.sidebar-brand {
    padding: 4px 10px 20px 10px;
    margin-bottom: 18px;

    border-bottom: 1px solid #22324A;
}

.sidebar-logo {
    width: 46px;
    height: 46px;

    display: flex;
    align-items: center;
    justify-content: center;

    margin-bottom: 13px;

    border-radius: 12px;

    background: linear-gradient(
        135deg,
        #172B4A,
        #102039
    );

    border: 1px solid #2D4770;

    font-size: 25px;

    box-shadow:
        0 8px 22px rgba(0, 0, 0, 0.25);
}


.sidebar-title {
    color: #F4F7FC;

    font-size: 21px;
    font-weight: 800;

    line-height: 1.2;

    letter-spacing: -0.4px;
}


.sidebar-subtitle {
    margin-top: 10px;

    color: #8FA0BA;

    font-size: 12px;
    font-weight: 500;

    line-height: 1.55;
}


/* ============================================================
   PLATFORM LABEL
   ============================================================ */

.sidebar-section {
    padding: 0 10px 8px 10px;

    color: #7184A3;

    font-size: 10px;
    font-weight: 800;

    letter-spacing: 1.8px;
}


/* ============================================================
   NAVIGATION
   ============================================================ */

section[data-testid="stSidebar"]
[role="radiogroup"] {

    gap: 4px !important;
}


/* Hide Streamlit radio circle */
section[data-testid="stSidebar"]
[role="radiogroup"]
label > div:first-child {

    display: none !important;
}


/* Navigation item */
section[data-testid="stSidebar"]
[role="radiogroup"]
label {

    min-height: 43px !important;

    display: flex !important;
    align-items: center !important;

    padding: 7px 12px !important;

    margin: 2px 0 !important;

    border-radius: 9px !important;

    border: 1px solid transparent !important;

    background: transparent !important;

    color: #AAB8CE !important;

    font-size: 14px !important;
    font-weight: 600 !important;

    transition:
        background 0.15s ease,
        border 0.15s ease,
        color 0.15s ease,
        transform 0.15s ease;

    cursor: pointer;
}


/* Navigation text */
section[data-testid="stSidebar"]
[role="radiogroup"]
label p {

    color: #AAB8CE !important;

    font-size: 14px !important;
    font-weight: 600 !important;
}


/* Hover */
section[data-testid="stSidebar"]
[role="radiogroup"]
label:hover {

    background: #111E31 !important;

    border-color: #213754 !important;

    transform: translateX(2px);
}


section[data-testid="stSidebar"]
[role="radiogroup"]
label:hover p {

    color: #F4F7FC !important;
}


/* ============================================================
   ACTIVE PAGE
   ============================================================ */

section[data-testid="stSidebar"]
[role="radiogroup"]
label:has(input:checked) {

    background: linear-gradient(
        90deg,
        rgba(79, 124, 255, 0.22),
        rgba(79, 124, 255, 0.08)
    ) !important;

    border-color: #31558F !important;

    box-shadow:
        inset 3px 0 0 #4F7CFF,
        0 5px 18px rgba(0, 0, 0, 0.12);
}


section[data-testid="stSidebar"]
[role="radiogroup"]
label:has(input:checked) p {

    color: #FFFFFF !important;

    font-weight: 750 !important;
}


/* ============================================================
   SYSTEM STATUS
   ============================================================ */

.sidebar-system {

    margin: 25px 0 0 0;

    padding: 14px 15px;

    border-radius: 11px;

    background: linear-gradient(
        145deg,
        #111D30,
        #0D1829
    );

    border: 1px solid #253A59;

    box-shadow:
        0 10px 25px rgba(0, 0, 0, 0.16);
}


.sidebar-system-title {

    margin-bottom: 10px;

    color: #7184A3;

    font-size: 9px;
    font-weight: 800;

    letter-spacing: 1.5px;
}


.sidebar-system-status {

    display: flex;
    align-items: center;

    gap: 7px;

    margin-bottom: 9px;

    color: #DCE6F5;

    font-size: 10px;
    font-weight: 750;
}


.status-dot {

    width: 7px;
    height: 7px;

    flex-shrink: 0;

    border-radius: 50%;

    background: #35C98B;

    box-shadow:
        0 0 8px rgba(53, 201, 139, 0.75);
}


.sidebar-system-text {

    color: #8192AD;

    font-size: 10px;

    line-height: 1.65;
}

    </style>
    """
)




# ============================================================
# LOAD DATA
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data" / "processed"

mapping_file = DATA_DIR / "cpse_material_mapping.csv"
migration_file = DATA_DIR / "migration_mapping.csv"
master_file = DATA_DIR / "national_material_master.csv"
review_file = DATA_DIR / "review_queue.csv"
audit_file = DATA_DIR / "audit_log.csv"

mapping_df = pd.read_csv(mapping_file)
migration_df = pd.read_csv(migration_file)
master_df = pd.read_csv(master_file)
review_df = pd.read_csv(review_file)
audit_df = pd.read_csv(audit_file)


# ============================================================
# HEADER
# ============================================================

st.html(
    """
    <div class="page-kicker">
        NATIONAL MATERIAL INTELLIGENCE PLATFORM
    </div>

    <div class="page-title">
        National Material Harmonization
    </div>

    <div class="page-subtitle">
        AI-driven standardization and harmonization of material codes,
        technical specifications and legacy records across CPSEs.
    </div>

    <div class="demo-pill">
        ● DEMONSTRATION ENVIRONMENT
    </div>
    """
)

# ============================================================
# KPI CALCULATIONS
# ============================================================

total_materials = len(mapping_df)
national_materials = len(master_df)

auto_mapped = (
    migration_df["migration_status"] == "MIGRATION_READY"
).sum()

review_required = (
    migration_df["migration_status"] == "REVIEW_REQUIRED"
).sum()

blocked = (
    migration_df["migration_status"] == "BLOCKED"
).sum()

cpse_count = mapping_df["cpse"].nunique()


# ============================================================
# KPI CARDS
# ============================================================

col1, col2, col3, col4, col5 = st.columns(5)

def kpi(label, value, help_text):
    st.html(
        f"""
        <div class="kpi-card">
            <div class="kpi-top">
                <div class="kpi-label">{label}</div>
                <div class="kpi-dot"></div>
            </div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-help">{help_text}</div>
        </div>
        """
    )

with col1:
    kpi(
        "CPSE Records",
        f"{total_materials:,}",
        "Legacy material records"
    )

with col2:
    kpi(
        "National Materials",
        f"{national_materials:,}",
        "Standardized material"
    )

with col3:
    kpi(
        "Auto Mapped",
        f"{auto_mapped:,}",
        "Ready for migration"
    )

with col4:
    kpi(
        "Review Required",
        f"{review_required:,}",
        "Human validation queue"
    )

with col5:
    kpi(
        "Blocked",
        f"{blocked:,}",
        "Requires resolution"
    )

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.html(
        """
        <div class="sidebar-brand">

            <div class="sidebar-logo">
                🏭
            </div>

            <div class="sidebar-title">
                National Material<br>
                Intelligence
            </div>

            <div class="sidebar-subtitle">
                AI-driven standardization<br>
                across CPSE material masters
            </div>

        </div>

        <div class="sidebar-section">
            PLATFORM
        </div>
        """
    )

    page = st.radio(
        "Select Module",
        [
            "Dashboard",
            "Material Matching",
            "Review & Approval",
            "National Material Master",
            "Legacy Migration",
            "Analytics",
            "Audit Trail"
        ],
        label_visibility="collapsed"
    )

    st.html(
        """
        <div class="sidebar-system">

            <div class="sidebar-system-title">
                SYSTEM STATUS
            </div>

            <div class="sidebar-system-status">
                <span class="status-dot"></span>
                ALL SYSTEMS OPERATIONAL
            </div>

            <div class="sidebar-system-text">
                Matching Engine • Attribute Engine<br>
                National Master • Migration Layer
            </div>

        </div>
        """
    )
# ============================================================
# DASHBOARD
# ============================================================

if page == "Dashboard":

    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    st.html(
        """
        <div class="page-kicker">
            SYSTEM OVERVIEW
        </div>

        <div class="page-title">
            Command Center
        </div>

        <div class="page-subtitle">
            Monitor material harmonization, matching decisions and
            migration readiness across participating CPSEs.
        </div>
        """
    )
    # --------------------------------------------------------
    # SYSTEM STATUS
    # --------------------------------------------------------

    col1, col2 = st.columns([3, 1])

    with col1:
        st.html(
            """
            <div class="section-wrap">
                <div class="section-kicker">
                    PROCESS MONITOR
                </div>

                <div class="section-title">
                    Material Harmonization Pipeline
                </div>

                <div class="section-description">
                    From legacy CPSE records to validated national material codes.
                </div>
            </div>
            """
        )
    with col2:
        st.success("● SYSTEM READY")

    st.html(
        """
        <div class="pipeline">

            <div class="pipeline-step">
                <div class="pipeline-circle">01</div>
                <div class="pipeline-name">CPSE DATA</div>
                <div class="pipeline-status">INGESTED</div>
            </div>

            <div class="pipeline-arrow">→</div>

            <div class="pipeline-step">
                <div class="pipeline-circle">02</div>
                <div class="pipeline-name">NORMALIZE</div>
                <div class="pipeline-status">STANDARDIZED</div>
            </div>

            <div class="pipeline-arrow">→</div>

            <div class="pipeline-step">
                <div class="pipeline-circle">03</div>
                <div class="pipeline-name">ATTRIBUTES</div>
                <div class="pipeline-status">EXTRACTED</div>
            </div>

            <div class="pipeline-arrow">→</div>

            <div class="pipeline-step">
                <div class="pipeline-circle">04</div>
                <div class="pipeline-name">AI MATCHING</div>
                <div class="pipeline-status">ANALYZED</div>
            </div>

            <div class="pipeline-arrow">→</div>

            <div class="pipeline-step">
                <div class="pipeline-circle">05</div>
                <div class="pipeline-name">VALIDATION</div>
                <div class="pipeline-status">REVIEWED</div>
            </div>

            <div class="pipeline-arrow">→</div>

            <div class="pipeline-step">
                <div class="pipeline-circle">06</div>
                <div class="pipeline-name">NATIONAL CODE</div>
                <div class="pipeline-status">HARMONIZED</div>
            </div>

            <div class="pipeline-arrow">→</div>

            <div class="pipeline-step">
                <div class="pipeline-circle">07</div>
                <div class="pipeline-name">MIGRATION</div>
                <div class="pipeline-status">CONTROLLED</div>
            </div>

        </div>
        """
    )

    st.divider()

    

    # --------------------------------------------------------
    # INTERACTIVE EXPLORER
    # --------------------------------------------------------

    st.html(
        """
        <div class="section-wrap">
            <div class="section-kicker">
                MATERIAL EXPLORER
            </div>

            <div class="section-title">
                Explore Material Records
            </div>

            <div class="section-description">
                Search, filter and inspect harmonization recommendations
                generated by the matching engine.
            </div>
        </div>
        """
    )

    filter_col1, filter_col2, filter_col3 = st.columns(3)

    with filter_col1:
        cpse_filter = st.selectbox(
            "CPSE",
            ["All"] + sorted(
                mapping_df["cpse"].dropna().unique().tolist()
            )
        )

    with filter_col2:
        category_filter = st.selectbox(
            "Category",
            ["All"] + sorted(
                mapping_df["category"].dropna().unique().tolist()
            )
        )

    with filter_col3:
        status_filter = st.selectbox(
            "Migration Status",
            [
                "All",
                "MIGRATION_READY",
                "REVIEW_REQUIRED",
                "BLOCKED"
            ]
        )

    search = st.text_input(
        "Search material",
        placeholder="Search description, CPSE code or National Material Code..."
    )

    explorer = mapping_df.copy()

    if cpse_filter != "All":
        explorer = explorer[
            explorer["cpse"] == cpse_filter
        ]

    if category_filter != "All":
        explorer = explorer[
            explorer["category"] == category_filter
        ]

    if status_filter != "All":
        status_records = migration_df[
            migration_df["migration_status"] == status_filter
        ]["record_id"]

        explorer = explorer[
            explorer["record_id"].isin(status_records)
        ]

    if search:
        search_value = search.lower()

        search_mask = (
            explorer["cpse_description"]
            .fillna("")
            .astype(str)
            .str.lower()
            .str.contains(search_value, regex=False)
            |
            explorer["cpse_material_code"]
            .fillna("")
            .astype(str)
            .str.lower()
            .str.contains(search_value, regex=False)
            |
            explorer["national_material_code"]
            .fillna("")
            .astype(str)
            .str.lower()
            .str.contains(search_value, regex=False)
        )

        explorer = explorer[search_mask]

    st.caption(
        f"Showing **{len(explorer)}** of **{total_materials}** records"
    )

    # --------------------------------------------------------
    # MATERIAL CARDS
    # --------------------------------------------------------

    if len(explorer) > 0:

        display_columns = [
            "record_id",
            "cpse",
            "cpse_material_code",
            "cpse_description",
            "national_material_code",
            "confidence",
            "final_decision"
        ]

        display_df = explorer[display_columns].copy()

        display_df["confidence"] = (
            display_df["confidence"]
            .round(1)
            .astype(str)
            + "%"
        )

        display_df.columns = [
            "Record",
            "CPSE",
            "Legacy Code",
            "Material Description",
            "National Code",
            "Confidence",
            "Decision"
        ]

        st.dataframe(
            display_df.head(25),
            use_container_width=True,
            hide_index=True
        )

        st.caption(
            "Select a record below to inspect the complete harmonization reasoning."
        )

        # ----------------------------------------------------
        # INTERACTIVE MATERIAL SELECTION
        # ----------------------------------------------------

        selected_record = st.selectbox(
            "Inspect Material",
            explorer["record_id"].tolist(),
            format_func=lambda x: (
                f"Record {x} — "
                f"{explorer.loc[explorer['record_id'] == x, 'cpse_description'].iloc[0]}"
            )
        )

        selected = explorer[
            explorer["record_id"] == selected_record
        ].iloc[0]

        st.divider()

# ========================================================
# MATERIAL INTELLIGENCE PREVIEW
# ========================================================

        st.subheader("🧠 Material Intelligence Preview")

        preview_col1, preview_col2 = st.columns([1, 1])


        # ========================================================
        # LEFT — LEGACY MATERIAL
        # ========================================================

        with preview_col1:

            st.markdown("#### Legacy CPSE Material")

            st.html(
                f"""
                <div class="material-source-card">

                    <div class="source-header">
                        <div>
                            <div class="source-label">SOURCE RECORD</div>
                            <div class="source-cpse">
                                {selected["cpse"]}
                            </div>
                        </div>

                        <div class="source-badge">
                            LEGACY
                        </div>
                    </div>

                    <div class="material-code-box">
                        <div class="field-label">LEGACY MATERIAL CODE</div>
                        <div class="legacy-code">
                            {selected["cpse_material_code"]}
                        </div>
                    </div>

                    <div class="material-description">
                        {selected["cpse_description"]}
                    </div>

                    <div class="source-details">

                        <div class="source-detail">
                            <span>UOM</span>
                            <strong>{selected["cpse_uom"]}</strong>
                        </div>

                        <div class="source-detail">
                            <span>CATEGORY</span>
                            <strong>{selected["category"]}</strong>
                        </div>

                    </div>

                </div>
                """
            )


        # ========================================================
        # RIGHT — NATIONAL RECOMMENDATION
        # ========================================================

        with preview_col2:

            st.markdown("#### National Recommendation")

            confidence = float(selected["confidence"])
            confidence_gap = float(selected["confidence_gap"])
            conflicts = int(selected["conflict_count"])

            confidence_class = (
                "high"
                if confidence >= 85
                else "medium"
                if confidence >= 60
                else "low"
            )

            decision = str(selected["final_decision"])

            decision_class = {
                "MATCH": "match",
                "REVIEW": "review",
                "NO_MATCH": "blocked"
            }.get(decision, "review")

            st.html(
                f"""
                <div class="recommendation-card">

                    <div class="recommendation-header">

                        <div>
                            <div class="source-label">
                                RECOMMENDED NATIONAL MATERIAL
                            </div>

                            <div class="national-code">
                                {selected["national_material_code"]}
                            </div>
                        </div>

                        <div class="decision-pill {decision_class}">
                            {decision}
                        </div>

                    </div>

                    <div class="standard-description">
                        <div class="field-label">
                            STANDARD DESCRIPTION
                        </div>

                        <div class="standard-text">
                            {selected["canonical_description"]}
                        </div>
                    </div>

                    <div class="recommendation-category">
                        <span>CATEGORY</span>
                        <strong>{selected["category"]}</strong>
                    </div>

                    <div class="confidence-panel {confidence_class}">

                        <div class="confidence-left">

                            <div class="confidence-label">
                                MATCH CONFIDENCE
                            </div>

                            <div class="confidence-value">
                                {confidence:.1f}%
                            </div>

                        </div>

                        <div class="confidence-right">
                            <div class="confidence-status">
                                {"HIGH CONFIDENCE" if confidence >= 85
                                else "MEDIUM CONFIDENCE" if confidence >= 60
                                else "LOW CONFIDENCE"}
                            </div>

                            <div class="confidence-bar">
                                <div
                                    class="confidence-fill"
                                    style="width:{min(confidence, 100)}%"
                                ></div>
                            </div>
                        </div>

                    </div>

                </div>
                """
            )


        # ========================================================
        # MATCHING EVIDENCE
        # ========================================================

        st.markdown("#### 🔍 Matching Evidence")

        evidence_col1, evidence_col2, evidence_col3 = st.columns(3)


        with evidence_col1:

            st.html(
                f"""
                <div class="evidence-card confidence-card">

                    <div class="evidence-icon">✓</div>

                    <div class="evidence-label">
                        CONFIDENCE
                    </div>

                    <div class="evidence-value">
                        {confidence:.1f}%
                    </div>

                    <div class="evidence-sub">
                        Overall match score
                    </div>

                </div>
                """
            )


        with evidence_col2:

            st.html(
                f"""
                <div class="evidence-card gap-card">

                    <div class="evidence-icon">↕</div>

                    <div class="evidence-label">
                        CONFIDENCE GAP
                    </div>

                    <div class="evidence-value">
                        {confidence_gap:.1f}%
                    </div>

                    <div class="evidence-sub">
                        Best vs second candidate
                    </div>

                </div>
                """
            )


        with evidence_col3:

            conflict_label = (
                "No conflicts detected"
                if conflicts == 0
                else f"{conflicts} technical conflict"
                + ("s" if conflicts != 1 else "")
            )

            st.html(
                f"""
                <div class="evidence-card {
                    "conflict-clear" if conflicts == 0 else "conflict-danger"
                }">

                    <div class="evidence-icon">
                        {"✓" if conflicts == 0 else "!"}
                    </div>

                    <div class="evidence-label">
                        TECHNICAL CONFLICTS
                    </div>

                    <div class="evidence-value">
                        {conflicts}
                    </div>

                    <div class="evidence-sub">
                        {conflict_label}
                    </div>

                </div>
                """
            )


        # ========================================================
        # DECISION EXPLANATION
        # ========================================================

        decision_messages = {
            "MATCH": (
                "MATCH",
                "Suitable for automated harmonization."
            ),
            "REVIEW": (
                "REVIEW",
                "Requires human validation before harmonization."
            ),
            "NO_MATCH": (
                "BLOCKED",
                "Technical conflicts prevent automatic harmonization."
            )
        }

        decision_title, decision_text = decision_messages.get(
            decision,
            ("REVIEW", "Requires human validation.")
        )

        st.html(
            f"""
            <div class="decision-explanation {decision_class}">

                <div class="decision-main">

                    <div class="decision-symbol">
                        {"✓" if decision == "MATCH"
                        else "!" if decision == "REVIEW"
                        else "×"}
                    </div>

                    <div>
                        <div class="decision-title">
                            {decision_title}
                        </div>

                        <div class="decision-text">
                            {decision_text}
                        </div>
                    </div>

                </div>

                <div class="decision-next">
                    NEXT
                    <span>View detailed evidence →</span>
                </div>

            </div>
            """
        )


# --------------------------------------------------------
# SYSTEM OVERVIEW
# --------------------------------------------------------

    st.subheader("📊 System Overview")

    total_records = auto_mapped + review_required + blocked

    ready_pct = (
        auto_mapped / total_records * 100
        if total_records > 0 else 0
    )

    review_pct = (
        review_required / total_records * 100
        if total_records > 0 else 0
    )

    blocked_pct = (
        blocked / total_records * 100
        if total_records > 0 else 0
    )


    overview_col1, overview_col2 = st.columns([1.15, 1])


    # ========================================================
    # LEFT — READINESS
    # ========================================================

    with overview_col1:

        st.markdown("#### Migration Readiness")

        fig = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=ready_pct,
                number={
                    "suffix": "%",
                    "font": {
                        "size": 42,
                        "color": TEXT_MAIN
                    }
                },
                title={
                    "text": "Records Ready for Migration",
                    "font": {
                        "size": 15,
                        "color": TEXT_MUTED
                    }
                },
                gauge={
                    "axis": {
                        "range": [0, 100],
                        "tickwidth": 0,
                        "tickcolor": "rgba(0,0,0,0)",
                        "tickfont": {
                            "color": TEXT_MUTED
                        }
                    },
                    "bar": {
                        "color": COLOR_GREEN,
                        "thickness": 0.28
                    },
                    "bgcolor": "#1A2638",
                    "borderwidth": 0,
                    "steps": [
                        {
                            "range": [0, 70],
                            "color": "#182335"
                        },
                        {
                            "range": [70, 90],
                            "color": "#1D2B3E"
                        },
                        {
                            "range": [90, 100],
                            "color": "#203244"
                        }
                    ]
                }
            )
        )

        fig.update_layout(
            height=300,
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(
                l=25,
                r=25,
                t=35,
                b=10
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False}
        )

        st.caption(
            f"{auto_mapped} of {total_records} records currently meet "
            "migration-readiness criteria."
        )


    # ========================================================
    # RIGHT — STATUS BREAKDOWN
    # ========================================================

    with overview_col2:

        st.markdown("#### Migration Status")

        # ----------------------------
        # Migration Ready
        # ----------------------------

        st.html(
            f"""
            <div class="overview-status-card ready">
                <div class="overview-status-icon">✓</div>
                <div class="overview-status-content">
                    <div class="overview-status-title">
                        Migration Ready
                    </div>
                    <div class="overview-status-sub">
                        Cleared for migration
                    </div>
                </div>
                <div class="overview-status-number">
                    {auto_mapped}
                    <span>{ready_pct:.1f}%</span>
                </div>
            </div>
            """
        )

        # ----------------------------
        # Review Required
        # ----------------------------

        st.html(
            f"""
            <div class="overview-status-card review">
                <div class="overview-status-icon">!</div>
                <div class="overview-status-content">
                    <div class="overview-status-title">
                        Review Required
                    </div>
                    <div class="overview-status-sub">
                        Awaiting human validation
                    </div>
                </div>
                <div class="overview-status-number">
                    {review_required}
                    <span>{review_pct:.1f}%</span>
                </div>
            </div>
            """
        )

        # ----------------------------
        # Blocked
        # ----------------------------

        st.html(
            f"""
            <div class="overview-status-card blocked">
                <div class="overview-status-icon">×</div>
                <div class="overview-status-content">
                    <div class="overview-status-title">
                        Blocked
                    </div>
                    <div class="overview-status-sub">
                        Technical conflict detected
                    </div>
                </div>
                <div class="overview-status-number">
                    {blocked}
                    <span>{blocked_pct:.1f}%</span>
                </div>
            </div>
            """
        )

        st.html(
            f"""
            <div class="overview-total">
                <div>
                    <div class="overview-total-label">
                        TOTAL MATERIAL RECORDS
                    </div>
                    <div class="overview-total-value">
                        {total_records}
                    </div>
                </div>

                <div class="overview-total-badge">
                    DEMO DATASET
                </div>
            </div>
            """
        )

    # --------------------------------------------------------
    # DEMO HINT
    # --------------------------------------------------------

    st.divider()

    st.info(
        "💡 **Demo tip:** Select a CPSE, category or migration status "
        "above, then choose a material to demonstrate how the system "
        "moves from a legacy CPSE description to a National Material Code."
    )




# ============================================================
# MATERIAL MATCHING
# ============================================================

# ============================================================
# MATERIAL MATCHING
# ============================================================

elif page == "Material Matching":

    st.header("🔎 Material Matching")

    # ========================================================
    # INTRODUCTION
    # ========================================================

    st.html(
        """
        <div class="matching-intro">

            <div class="matching-intro-title">
                AI-powered material harmonization workspace
            </div>

            <div class="matching-intro-text">
                Compare legacy CPSE materials against the National
                Material Master using description similarity,
                technical attributes, confidence scoring, and
                conflict detection.
            </div>

        </div>
        """
    )

    # ========================================================
    # SEARCH
    # ========================================================

    search = st.text_input(
        "🔍 Search material description or CPSE material code",
        placeholder="Example: SS304, CPSEB-112038, gate valve..."
    )

    filtered = mapping_df.copy()

    if search:

        search_lower = search.lower()

        mask = (
            filtered["cpse_description"]
            .fillna("")
            .astype(str)
            .str.lower()
            .str.contains(search_lower, regex=False)
            |
            filtered["cpse_material_code"]
            .fillna("")
            .astype(str)
            .str.lower()
            .str.contains(search_lower, regex=False)
        )

        filtered = filtered[mask]

    st.html(
        f"""
        <div class="matching-count">
            <span>●</span>
            <span>Matching records:</span>
            <strong>{len(filtered)}</strong>
        </div>
        """
    )

    # ========================================================
    # MATERIAL SELECTOR
    # ========================================================

    if len(filtered) > 0:

        selected_record = st.selectbox(
            "Select a material to inspect",
            filtered["record_id"].tolist()
        )

        selected = filtered[
            filtered["record_id"] == selected_record
        ].iloc[0]

        # ====================================================
        # PREPARE VALUES
        # ====================================================

        confidence = float(selected["confidence"])
        confidence_gap = float(selected["confidence_gap"])
        conflict_count = int(selected["conflict_count"])

        decision = (
            str(selected["final_decision"])
            .upper()
            .replace("_", " ")
        )

        # Decision styling
        if decision == "MATCH":

            decision_class = "decision-match"
            decision_main_class = "match"
            decision_icon = "✓"
            decision_text = "Suitable for automated harmonization."

        elif decision == "REVIEW":

            decision_class = "decision-review"
            decision_main_class = "review"
            decision_icon = "!"
            decision_text = "Human validation recommended before migration."

        else:

            decision_class = "decision-no-match"
            decision_main_class = "no-match"
            decision_icon = "×"
            decision_text = "Material should not be automatically harmonized."

        # ====================================================
        # MATERIAL HARMONIZATION
        # ====================================================

        st.html(
            f"""
            <div class="harmonization-shell">

                <div class="harmonization-header">

                    <div>
                        <div class="harmonization-title">
                            📦 Material Harmonization
                        </div>

                        <div class="harmonization-subtitle">
                            Legacy material → National standard
                        </div>
                    </div>

                    <div class="decision-badge {decision_class}">
                        {decision_icon} {decision}
                    </div>

                </div>

                <div class="material-card legacy">

                    <div class="material-card-title">
                        Legacy CPSE Material
                    </div>

                    <div class="material-card-code">
                        {selected["cpse_material_code"]}
                    </div>

                    <div class="material-card-description">
                        {selected["cpse_description"]}
                    </div>

                    <div class="material-meta">

                        <div class="material-tag">
                            <strong>CPSE</strong>&nbsp;
                            {selected["cpse"]}
                        </div>

                        <div class="material-tag">
                            <strong>UOM</strong>&nbsp;
                            {selected["cpse_uom"]}
                        </div>

                    </div>

                </div>

                <div class="ai-connection">
                    ✦ AI HARMONIZATION ✦
                </div>

                <div class="material-card national">

                    <div class="material-card-title">
                        National Standard
                    </div>

                    <div class="national-code">
                        {selected["national_material_code"]}
                    </div>

                    <div class="material-card-description">
                        {selected["canonical_description"]}
                    </div>

                    <div class="material-meta">

                        <div class="material-tag">
                            <strong>Category</strong>&nbsp;
                            {selected["category"]}
                        </div>

                    </div>

                </div>

            </div>
            """
        )

        # ====================================================
        # AI MATCHING EVIDENCE
        # ====================================================

        st.html(
            """
            <div class="evidence-shell">

                <div class="evidence-header">
                    🤖 <span>AI</span> Matching Evidence
                </div>

            </div>
            """
        )

        metric_col1, metric_col2, metric_col3 = st.columns(3)

        with metric_col1:

            confidence_color = (
                "green"
                if confidence >= 90
                else "blue"
                if confidence >= 75
                else "red"
            )

            st.html(
                f"""
                <div class="evidence-metric confidence">

                    <div class="evidence-label">
                        Confidence
                    </div>

                    <div class="evidence-value {confidence_color}">
                        {confidence:.1f}%
                    </div>

                </div>
                """
            )

        with metric_col2:

            st.html(
                f"""
                <div class="evidence-metric gap">

                    <div class="evidence-label">
                        Confidence Gap
                    </div>

                    <div class="evidence-value blue">
                        {confidence_gap:.1f}%
                    </div>

                </div>
                """
            )

        with metric_col3:

            conflict_color = (
                "green"
                if conflict_count == 0
                else "red"
            )

            st.html(
                f"""
                <div class="evidence-metric conflicts">

                    <div class="evidence-label">
                        Technical Conflicts
                    </div>

                    <div class="evidence-value {conflict_color}">
                        {conflict_count}
                    </div>

                </div>
                """
            )

        # ====================================================
        # CONFIDENCE INTERPRETATION
        # ====================================================

        if confidence >= 90:

            st.html(
                """
                <div class="evidence-status good">
                    ● <strong>High-confidence recommendation</strong>
                    — strong evidence supports this harmonization.
                </div>
                """
            )

        elif confidence >= 75:

            st.html(
                """
                <div class="evidence-status warn">
                    ● <strong>Moderate-confidence recommendation</strong>
                    — validate before migration.
                </div>
                """
            )

        else:

            st.html(
                """
                <div class="evidence-status bad">
                    ● <strong>Low-confidence recommendation</strong>
                    — human validation is required.
                </div>
                """
            )

        if conflict_count > 0:

            st.html(
                f"""
                <div class="evidence-status bad">
                    ⚠ <strong>{conflict_count} technical conflict(s)</strong>
                    detected between the legacy and national material.
                </div>
                """
            )

        else:

            st.html(
                """
                <div class="evidence-status good">
                    ✓ <strong>No technical conflicts detected.</strong>
                </div>
                """
            )

        # ====================================================
        # ATTRIBUTE LEVEL EVIDENCE
        # ====================================================

        st.html(
            """
            <div class="evidence-header" style="margin-top:28px;">
                🔬 Attribute-Level Evidence
            </div>
            """
        )

        try:

            evidence = json.loads(
                selected["attribute_evidence"]
            )

            matched = [
                item for item in evidence
                if item["status"] == "MATCH"
            ]

            conflicts = [
                item for item in evidence
                if item["status"] == "CONFLICT"
            ]

            unavailable = [
                item for item in evidence
                if item["status"] == "NOT_AVAILABLE"
            ]

            # ----------------------------------------------
            # SUMMARY
            # ----------------------------------------------

            st.html(
                f"""
                <div class="evidence-pills">

                    <div class="evidence-pill matched">
                        ✓ {len(matched)} Matched
                    </div>

                    <div class="evidence-pill conflict">
                        ⚠ {len(conflicts)} Conflicts
                    </div>

                    <div class="evidence-pill unavailable">
                        — {len(unavailable)} Not Available
                    </div>

                </div>
                """
            )

            # ----------------------------------------------
            # MATCHED ATTRIBUTES
            # ----------------------------------------------

            if matched:

                rows = ""

                for item in matched:

                    critical = (
                        " • Critical"
                        if item["critical"]
                        else ""
                    )

                    rows += f"""
                    <div class="attribute-row">

                        <div class="attribute-name">
                            {item["attribute"]}{critical}
                        </div>

                        <div class="attribute-value match">
                            {item["record_value"]}
                        </div>

                        <div class="attribute-value match">
                            {item["canonical_value"]}
                        </div>

                        <div class="attribute-result">
                            ✓ MATCH
                        </div>

                    </div>
                    """

                st.html(
                    f"""
                    <div class="attribute-shell">

                        <div class="attribute-row attribute-header">

                            <div>Attribute</div>
                            <div>Legacy</div>
                            <div>National</div>
                            <div>Result</div>

                        </div>

                        {rows}

                    </div>
                    """
                )

            # ----------------------------------------------
            # CONFLICTING ATTRIBUTES
            # ----------------------------------------------

            if conflicts:

                conflict_rows = ""

                for item in conflicts:

                    critical = (
                        " • Critical"
                        if item["critical"]
                        else ""
                    )

                    conflict_rows += f"""
                    <div class="attribute-row">

                        <div class="attribute-name">
                            {item["attribute"]}{critical}
                        </div>

                        <div class="attribute-value">
                            {item["record_value"]}
                        </div>

                        <div class="attribute-value">
                            {item["canonical_value"]}
                        </div>

                        <div class="attribute-result conflict">
                            ⚠ CONFLICT
                        </div>

                    </div>
                    """

                st.html(
                    f"""
                    <div style="margin-top:14px;">

                        <div class="attribute-shell">

                            <div class="attribute-row attribute-header">

                                <div>Attribute</div>
                                <div>Legacy</div>
                                <div>National</div>
                                <div>Result</div>

                            </div>

                            {conflict_rows}

                        </div>

                    </div>
                    """
                )

            # ----------------------------------------------
            # UNAVAILABLE ATTRIBUTES
            # ----------------------------------------------

            if unavailable:

                with st.expander(
                    f"View {len(unavailable)} unavailable attributes"
                ):

                    for item in unavailable:

                        st.write(
                            f"— **{item['attribute']}**"
                        )

        except Exception:

            st.warning(
                "Attribute-level evidence is not available "
                "for this matching record."
            )

        # ====================================================
        # HARMONIZATION DECISION
        # ====================================================

        st.html(
            """
            <div class="decision-header" style="margin-top:30px;">
                🎯 Harmonization Decision
            </div>
            """
        )

        decision_col1, decision_col2 = st.columns(
            [1.2, 1]
        )

        with decision_col1:

            st.html(
                f"""
                <div class="decision-main {decision_main_class}">

                    <div class="decision-label">
                        Final Decision
                    </div>

                    <div class="decision-value">
                        {decision_icon} {decision}
                    </div>

                    <div class="decision-explanation">
                        {decision_text}
                    </div>

                </div>
                """
            )

        with decision_col2:

            st.html(
                f"""
                <div class="national-code-large">

                    <div class="national-code-label">
                        National Material Code
                    </div>

                    <div class="national-code-value">
                        {selected["national_material_code"]}
                    </div>

                </div>
                """
            )

        # ====================================================
        # MATCHING INTERPRETATION
        # ====================================================

        interpretation = []

        if confidence >= 90:

            interpretation.append(
                "Strong overall similarity was found between "
                "the legacy material and the recommended national material."
            )

        elif confidence >= 75:

            interpretation.append(
                "The system identified a reasonable candidate, "
                "but validation is recommended before migration."
            )

        else:

            interpretation.append(
                "The recommendation does not have sufficient "
                "confidence for automatic migration."
            )

        if conflict_count > 0:

            interpretation.append(
                "Technical attribute conflicts were detected "
                "and require authorized review."
            )

        else:

            interpretation.append(
                "No conflicting technical attributes were detected."
            )

        st.html(
            f"""
            <div class="interpretation-box">

                <div class="interpretation-title">
                    ⚙ Matching Interpretation
                </div>

                <div class="interpretation-text">

                    • {interpretation[0]}<br><br>
                    • {interpretation[1]}

                </div>

            </div>
            """
        )

        # ====================================================
        # COMPLETE RECORD
        # ====================================================

        with st.expander(
            "📋 View Complete Matching Record"
        ):

            st.dataframe(
                selected.to_frame().T,
                use_container_width=True,
                hide_index=True
            )

    else:

        st.warning(
            "No materials found matching your search."
        )

# ============================================================
# REVIEW & APPROVAL
# ============================================================

elif page == "Review & Approval":

    st.header("👤 Human Review & Approval")

    st.info(
        "AI recommendations with uncertainty or conflicts require "
        "human validation before migration."
    )

    st.write(
        f"Records awaiting review: **{len(review_df)}**"
    )

    if len(review_df) == 0:
        st.success("🎉 No materials are currently awaiting review.")

    else:

        # ----------------------------------------------------
        # Select material
        # ----------------------------------------------------

        review_options = review_df["record_id"].tolist()

        selected_record = st.selectbox(
            "Select a material to review",
            review_options
        )

        selected = review_df[
            review_df["record_id"] == selected_record
        ].iloc[0]

        st.divider()

        # ----------------------------------------------------
        # Material Information
        # ----------------------------------------------------

        st.subheader("📦 Material Information")

        col1, col2 = st.columns(2)

        with col1:

            st.write("**Record ID**")
            st.write(selected["record_id"])

            st.write("**CPSE**")
            st.write(selected["cpse"])

            st.write("**Legacy Material Code**")
            st.write(selected["cpse_material_code"])

            st.write("**Original Description**")
            st.write(selected["cpse_description"])

            st.write("**UOM**")
            st.write(selected["cpse_uom"])

        with col2:

            st.write("**AI Recommended National Code**")
            st.success(selected["national_material_code"])

            st.write("**Standardized Description**")
            st.write(selected["canonical_description"])

            st.write("**Category**")
            st.write(selected["category"])

            st.write("**Migration Status**")
            st.write(selected["migration_status"])

            st.write("**Priority**")
            st.write(selected["priority"])

        st.divider()

        # ----------------------------------------------------
        # AI Matching Evidence
        # ----------------------------------------------------

        st.subheader("🔍 AI Matching Evidence")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "AI Confidence",
                f"{selected['confidence']:.2f}%"
            )

        with col2:

            st.metric(
                "Confidence Gap",
                f"{selected['confidence_gap']:.2f}%"
            )

        with col3:

            st.metric(
                "Technical Conflicts",
                int(selected["conflict_count"])
            )

        if int(selected["conflict_count"]) > 0:

            st.warning(
                f"⚠️ {int(selected['conflict_count'])} technical "
                "conflict(s) detected. Verify the recommendation carefully."
            )

        else:

            st.success(
                "✅ No technical conflicts detected."
            )

        st.divider()

        # ----------------------------------------------------
        # Human Decision
        # ----------------------------------------------------

        st.subheader("✍️ Reviewer Decision")

        decision = st.radio(
            "Decision",
            ["Approve", "Reject"],
            horizontal=True
        )

        reviewer = st.text_input(
            "Reviewer Name",
            placeholder="Enter reviewer name"
        )

        comment = st.text_area(
            "Review Comment",
            placeholder="Explain the reason for your decision..."
        )

        if st.button(
            "Submit Decision",
            type="primary",
            use_container_width=True
        ):

            if not reviewer.strip():

                st.error(
                    "Please enter the reviewer name."
                )

            elif not comment.strip():

                st.error(
                    "Please enter a review comment."
                )

            else:

                # Load latest review decision store
                decisions_file = (
                    DATA_DIR / "review_decisions.csv"
                )

                decisions_df = pd.read_csv(
                    decisions_file,
                    dtype={
                        "decision": "string",
                        "reviewer": "string",
                        "review_comment": "string",
                        "decision_timestamp": "string"
                    }
                )
                # Ensure editable text columns use string dtype
                for column in [
                    "decision",
                    "reviewer",
                    "review_comment",
                    "decision_timestamp"
                ]:
                    if column in decisions_df.columns:
                        decisions_df[column] = decisions_df[column].astype("string")

                # ------------------------------------------------
                # Save human decision
                # ------------------------------------------------

                mask = (
                    decisions_df["record_id"]
                    == selected_record
                )

                decisions_df.loc[
                    mask,
                    "decision"
                ] = decision

                decisions_df.loc[
                    mask,
                    "reviewer"
                ] = reviewer

                decisions_df.loc[
                    mask,
                    "review_comment"
                ] = comment

                decisions_df.loc[
                    mask,
                    "decision_timestamp"
                ] = datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

                decisions_df.to_csv(
                    decisions_file,
                    index=False
                )

                st.success(
                    f"✅ Decision recorded: **{decision}**"
                )

                st.info(
                    "The original AI recommendation has been "
                    "preserved. The human decision is stored separately."
                )

                st.rerun()

        # ----------------------------------------------------
        # Review Progress
        # ----------------------------------------------------

        st.divider()

        st.subheader("📋 Review Progress")

        decisions_df = pd.read_csv(
            DATA_DIR / "review_decisions.csv",
            dtype={
                "decision": "string",
                "reviewer": "string",
                "review_comment": "string",
                "decision_timestamp": "string"
            }
        )

        completed = decisions_df[
            decisions_df["decision"].fillna("").astype(str).str.strip() != ""
        ]

        pending = len(decisions_df) - len(completed)

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Pending Reviews",
                pending
            )

        with col2:

            st.metric(
                "Completed Reviews",
                len(completed)
            )

        if len(completed) > 0:

            st.dataframe(
                completed[
                    [
                        "record_id",
                        "cpse",
                        "decision",
                        "reviewer",
                        "review_comment",
                        "decision_timestamp"
                    ]
                ],
                use_container_width=True,
                hide_index=True
            )


# ============================================================
# NATIONAL MATERIAL MASTER
# ============================================================

elif page == "National Material Master":

    st.header("🌐 National Material Master")

    category = st.selectbox(
        "Filter by Category",
        ["All"] + sorted(master_df["category"].unique().tolist())
    )

    filtered_master = master_df.copy()

    if category != "All":
        filtered_master = filtered_master[
            filtered_master["category"] == category
        ]

    st.write(
        f"National materials: **{len(filtered_master)}**"
    )

    st.dataframe(
        filtered_master,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# LEGACY MIGRATION
# ============================================================

elif page == "Legacy Migration":

    st.header("🔄 Legacy Migration")

    st.caption(
        "Controlled migration of legacy CPSE material codes into "
        "standardized National Material Codes."
    )

    # --------------------------------------------------------
    # MIGRATION SUMMARY
    # --------------------------------------------------------

    total_records = len(migration_df)

    migration_ready = (
        migration_df["migration_status"] == "MIGRATION_READY"
    ).sum()

    review_required = (
        migration_df["migration_status"] == "REVIEW_REQUIRED"
    ).sum()

    blocked = (
        migration_df["migration_status"] == "BLOCKED"
    ).sum()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Legacy Records",
            f"{total_records:,}"
        )

    with col2:
        st.metric(
            "Migration Ready",
            f"{migration_ready:,}"
        )

    with col3:
        st.metric(
            "Requires Review",
            f"{review_required + blocked:,}"
        )

    st.divider()

    # --------------------------------------------------------
    # FILTER
    # --------------------------------------------------------

    col1, col2 = st.columns([1, 2])

    with col1:

        status_filter = st.selectbox(
            "Migration Status",
            [
                "All",
                "MIGRATION_READY",
                "REVIEW_REQUIRED",
                "BLOCKED"
            ]
        )

    with col2:

        migration_search = st.text_input(
            "🔎 Search legacy code or description",
            placeholder="Example: CPSEC-769987, cable, valve..."
        )

    filtered_migration = migration_df.copy()

    # Status filter
    if status_filter != "All":
        filtered_migration = filtered_migration[
            filtered_migration["migration_status"]
            == status_filter
        ]

    # Search filter
    if migration_search:

        search_value = migration_search.lower()

        mask = (
            filtered_migration["cpse_material_code"]
            .fillna("")
            .astype(str)
            .str.lower()
            .str.contains(
                search_value,
                regex=False
            )
            |
            filtered_migration["cpse_description"]
            .fillna("")
            .astype(str)
            .str.lower()
            .str.contains(
                search_value,
                regex=False
            )
        )

        filtered_migration = filtered_migration[mask]

    st.caption(
        f"Showing {len(filtered_migration):,} migration records"
    )

    # --------------------------------------------------------
    # MIGRATION TABLE
    # --------------------------------------------------------

    migration_columns = [
        "cpse",
        "cpse_material_code",
        "cpse_description",
        "national_material_code",
        "migration_status",
        "migration_action"
    ]

    display_migration = filtered_migration[
        migration_columns
    ].copy()

    display_migration.columns = [
        "CPSE",
        "Legacy Material Code",
        "Legacy Description",
        "National Material Code",
        "Migration Status",
        "Action"
    ]

    st.dataframe(
        display_migration,
        use_container_width=True,
        hide_index=True,
        height=430,
        column_config={
            "CPSE": st.column_config.TextColumn(
                "CPSE",
                width="small"
            ),

            "Legacy Material Code": st.column_config.TextColumn(
                "Legacy Material Code",
                width="medium"
            ),

            "Legacy Description": st.column_config.TextColumn(
                "Legacy Description",
                width="large"
            ),

            "National Material Code": st.column_config.TextColumn(
                "National Material Code",
                width="medium"
            ),

            "Migration Status": st.column_config.TextColumn(
                "Migration Status",
                width="medium"
            ),

            "Action": st.column_config.TextColumn(
                "Action",
                width="medium"
            )
        }
    )

    # --------------------------------------------------------
    # SELECT RECORD FOR MIGRATION DETAIL
    # --------------------------------------------------------

    if len(filtered_migration) > 0:

        st.divider()

        selected_id = st.selectbox(
            "Select a record to inspect",
            filtered_migration["record_id"].tolist(),
            format_func=lambda x: (
                filtered_migration[
                    filtered_migration["record_id"] == x
                ]["cpse_material_code"].iloc[0]
            )
        )

        selected = filtered_migration[
            filtered_migration["record_id"] == selected_id
        ].iloc[0]

        # ----------------------------------------------------
        # MIGRATION MAPPING
        # ----------------------------------------------------

        st.subheader("📦 Migration Mapping")

        col1, col2 = st.columns([1, 1])

        with col1:

            st.markdown("**Legacy Material**")

            st.markdown(
                f"""
                **{selected['cpse_material_code']}**

                {selected['cpse_description']}

                CPSE: `{selected['cpse']}`
                """
            )

        with col2:

            st.markdown("**National Material**")

            st.markdown(
                f"""
                **{selected['national_material_code']}**

                {selected['canonical_description']}

                Category: `{selected['category']}`
                """
            )

        # ----------------------------------------------------
        # MIGRATION STATUS
        # ----------------------------------------------------

        status = selected["migration_status"]

        if status == "MIGRATION_READY":

            st.success(
                "🟢 MIGRATION READY — mapping can proceed."
            )

        elif status == "REVIEW_REQUIRED":

            st.warning(
                "🟡 REVIEW REQUIRED — human validation is required "
                "before migration."
            )

        else:

            st.error(
                "🔴 BLOCKED — migration should not proceed."
            )

        # ----------------------------------------------------
        # ACTION
        # ----------------------------------------------------

        st.caption(
            f"Recommended action: **{selected['migration_action']}**"
        )


# ============================================================
# ANALYTICS & PROCUREMENT INTELLIGENCE
# ============================================================

elif page == "Analytics":

    st.header("📊 Analytics & Procurement Intelligence")

    # ========================================================
    # HERO
    # ========================================================

    st.html(
        """
        <div class="analytics-hero">

            <div class="analytics-hero-title">
                National Material Intelligence Dashboard
            </div>

            <div class="analytics-hero-text">
                Analyze harmonization readiness, cross-CPSE material
                convergence, consolidation opportunities and migration
                status across the prototype material master.
            </div>

        </div>
        """
    )

    # ========================================================
    # DATA PREPARATION
    # ========================================================

    analytics_df = migration_df.copy()

    total_materials = len(analytics_df)

    auto_mapped = (
        analytics_df["migration_status"]
        == "MIGRATION_READY"
    ).sum()

    review_required = (
        analytics_df["migration_status"]
        == "REVIEW_REQUIRED"
    ).sum()

    blocked = (
        analytics_df["migration_status"]
        == "BLOCKED"
    ).sum()

    migration_rate = (
        auto_mapped / total_materials * 100
        if total_materials > 0
        else 0
    )

    unique_national_materials = (
        analytics_df["national_material_code"]
        .nunique()
    )

    potential_reduction = (
        total_materials - unique_national_materials
    )

    reduction_percentage = (
        potential_reduction / total_materials * 100
        if total_materials > 0
        else 0
    )

    # ========================================================
    # TOP KPI ROW
    # ========================================================

    st.html(
        """
        <div class="analytics-section">
            Harmonization Overview
        </div>

        <div class="analytics-section-sub">
            Current state of the material harmonization pipeline
        </div>
        """
    )

    k1, k2, k3, k4 = st.columns(4)

    with k1:
        st.html(
            f"""
            <div class="analytics-stat blue">
                <div class="analytics-stat-label">
                    Total Materials
                </div>

                <div class="analytics-stat-value">
                    {total_materials:,}
                </div>

                <div class="analytics-stat-help">
                    Legacy records analyzed
                </div>
            </div>
            """
        )

    with k2:
        st.html(
            f"""
            <div class="analytics-stat green">
                <div class="analytics-stat-label">
                    Migration Ready
                </div>

                <div class="analytics-stat-value">
                    {auto_mapped:,}
                </div>

                <div class="analytics-stat-help">
                    Ready for migration
                </div>
            </div>
            """
        )

    with k3:
        st.html(
            f"""
            <div class="analytics-stat amber">
                <div class="analytics-stat-label">
                    Review Required
                </div>

                <div class="analytics-stat-value">
                    {review_required:,}
                </div>

                <div class="analytics-stat-help">
                    Human validation needed
                </div>
            </div>
            """
        )

    with k4:
        st.html(
            f"""
            <div class="analytics-stat purple">
                <div class="analytics-stat-label">
                    Migration Readiness
                </div>

                <div class="analytics-stat-value">
                    {migration_rate:.1f}%
                </div>

                <div class="analytics-stat-help">
                    Records migration-ready
                </div>
            </div>
            """
        )

    # ========================================================
    # MIGRATION OVERVIEW
    # ========================================================

    st.html(
        """
        <div class="analytics-section">
            Migration Overview
        </div>

        <div class="analytics-section-sub">
            Distribution of records across migration decisions
        </div>
        """
    )

    chart_col1, chart_col2 = st.columns([1, 1.25])

    # --------------------------------------------------------
    # DONUT
    # --------------------------------------------------------

    with chart_col1:

        status_chart = pd.DataFrame({
            "Status": [
                "Migration Ready",
                "Review Required",
                "Blocked"
            ],
            "Records": [
                auto_mapped,
                review_required,
                blocked
            ]
        })

        fig = go.Figure(
            data=[
                go.Pie(
                    labels=status_chart["Status"],
                    values=status_chart["Records"],
                    hole=0.68,
                    textinfo="percent",
                    textposition="inside",
                    marker=dict(
                        colors=[
                            COLOR_GREEN,
                            COLOR_AMBER,
                            COLOR_RED
                        ],
                        line=dict(
                            color="#0B1220",
                            width=3
                        )
                    )
                )
            ]
        )

        fig.add_annotation(
            text=(
                f"<b>{total_materials}</b>"
                "<br><span style='font-size:11px'>Records</span>"
            ),
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(
                size=23,
                color=TEXT_MAIN
            )
        )

        fig.update_layout(
            height=330,
            margin=dict(
                l=10,
                r=10,
                t=15,
                b=10
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(
                color=TEXT_MUTED
            ),
            legend=dict(
                orientation="h",
                y=-0.05,
                x=0.5,
                xanchor="center",
                bgcolor="rgba(0,0,0,0)"
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False}
        )

    # --------------------------------------------------------
    # STATUS BAR
    # --------------------------------------------------------

    with chart_col2:

        fig = px.bar(
            status_chart,
            x="Records",
            y="Status",
            orientation="h",
            text="Records",
            color="Status",
            color_discrete_map={
                "Migration Ready": COLOR_GREEN,
                "Review Required": COLOR_AMBER,
                "Blocked": COLOR_RED
            }
        )

        fig.update_traces(
            textposition="outside",
            textfont=dict(
                color=TEXT_MAIN,
                size=13
            ),
            marker_line_width=0
        )

        fig = style_chart(fig, 330)

        fig.update_layout(
            showlegend=False,
            xaxis_title=None,
            yaxis_title=None,
            xaxis=dict(
                showgrid=True,
                gridcolor=CHART_GRID
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False}
        )

    st.html(
        f"""
        <div class="analytics-insight">
            <strong>{migration_rate:.1f}%</strong> of prototype records
            are currently classified as migration-ready.
            <strong>{review_required}</strong> require review and
            <strong>{blocked}</strong> are blocked from migration.
        </div>
        """
    )

    # ========================================================
    # CPSE-WISE ANALYSIS
    # ========================================================

    st.html(
        """
        <div class="analytics-section">
            🏢 CPSE-wise Harmonization
        </div>

        <div class="analytics-section-sub">
            Compare material readiness across participating enterprises
        </div>
        """
    )

    cpse_summary = (
        analytics_df
        .groupby("cpse")
        .agg(
            Total_Materials=("record_id", "count"),

            Migration_Ready=(
                "migration_status",
                lambda x: (
                    x == "MIGRATION_READY"
                ).sum()
            ),

            Review_Required=(
                "migration_status",
                lambda x: (
                    x == "REVIEW_REQUIRED"
                ).sum()
            ),

            Blocked=(
                "migration_status",
                lambda x: (
                    x == "BLOCKED"
                ).sum()
            )
        )
        .reset_index()
    )

    cpse_summary["Readiness_%"] = (
        cpse_summary["Migration_Ready"]
        / cpse_summary["Total_Materials"]
        * 100
    ).round(1)

    cpse_col1, cpse_col2 = st.columns([1.05, 1])

    with cpse_col1:

        st.dataframe(
            cpse_summary,
            use_container_width=True,
            hide_index=True,
            column_config={
                "cpse": st.column_config.TextColumn(
                    "CPSE"
                ),
                "Total_Materials": st.column_config.NumberColumn(
                    "Total"
                ),
                "Migration_Ready": st.column_config.NumberColumn(
                    "Ready"
                ),
                "Review_Required": st.column_config.NumberColumn(
                    "Review"
                ),
                "Blocked": st.column_config.NumberColumn(
                    "Blocked"
                ),
                "Readiness_%": st.column_config.ProgressColumn(
                    "Readiness",
                    min_value=0,
                    max_value=100,
                    format="%.1f%%"
                )
            }
        )

    with cpse_col2:

        cpse_chart = cpse_summary.sort_values(
            "Readiness_%"
        )

        fig = px.bar(
            cpse_chart,
            x="Readiness_%",
            y="cpse",
            orientation="h",
            text="Readiness_%",
            labels={
                "Readiness_%": "Migration Readiness",
                "cpse": ""
            }
        )

        fig.update_traces(
            marker_color=COLOR_BLUE,
            marker_line_width=0,
            texttemplate="%{text:.1f}%",
            textposition="outside",
            textfont=dict(
                color=TEXT_MAIN,
                size=12
            )
        )

        fig = style_chart(fig, 300)

        fig.update_layout(
            xaxis=dict(
                range=[0, 105],
                ticksuffix="%"
            ),
            showlegend=False
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False}
        )

    # ========================================================
    # CATEGORY ANALYSIS
    # ========================================================

    st.html(
        """
        <div class="analytics-section">
            🧩 Material Category Intelligence
        </div>

        <div class="analytics-section-sub">
            Identify categories with high consolidation and migration potential
        </div>
        """
    )

    category_summary = (
        analytics_df
        .groupby("category")
        .agg(
            Total_Materials=("record_id", "count"),

            Migration_Ready=(
                "migration_status",
                lambda x: (
                    x == "MIGRATION_READY"
                ).sum()
            ),

            Review_Required=(
                "migration_status",
                lambda x: (
                    x == "REVIEW_REQUIRED"
                ).sum()
            ),

            Blocked=(
                "migration_status",
                lambda x: (
                    x == "BLOCKED"
                ).sum()
            )
        )
        .reset_index()
    )

    category_summary["Readiness_%"] = (
        category_summary["Migration_Ready"]
        / category_summary["Total_Materials"]
        * 100
    ).round(1)

    cat_col1, cat_col2 = st.columns([1, 1.2])

    with cat_col1:

        st.dataframe(
            category_summary,
            use_container_width=True,
            hide_index=True,
            column_config={
                "category": st.column_config.TextColumn(
                    "Category"
                ),
                "Total_Materials": st.column_config.NumberColumn(
                    "Total"
                ),
                "Migration_Ready": st.column_config.NumberColumn(
                    "Ready"
                ),
                "Review_Required": st.column_config.NumberColumn(
                    "Review"
                ),
                "Blocked": st.column_config.NumberColumn(
                    "Blocked"
                ),
                "Readiness_%": st.column_config.ProgressColumn(
                    "Readiness",
                    min_value=0,
                    max_value=100,
                    format="%.1f%%"
                )
            }
        )

    with cat_col2:

        category_chart = category_summary.sort_values(
            "Total_Materials",
            ascending=True
        )

        fig = px.bar(
            category_chart,
            x="Total_Materials",
            y="category",
            orientation="h",
            text="Total_Materials"
        )

        fig.update_traces(
            marker_color=COLOR_CYAN,
            marker_line_width=0,
            textposition="outside",
            textfont=dict(
                color=TEXT_MAIN,
                size=11
            )
        )

        fig = style_chart(fig, 360)

        fig.update_layout(
            xaxis_title="Legacy Records",
            yaxis_title=None,
            showlegend=False
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False}
        )

    # ========================================================
    # CROSS CPSE COMMON MATERIALS
    # ========================================================

    st.html(
        """
        <div class="analytics-section">
            🌐 Cross-CPSE Common Materials
        </div>

        <div class="analytics-section-sub">
            National materials already shared across multiple CPSEs
        </div>
        """
    )

    national_usage = (
        analytics_df
        .groupby("national_material_code")
        .agg(
            CPSE_Count=("cpse", "nunique"),
            Legacy_Record_Count=("record_id", "count"),
            Category=("category", "first"),
            National_Description=(
                "canonical_description",
                "first"
            )
        )
        .reset_index()
    )

    common_materials = national_usage[
        national_usage["CPSE_Count"] > 1
    ].copy()

    common_materials = common_materials.sort_values(
        ["CPSE_Count", "Legacy_Record_Count"],
        ascending=False
    )

    if len(common_materials) > 0:

        st.html(
            f"""
            <div class="analytics-insight">
                <strong>{len(common_materials)}</strong> national
                materials are shared across multiple CPSEs,
                demonstrating cross-enterprise material convergence.
            </div>
            """
        )

        common_chart = common_materials.head(10).copy()

        fig = px.bar(
            common_chart.sort_values(
                "Legacy_Record_Count"
            ),
            x="Legacy_Record_Count",
            y="national_material_code",
            orientation="h",
            text="Legacy_Record_Count"
        )

        fig.update_traces(
            marker_color=COLOR_PURPLE,
            marker_line_width=0,
            textposition="outside",
            textfont=dict(
                color=TEXT_MAIN,
                size=11
            )
        )

        fig = style_chart(fig, 350)

        fig.update_layout(
            xaxis_title="Legacy Records Consolidated",
            yaxis_title="National Material Code",
            showlegend=False
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False}
        )

        st.dataframe(
            common_materials[
                [
                    "national_material_code",
                    "National_Description",
                    "Category",
                    "CPSE_Count",
                    "Legacy_Record_Count"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No cross-CPSE common materials identified."
        )

    # ========================================================
    # CONSOLIDATION OPPORTUNITY
    # ========================================================

    st.html(
        """
        <div class="analytics-section">
            📉 Consolidation Opportunity
        </div>

        <div class="analytics-section-sub">
            Potential reduction in duplicate legacy material representations
        </div>
        """
    )

    c1, c2, c3 = st.columns(3)

    with c1:

        st.html(
            f"""
            <div class="analytics-stat blue">

                <div class="analytics-stat-label">
                    Legacy Records
                </div>

                <div class="analytics-stat-value">
                    {total_materials:,}
                </div>

                <div class="analytics-stat-help">
                    Before harmonization
                </div>

            </div>
            """
        )

    with c2:

        st.html(
            f"""
            <div class="analytics-stat green">

                <div class="analytics-stat-label">
                    National Codes
                </div>

                <div class="analytics-stat-value">
                    {unique_national_materials:,}
                </div>

                <div class="analytics-stat-help">
                    Standardized representations
                </div>

            </div>
            """
        )

    with c3:

        st.html(
            f"""
            <div class="analytics-stat purple">

                <div class="analytics-stat-label">
                    Potential Consolidation
                </div>

                <div class="analytics-stat-value">
                    {potential_reduction:,}
                </div>

                <div class="analytics-stat-help">
                    Fewer material representations
                </div>

            </div>
            """
        )

    st.html(
        f"""
        <div class="analytics-insight">
            The prototype dataset indicates a potential
            <strong>{reduction_percentage:.1f}% reduction</strong>
            in material-record duplication after harmonization.
        </div>

        <div class="analytics-warning">
            ⚠ <strong>Prototype limitation:</strong>
            These results use synthetic benchmark data.
            They demonstrate the analytical workflow and should
            not be interpreted as actual CPSE procurement savings.
        </div>
        """
    )

    # ========================================================
    # PROCUREMENT INTELLIGENCE
    # ========================================================

    st.html(
        """
        <div class="analytics-section">
            💡 Procurement Intelligence
        </div>

        <div class="analytics-section-sub">
            Business opportunities enabled by a common national material vocabulary
        </div>
        """
    )

    p1, p2, p3 = st.columns(3)

    with p1:

        st.html(
            """
            <div class="procurement-card">

                <div class="procurement-icon">
                    🔗
                </div>

                <div class="procurement-title">
                    Demand Aggregation
                </div>

                <div class="procurement-text">
                    Identify the same standardized material
                    across multiple CPSEs to support consolidated
                    demand visibility.
                </div>

            </div>
            """
        )

    with p2:

        st.html(
            """
            <div class="procurement-card">

                <div class="procurement-icon">
                    ♻️
                </div>

                <div class="procurement-title">
                    Duplicate Reduction
                </div>

                <div class="procurement-text">
                    Multiple legacy representations can be mapped
                    to one standardized national material identity.
                </div>

            </div>
            """
        )

    with p3:

        st.html(
            """
            <div class="procurement-card">

                <div class="procurement-icon">
                    📐
                </div>

                <div class="procurement-title">
                    Specification Consistency
                </div>

                <div class="procurement-text">
                    Standardized descriptions and technical attributes
                    improve consistency across enterprise material masters.
                </div>

            </div>
            """
        )

    p4, p5, p6 = st.columns(3)

    with p4:

        st.html(
            """
            <div class="procurement-card">

                <div class="procurement-icon">
                    🌐
                </div>

                <div class="procurement-title">
                    Cross-CPSE Visibility
                </div>

                <div class="procurement-text">
                    A common material code makes equivalent materials
                    easier to discover across enterprise boundaries.
                </div>

            </div>
            """
        )

    with p5:

        st.html(
            """
            <div class="procurement-card">

                <div class="procurement-icon">
                    🛡️
                </div>

                <div class="procurement-title">
                    Migration Control
                </div>

                <div class="procurement-text">
                    Uncertain mappings are routed for human validation
                    instead of being migrated automatically.
                </div>

            </div>
            """
        )

    with p6:

        st.html(
            """
            <div class="procurement-card">

                <div class="procurement-icon">
                    📈
                </div>

                <div class="procurement-title">
                    Master Data Governance
                </div>

                <div class="procurement-text">
                    Centralized national material identities create a
                    stronger foundation for future procurement analytics.
                </div>

            </div>
            """
        )

    # ========================================================
    # FINAL NOTE
    # ========================================================

    st.html(
        """
        <div class="analytics-warning">

            <strong>Data boundary:</strong>
            This prototype demonstrates the harmonization and
            analytical workflow using synthetic material records.
            Actual procurement value, consumption trends and
            enterprise-wide savings require historical CPSE
            procurement and consumption data.

        </div>
        """
    )

# ============================================================
# AUDIT TRAIL
# ============================================================

elif page == "Audit Trail":

    st.header("📜 Audit Trail")

    st.caption(
        "Traceable record of system recommendations, review actions "
        "and migration decisions."
    )

    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    total_events = len(audit_df)

    unique_actions = audit_df["action"].nunique()

    unique_records = (
        audit_df["record_id"].nunique()
        if "record_id" in audit_df.columns
        else 0
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Audit Events",
            f"{total_events:,}"
        )

    with col2:
        st.metric(
            "Tracked Records",
            f"{unique_records:,}"
        )

    with col3:
        st.metric(
            "Action Types",
            f"{unique_actions:,}"
        )

    st.divider()

    # --------------------------------------------------------
    # FILTERS
    # --------------------------------------------------------

    col1, col2 = st.columns([1, 2])

    with col1:

        action_filter = st.selectbox(
            "Filter Action",
            ["All"] + sorted(
                audit_df["action"]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )
        )

    with col2:

        audit_search = st.text_input(
            "🔎 Search audit trail",
            placeholder="Search material code, record ID, action..."
        )

    filtered_audit = audit_df.copy()

    # Action filter
    if action_filter != "All":

        filtered_audit = filtered_audit[
            filtered_audit["action"] == action_filter
        ]

    # Search
    if audit_search:

        search_value = audit_search.lower()

        search_mask = pd.Series(
            False,
            index=filtered_audit.index
        )

        for column in filtered_audit.columns:

            search_mask = (
                search_mask
                |
                filtered_audit[column]
                .fillna("")
                .astype(str)
                .str.lower()
                .str.contains(
                    search_value,
                    regex=False
                )
            )

        filtered_audit = filtered_audit[search_mask]

    st.caption(
        f"Showing {len(filtered_audit):,} audit events"
    )

    # --------------------------------------------------------
    # AUDIT TABLE
    # --------------------------------------------------------

    st.dataframe(
        filtered_audit,
        use_container_width=True,
        hide_index=True,
        height=430
    )

    # --------------------------------------------------------
    # EVENT DETAILS
    # --------------------------------------------------------

    if len(filtered_audit) > 0:

        st.divider()

        st.subheader("🔍 Event Details")

        selected_index = st.selectbox(
            "Select an audit event",
            filtered_audit.index.tolist(),
            format_func=lambda x: (
                f"Event {x + 1} — "
                f"{filtered_audit.loc[x, 'action']}"
            )
        )

        selected_event = filtered_audit.loc[
            selected_index
        ]

        col1, col2 = st.columns(2)

        with col1:

            st.markdown("**Event Information**")

            for column in filtered_audit.columns:

                if column in [
                    "action",
                    "timestamp",
                    "record_id"
                ]:

                    value = selected_event[column]

                    st.write(
                        f"**{column.replace('_', ' ').title()}:** "
                        f"{value}"
                    )

        with col2:

            st.markdown("**Complete Event Record**")

            st.json(
                selected_event.to_dict()
            )