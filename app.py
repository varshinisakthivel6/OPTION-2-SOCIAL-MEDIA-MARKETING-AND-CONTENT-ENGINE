
import streamlit as st
import sys
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from engine.content_engine import generate, export_csv

st.set_page_config(
    page_title="IncuBrix | Social Content Studio",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -------------------- CUSTOM DESIGN --------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background:
        radial-gradient(ellipse at 5% 0%, rgba(105, 74, 220, 0.16), transparent 35%),
        radial-gradient(ellipse at 95% 10%, rgba(50, 120, 230, 0.12), transparent 32%),
        #090D1B;
    color: #F4F5FF;
}

.block-container {
    max-width: 1180px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

header[data-testid="stHeader"] {
    background: transparent;
}

#MainMenu, footer {
    visibility: hidden;
}

.hero {
    padding: 42px 38px;
    border: 1px solid rgba(167, 139, 250, 0.25);
    border-radius: 24px;
    background: linear-gradient(120deg, #191637 0%, #171B3A 55%, #102443 100%);
    box-shadow: 0 18px 55px rgba(0,0,0,0.25);
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
}

.hero-tag {
    display: inline-block;
    padding: 7px 13px;
    border: 1px solid rgba(196,181,253,0.35);
    border-radius: 30px;
    color: #D5C8FF;
    background: rgba(139,92,246,0.13);
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1.2px;
}

.hero h1 {
    font-family: 'Space Grotesk', sans-serif;
    font-size: clamp(32px, 5vw, 48px);
    line-height: 1.12;
    font-weight: 700;
    color: #FFFFFF;
    margin: 22px 0 12px 0;
}

.hero h1 span {
    background: linear-gradient(90deg, #C4B5FD, #7DD3FC);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero p {
    color: #C4C7DF;
    font-size: 16px;
    line-height: 1.7;
    max-width: 680px;
    margin-bottom: 0;
}

.section-heading {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 23px;
    font-weight: 700;
    color: #F5F3FF;
    margin-top: 30px;
    margin-bottom: 5px;
}

.section-sub {
    color: #929AB5;
    font-size: 13px;
    margin-bottom: 20px;
}

.panel {
    background: rgba(21, 27, 49, 0.88);
    border: 1px solid rgba(148,163,184,0.16);
    border-radius: 18px;
    padding: 24px;
    margin-bottom: 18px;
}

.stTextArea textarea {
    background: #10172B !important;
    color: #F4F5FF !important;
    border: 1px solid #303B5B !important;
    border-radius: 12px !important;
}

[data-testid="stFileUploader"] {
    background: #10172B;
    border: 1px dashed #7164C9;
    border-radius: 14px;
    padding: 15px;
}

[data-testid="stFileUploader"] section {
    background: transparent;
}

.stSlider [data-baseweb="slider"] {
    margin-top: 12px;
}

.stButton > button {
    background: linear-gradient(100deg, #7657E8, #4C8FEA);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 12px 24px;
    font-weight: 700;
    min-height: 48px;
    transition: 0.2s ease;
}

.stButton > button:hover {
    border: none;
    box-shadow: 0 8px 25px rgba(111, 89, 232, 0.35);
    transform: translateY(-1px);
}

.stDownloadButton > button {
    background: #18233C;
    border: 1px solid #53618A;
    color: #E8E9FF;
    border-radius: 11px;
    font-weight: 600;
    min-height: 44px;
}

.stDownloadButton > button:hover {
    border-color: #A78BFA;
    color: white;
}

.metric-card {
    background: linear-gradient(145deg, #171E36, #12192D);
    border: 1px solid rgba(148,163,184,0.18);
    border-radius: 16px;
    padding: 20px;
    min-height: 112px;
}

.metric-label {
    color: #A5AEC9;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.7px;
    text-transform: uppercase;
}

.metric-value {
    color: #FFFFFF;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 30px;
    font-weight: 700;
    margin-top: 8px;
}

div[data-testid="stExpander"] {
    background: #141C32;
    border: 1px solid #293654;
    border-radius: 14px;
    margin-bottom: 10px;
}

div[data-testid="stExpander"] summary {
    color: #F4F5FF;
    font-weight: 600;
}

.stCaption {
    color: #929AB5 !important;
}

hr {
    border-color: rgba(148,163,184,0.15);
}

.footer {
    text-align: center;
    color: #7F89A6;
    font-size: 12px;
    padding: 24px 0 5px 0;
}

.small-label {
    color: #A5AEC9;
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}

</style>
""", unsafe_allow_html=True)


# -------------------- HERO --------------------

st.markdown("""
<div class="hero">
    <div class="hero-tag">✦ INCUBRIX · CONTENT INTELLIGENCE</div>
    <h1>One idea.<br><span>Endless content.</span></h1>
    <p>
        Turn your articles, blogs and transcripts into social media drafts.
        Create smarter, repurpose faster and build a consistent content workflow.
    </p>
</div>
""", unsafe_allow_html=True)


# -------------------- SOURCE MATERIAL --------------------

st.markdown("""
<div class="section-heading">01 · Your source material</div>
<div class="section-sub">
Upload an article or paste your content to get started.
</div>
""", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="panel">', unsafe_allow_html=True)

    uploaded = st.file_uploader(
        "Upload your article or transcript",
        type=["txt", "md"],
        help="Supported formats: TXT and MD"
    )

    pasted_text = st.text_area(
        "Or paste your blog, article, podcast or webinar transcript",
        height=170,
        placeholder="Start with your source material..."
    )

    source_text = pasted_text.strip()
    source_name = "Pasted content"

    if uploaded is not None:
        source_text = uploaded.getvalue().decode(
            "utf-8", errors="replace"
        ).strip()
        source_name = uploaded.name

    if source_text:
        st.success(
            f"Source loaded: {source_name} · {len(source_text):,} characters"
        )
    else:
        st.caption("Supported formats: TXT · MD")

    st.markdown('</div>', unsafe_allow_html=True)


# -------------------- GENERATION SETTINGS --------------------

st.markdown("""
<div class="section-heading">02 · Generation settings</div>
<div class="section-sub">
Choose how many content drafts you want to create.
</div>
""", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="panel">', unsafe_allow_html=True)

    count = st.slider(
        "Number of content drafts",
        min_value=1,
        max_value=30,
        value=10,
        step=1
    )

    st.markdown(
        f'<div class="small-label">Selected drafts</div>'
        f'<div style="font-size:25px;font-weight:700;color:#C4B5FD;'
        f'margin-top:5px;">{count} drafts</div>',
        unsafe_allow_html=True
    )

    generate_button = st.button(
        "✦  Generate content",
        type="primary",
        use_container_width=True
    )

    st.markdown('</div>', unsafe_allow_html=True)


# -------------------- GENERATE CONTENT --------------------

if generate_button:
    if not source_text:
        st.warning("Please upload a source file or paste your content first.")
    else:
        try:
            with st.spinner("Creating your content drafts..."):
                result = generate(source_text, count)

            st.session_state["result"] = result
            st.session_state["source_name"] = source_name
            st.success("Content generation completed!")

        except Exception as error:
            st.error(f"Generation failed: {error}")


# -------------------- RESULTS --------------------

if "result" in st.session_state:

    result = st.session_state["result"]
    items = result["items"]

    st.markdown("""
    <div class="section-heading">03 · Your content results</div>
    <div class="section-sub">
    Review your generated drafts and prepare them for your content workflow.
    </div>
    """, unsafe_allow_html=True)

    a, b, c = st.columns(3)

    with a:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Drafts generated</div>
            <div class="metric-value">{len(items)}</div>
        </div>
        """, unsafe_allow_html=True)

    with b:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Rejected drafts</div>
            <div class="metric-value">{len(result['rejected'])}</div>
        </div>
        """, unsafe_allow_html=True)

    with c:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Runtime (minutes)</div>
            <div class="metric-value">{result['runtime_minutes']:.5f}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="section-heading">Generated content</div>
    """, unsafe_allow_html=True)

    for index, item in enumerate(items, start=1):
        heading = (
            f"✦ {index}. {item['platform']} · "
            f"{item['format']} · {item['asset_id']}"
        )

        with st.expander(heading, expanded=(index == 1)):

            st.markdown("**Content hook**")
            st.write(item["hook"])

            st.markdown("**Caption**")
            st.write(item["caption"])

            st.markdown("**Call to action**")
            st.write(item["cta"])

            st.markdown("**Tracking link**")
            st.code(item["utm_link"], language=None)

            st.caption(
                f"Content pillar: {item.get('content_pillar', 'N/A')} "
                f"· Review status: {item.get('status', 'Draft')}"
            )

    # -------------------- EXPORT --------------------

    st.markdown("""
    <div class="section-heading">04 · Export your content</div>
    <div class="section-sub">
    Download your generated drafts for further review and editing.
    </div>
    """, unsafe_allow_html=True)

    csv_path = ROOT / "outputs" / "generated_content.csv"
    export_csv(items, csv_path)

    col1, col2 = st.columns(2)

    with col1:
        st.download_button(
            "↓  Download CSV",
            data=csv_path.read_bytes(),
            file_name="incubrix_generated_content.csv",
            mime="text/csv",
            use_container_width=True
        )

    with col2:
        st.download_button(
            "↓  Download JSON",
            data=json.dumps(result, indent=2).encode("utf-8"),
            file_name="incubrix_generated_content.json",
            mime="application/json",
            use_container_width=True
        )


# -------------------- FOOTER --------------------

st.markdown("""
<hr>
<div class="footer">
    <strong>IncuBrix Social Content Studio</strong><br>
    Assessment prototype · Human review required before publishing<br><br>
    Offline mode uses deterministic templates, not a trained AI model.
    Product claims, content rights, platform formats, links and final media
    should be reviewed before publishing.
</div>
""", unsafe_allow_html=True)

