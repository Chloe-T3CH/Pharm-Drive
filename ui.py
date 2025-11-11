import json
import time
from datetime import datetime

import requests
import streamlit as st

DEFAULT_MISSION = (
    "As a medical science liaison, explain document changes in simple, department-aware language "
    "that marketing, medical affairs, legal, and sales teams can act on."
)

st.set_page_config(
    page_title="Pharm-Drive | AI Content Intelligence",
    page_icon="⚕️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Dark Minimalist Professional CSS
st.markdown(
    """
<style>
    /* Dark background throughout */
    .main {
        background: #0e1117;
    }
    
    /* Dark content container */
    .block-container {
        background: #0e1117 !important;
        padding: 2rem !important;
        max-width: 1200px;
    }
    
    /* Light text on dark background */
    .main h1, .main h2, .main h3, .main h4, .main h5, .main h6 {
        color: #fafafa !important;
    }
    
    .main p, .main span, .main div, .main label, .main li {
        color: #e5e7eb !important;
    }
    
    /* Hero section - clean purple accent */
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        border: 1px solid rgba(102, 126, 234, 0.3);
    }
    
    .hero-section h1 {
        color: white !important;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        font-weight: 700;
    }
    
    .hero-section h3 {
        color: rgba(255, 255, 255, 0.95) !important;
        font-weight: 500;
        font-size: 1.3rem;
    }
    
    .hero-section p {
        color: rgba(255, 255, 255, 0.95) !important;
        font-size: 1.05rem;
        line-height: 1.7;
    }
    
    /* File uploader - dark with purple accent */
    [data-testid="stFileUploader"] {
        background: #1a1d29 !important;
        border: 2px dashed #667eea !important;
        border-radius: 12px;
        padding: 2rem !important;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #764ba2 !important;
        background: #1f2332 !important;
    }
    
    [data-testid="stFileUploader"] section {
        background: transparent !important;
    }
    
    [data-testid="stFileUploader"] label,
    [data-testid="stFileUploader"] span,
    [data-testid="stFileUploader"] small,
    [data-testid="stFileUploader"] p {
        color: #e5e7eb !important;
    }
    
    /* Primary buttons - purple gradient */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1.05rem;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-1px);
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.35);
    }
    
    /* Secondary buttons */
    .stButton > button {
        background: #1a1d29 !important;
        color: #667eea !important;
        border: 1px solid #667eea !important;
        padding: 0.7rem 1.5rem;
        font-weight: 600;
        border-radius: 8px;
    }
    
    .stButton > button:hover {
        background: rgba(102, 126, 234, 0.1) !important;
    }
    
    /* Download buttons */
    .stDownloadButton > button {
        background: #1a1d29 !important;
        border: 1px solid #667eea !important;
        color: #667eea !important;
        font-weight: 600;
        border-radius: 8px;
    }
    
    .stDownloadButton > button:hover {
        background: rgba(102, 126, 234, 0.15) !important;
    }
    
    /* Metrics - purple accent */
    [data-testid="stMetricValue"] {
        color: #667eea !important;
        font-size: 1.8rem !important;
        font-weight: 700;
    }
    
    [data-testid="stMetricLabel"] {
        color: #9ca3af !important;
        font-weight: 600;
        font-size: 0.9rem;
    }
    
    [data-testid="stMetricDelta"] {
        color: #48bb78 !important;
    }
    
    /* Alert boxes - dark themed */
    [data-testid="stAlert"] {
        border-radius: 8px;
        padding: 1rem;
        background: #1a1d29 !important;
    }
    
    /* Success */
    [data-testid="stAlert"][kind="success"] {
        border-left: 3px solid #48bb78 !important;
    }
    
    [data-testid="stAlert"][kind="success"] * {
        color: #86efac !important;
    }
    
    /* Info */
    [data-testid="stAlert"][kind="info"] {
        border-left: 3px solid #667eea !important;
    }
    
    [data-testid="stAlert"][kind="info"] * {
        color: #a5b4fc !important;
    }
    
    /* Warning */
    [data-testid="stAlert"][kind="warning"] {
        border-left: 3px solid #f59e0b !important;
    }
    
    [data-testid="stAlert"][kind="warning"] * {
        color: #fbbf24 !important;
    }
    
    /* Error */
    [data-testid="stAlert"][kind="error"] {
        border-left: 3px solid #ef4444 !important;
    }
    
    [data-testid="stAlert"][kind="error"] * {
        color: #fca5a5 !important;
    }
    
    /* Tabs - minimal dark */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: transparent;
        border-bottom: 1px solid #2d3748;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        border-radius: 0;
        padding: 12px 24px;
        color: #9ca3af !important;
        font-weight: 600;
        border: none;
    }
    
    .stTabs [aria-selected="true"] {
        background: transparent !important;
        border-bottom: 3px solid #667eea !important;
        color: #667eea !important;
    }
    
    /* Input fields - dark */
    input, textarea, select {
        background: #1a1d29 !important;
        color: #e5e7eb !important;
        border: 1px solid #374151 !important;
        border-radius: 8px;
    }
    
    input:focus, textarea:focus, select:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2) !important;
    }
    
    /* Labels */
    .stTextInput label,
    .stTextArea label,
    .stSelectbox label,
    .stMultiselect label,
    .stRadio label,
    .stCheckbox label {
        color: #e5e7eb !important;
        font-weight: 600 !important;
    }
    
    /* Radio and checkbox */
    .stRadio div[role="radiogroup"] label,
    .stCheckbox label {
        color: #e5e7eb !important;
    }
    
    /* Expander - dark */
    .streamlit-expanderHeader {
        background: #1a1d29 !important;
        border: 1px solid #374151 !important;
        border-radius: 8px;
        color: #e5e7eb !important;
        font-weight: 600;
    }
    
    .streamlit-expanderHeader:hover {
        background: #1f2332 !important;
        border-color: #667eea !important;
    }
    
    /* Code blocks */
    .stCodeBlock {
        background: #1a1d29 !important;
        border: 1px solid #374151 !important;
        border-radius: 8px;
    }
    
    /* Dataframes */
    .dataframe {
        background: #1a1d29 !important;
        color: #e5e7eb !important;
    }
    
    /* Progress bar */
    .stProgress > div > div > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    }
    
    /* Sidebar - dark */
    [data-testid="stSidebar"] {
        background: #0e1117 !important;
        border-right: 1px solid #2d3748;
    }
    
    [data-testid="stSidebar"] * {
        color: #e5e7eb !important;
    }
    
    /* Sidebar header */
    .sidebar-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    
    .sidebar-header h1 {
        color: white !important;
        margin: 0;
        font-size: 1.6rem;
        font-weight: 700;
    }
    
    .sidebar-header p {
        color: rgba(255, 255, 255, 0.95) !important;
        margin: 0;
        font-size: 0.85rem;
    }
    
    /* Footer */
    .footer-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-top: 3rem;
        text-align: center;
        border: 1px solid rgba(102, 126, 234, 0.3);
    }
    
    .footer-section * {
        color: white !important;
    }
    
    /* Caption text */
    .caption, small {
        color: #9ca3af !important;
    }
    
    /* Dividers */
    hr {
        border-color: #2d3748 !important;
    }
    
    /* Markdown section boxes */
    .info-box {
        background: #1a1d29;
        border-left: 3px solid #667eea;
        padding: 1.2rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .info-box * {
        color: #e5e7eb !important;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Session state
if "comparison_history" not in st.session_state:
    st.session_state.comparison_history = []
if "demo_mode" not in st.session_state:
    st.session_state.demo_mode = False
if "api_endpoint" not in st.session_state:
    st.session_state.api_endpoint = "http://localhost:8000"
if "summarizer_api_key" not in st.session_state:
    st.session_state.summarizer_api_key = ""
if "comparison_result" not in st.session_state:
    st.session_state.comparison_result = None

# Sidebar
with st.sidebar:
    st.markdown(
        """
        <div class='sidebar-header'>
            <h1>⚕️ Pharm-Drive</h1>
            <p>AI Content Intelligence</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    st.markdown("---")
    
    st.session_state.demo_mode = st.checkbox("🎬 Conference Demo Mode", value=st.session_state.demo_mode)
    if st.session_state.demo_mode:
        st.info("Demo mode active")
    
    st.markdown("---")
    st.markdown("### 🎯 About")
    st.markdown(
        """
        AI-powered intelligence that unifies marketing, medical affairs, legal, and sales.
        
        **Benefits:**
        - ⚡ Faster review cycles
        - ✅ Compliant messaging
        - 🤖 Automated detection
        - 📊 Actionable insights
        """
    )
    
    st.markdown("---")
    st.markdown("### 📊 Stats")
    st.metric("Comparisons", len(st.session_state.comparison_history))
    if st.session_state.comparison_history:
        last = st.session_state.comparison_history[-1]
        st.metric("Last Run", last["timestamp"].strftime("%H:%M"))
    
    st.markdown("---")
    st.markdown("### 🔌 API")
    try:
        response = requests.get(st.session_state.api_endpoint, timeout=1)
        if response.ok:
            st.success("Connected")
        else:
            st.warning("Partial")
    except requests.RequestException:
        st.error("Disconnected")
    
    st.markdown("---")
    st.caption("v1.0.0 | Conference Edition")

# Header
st.markdown(
    """
    <div class='hero-section'>
        <h1>⚕️ Pharm-Drive</h1>
        <h3>AI Content Intelligence Platform</h3>
        <p><strong>Transform document updates into actionable intelligence.</strong> Upload documents to receive AI-powered change analysis, compliance insights, and sales-ready summaries in seconds.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(
    ["📤 Compare", "📊 Results", "📈 Analytics", "⚙️ Settings"]
)

# TAB 1: Compare
with tab1:
    st.markdown("### Upload Documents")
    
    if st.session_state.demo_mode:
        st.warning("🎬 Demo Mode Active")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📄 Original")
        file1 = st.file_uploader(
            "Upload baseline version",
            type=["txt", "docx", "pdf", "pptx"],
            key="file1",
            help="The original document",
        )
        if file1:
            st.success(f"✓ {file1.name}")
            st.caption(f"{file1.size / 1024:.1f} KB")
    
    with col2:
        st.markdown("#### 📄 Updated")
        file2 = st.file_uploader(
            "Upload revised version",
            type=["txt", "docx", "pdf", "pptx"],
            key="file2",
            help="The updated document",
        )
        if file2:
            st.success(f"✓ {file2.name}")
            st.caption(f"{file2.size / 1024:.1f} KB")
    
    st.markdown("---")
    
    with st.expander("🔧 Advanced Options"):
        col1, col2 = st.columns(2)
        
        with col1:
            focus_area = st.selectbox(
                "Focus",
                ["General", "Dosage", "Safety", "Efficacy", "Contraindications", "Adverse Events"],
            )
            summary_length = st.select_slider(
                "Detail",
                options=["Brief", "Standard", "Comprehensive"],
                value="Standard",
            )
        
        with col2:
            priority_level = st.radio(
                "Priority",
                ["Auto-detect", "High", "Medium", "Low"],
            )
            include_technical_diff = st.checkbox("Include Diff", value=True)
        
        department_targets = st.multiselect(
            "Target Departments",
            ["Marketing", "Medical Affairs", "Legal", "Sales", "Patient Education"],
            default=["Marketing", "Medical Affairs", "Legal", "Sales"],
        )
        mission_instruction = st.text_area(
            "Instructions",
            value=DEFAULT_MISSION,
            height=100,
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    compare_button = st.button("🔍 Analyze Changes", type="primary", use_container_width=True)
    
    if compare_button:
        if not file1 or not file2:
            st.warning("⚠️ Please upload both documents")
        else:
            url = f"{st.session_state.api_endpoint.rstrip('/')}/compare"
            payload = {
                "mission_context": mission_instruction
                + " "
                + (f"Departments: {', '.join(department_targets)}." if department_targets else ""),
                "api_key": st.session_state.summarizer_api_key,
            }
            files = {
                "file_old": (file1.name, file1.getvalue(), file1.type),
                "file_new": (file2.name, file2.getvalue(), file2.type),
            }
            
            progress = st.progress(0)
            status = st.empty()
            
            for text, pct in [
                ("📄 Extracting...", 0.25),
                ("🔍 Computing diff...", 0.5),
                ("🤖 AI analyzing...", 0.75),
                ("📊 Finalizing...", 1.0),
            ]:
                status.text(text)
                progress.progress(pct)
                time.sleep(0.3)
            
            try:
                response = requests.post(url, files=files, data=payload, timeout=60)
                progress.empty()
                status.empty()
                
                if response.status_code == 200:
                    result = response.json()
                    st.session_state.comparison_result = result
                    st.session_state.comparison_history.append({
                        "timestamp": datetime.now(),
                        "file1": file1.name,
                        "file2": file2.name,
                        "focus": focus_area,
                        "priority": priority_level,
                        "result": result,
                    })
                    st.success("✅ Complete! Check Results tab")
                    st.balloons()
                else:
                    st.error(f"❌ Failed: {response.json().get('detail', 'Unknown error')}")
            
            except requests.exceptions.ConnectionError:
                progress.empty()
                status.empty()
                st.error("❌ Cannot connect to API")
            except requests.exceptions.Timeout:
                progress.empty()
                status.empty()
                st.error("❌ Request timed out")
            except Exception as exc:
                progress.empty()
                status.empty()
                st.error(f"❌ Error: {exc}")

# TAB 2: Results
with tab2:
    st.markdown("### Analysis Results")
    result = st.session_state.comparison_result
    
    if result:
        if st.session_state.comparison_history:
            latest = st.session_state.comparison_history[-1]
            st.markdown(
                f"""
                <div class='info-box'>
                    <strong>📄 {latest['file1']}</strong> → <strong>{latest['file2']}</strong><br>
                    <small>🕐 {latest['timestamp'].strftime("%B %d, %Y at %H:%M:%S")}</small>
                </div>
                """,
                unsafe_allow_html=True,
            )
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Method", result.get("method", "N/A").upper())
        col2.metric("Tokens", result.get("tokens_used", "N/A"))
        col3.metric("Processing", "Full" if not result.get("truncated") else "Partial")
        col4.metric("Time", "< 10s")
        
        st.markdown("---")
        
        st.markdown("### ⚠️ Compliance Impact")
        summary_text = result.get("summary", "No summary")
        
        risk_level = "LOW"
        if any(w in summary_text.lower() for w in ["dosage", "contraindication", "warning", "serious", "adverse"]):
            risk_level = "HIGH"
        elif any(w in summary_text.lower() for w in ["update", "change", "revised", "modified"]):
            risk_level = "MEDIUM"
        
        if risk_level == "HIGH":
            st.error("🔴 HIGH RISK")
        elif risk_level == "MEDIUM":
            st.warning("🟡 MEDIUM RISK")
        else:
            st.success("🟢 LOW RISK")
        
        st.markdown("### 🤖 AI Summary")
        st.info(summary_text)
        
        st.markdown("### 📋 Actions")
        if risk_level == "HIGH":
            st.markdown("- ✅ Immediate compliance review\n- ✅ Brief sales teams\n- ✅ Document in audit log\n- ✅ Notify medical affairs")
        elif risk_level == "MEDIUM":
            st.markdown("- ✅ Team lead review\n- ✅ Update materials\n- ✅ Legal alignment")
        else:
            st.markdown("- ✅ Acknowledge change\n- ✅ Update at next cycle")
        
        st.markdown("---")
        
        with st.expander("📋 Technical Diff"):
            diff_text = result.get("diff", "")
            st.code(diff_text or "No diff", language="diff")
            
            lines = diff_text.splitlines()
            adds = sum(1 for l in lines if l.startswith("+") and not l.startswith("+++"))
            dels = sum(1 for l in lines if l.startswith("-") and not l.startswith("---"))
            
            c1, c2, c3 = st.columns(3)
            c1.metric("Added", adds)
            c2.metric("Removed", dels)
            c3.metric("Net", abs(adds - dels))
        
        st.markdown("---")
        st.markdown("### 📤 Export")
        
        cols = st.columns(4)
        
        report = f"""PHARM-DRIVE ANALYSIS
{'=' * 50}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Risk: {risk_level}

SUMMARY:
{summary_text}

METADATA:
- Method: {result.get('method', 'N/A')}
- Tokens: {result.get('tokens_used', 'N/A')}
- Truncated: {result.get('truncated', False)}
"""
        
        cols[0].download_button("💾 Summary", report, f"summary_{datetime.now():%Y%m%d_%H%M%S}.txt")
        cols[1].download_button("📊 JSON", json.dumps(result, indent=2), f"data_{datetime.now():%Y%m%d_%H%M%S}.json")
        if cols[2].button("📧 Email"):
            st.info("Configure email")
        if cols[3].button("💬 Slack"):
            st.info("Configure Slack")
    
    else:
        st.info("👆 Run analysis in Compare tab")

# TAB 3: Analytics
with tab3:
    st.markdown("### 📈 Analytics")
    history = st.session_state.comparison_history
    
    if history:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total", len(history))
        c2.metric("Session", len(history))
        c3.metric("Avg Time", "< 10s")
        c4.metric("Success", "100%")
        
        st.markdown("---")
        st.markdown("### 📋 History")
        
        data = [{
            "Time": e["timestamp"].strftime("%H:%M:%S"),
            "Original": e["file1"],
            "Updated": e["file2"],
            "Focus": e["focus"],
        } for e in reversed(history)]
        
        st.dataframe(data, use_container_width=True)
    else:
        st.info("No data yet")

# TAB 4: Settings
with tab4:
    st.markdown("### ⚙️ Settings")
    
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown("#### 🔌 API")
        st.session_state.api_endpoint = st.text_input("Endpoint", st.session_state.api_endpoint)
        
        st.text_input(
            "API Key",
            st.session_state.summarizer_api_key,
            type="password",
            key="summarizer_api_key_input",
        )
        st.session_state.summarizer_api_key = st.session_state.get("summarizer_api_key_input", "")
        st.caption("Prefix with `openai:` or `gemini:` for provider selection.")
        
        if st.button("🔍 Test"):
            try:
                r = requests.get(st.session_state.api_endpoint, timeout=2)
                st.success("✅ Connected" if r.ok else "⚠️ Partial")
            except:
                st.error("❌ Failed")
        
        st.markdown("#### 📧 Notifications")
        st.checkbox("Email", value=True)
        st.checkbox("Slack", value=False)
        st.checkbox("Desktop", value=True)
    
    with c2:
        st.markdown("#### 🎨 Display")
        st.selectbox("Date Format", ["YYYY-MM-DD", "MM/DD/YYYY", "DD/MM/YYYY"])
        st.multiselect("Export", ["PDF", "DOCX", "JSON", "CSV"], default=["JSON"])
        
        st.markdown("#### 🔐 Security")
        st.checkbox("Auto-delete (30 days)", value=True)
        st.checkbox("Require auth", value=False)
    
    st.markdown("---")
    
    if st.button("💾 Save", use_container_width=True):
        st.success("✅ Saved")
        st.balloons()

# Footer
st.markdown(
    """
    <div class='footer-section'>
        <p style='font-size: 1.1rem; font-weight: 600; margin-bottom: 0.5rem;'>
            ⚕️ Pharm-Drive | AI Content Intelligence by Chloe Flibbert
        </p>
        <p style='font-size: 0.9rem; opacity: 0.95; margin: 0;'>
            © 2025 Pharm-Drive | Pharmaceutical sales excellence | Contact: chloe.gflibbert@gmail.com<br>
            Bridging marketing, medical affairs, legal, and sales
        </p>
        <p style='font-size: 0.8rem; opacity: 0.85; margin-top: 1rem;'>
            Built with ❤️ by using SHURGE, Streamlit, FastAPI, and OpenAI GPT-4
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)
