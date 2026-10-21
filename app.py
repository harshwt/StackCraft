import json
from pathlib import Path
import streamlit as st
from main import run_pipeline
from validator import extract_json

st.set_page_config(
    page_title="Stackcraft",
    page_icon="S",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

.block-container{
    padding-top:1rem;
    max-width:900px;
}

.stButton > button{
    width:100%;
    height:55px;
    border-radius:12px;
    font-size:18px;
    font-weight:600;
}

.hero-title{
    text-align:center;
    font-size:58px;
    font-weight:800;
    margin-bottom:0px;
}

.hero-sub{
    text-align:center;
    color:#9ca3af;
    font-size:20px;
    margin-bottom:30px;
}

</style>
""", unsafe_allow_html=True)

# Logo
logo_path = Path(__file__).resolve().parent / "applogo.png"
if logo_path.exists():
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        st.image(str(logo_path), width=200)

# Title
st.markdown(
    """
    <div class='hero-title'>
        Stackcraft
    </div>

    <div class='hero-sub'>
        Compile natural language requirements into structured application specifications.
    </div>
    """,
    unsafe_allow_html=True
)

# Prompt
user_prompt = st.text_area(
    label="Application Requirements",
    label_visibility="collapsed",
    placeholder="""Examples:

• Build a CRM with login, analytics and payments

• Create an e-commerce platform with inventory management

• Build a task manager with teams and notifications""",
    height=180
)

# Centered Generate Button
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    generate = st.button(
        "Compile Application",
        use_container_width=True
    )

def _format_display(raw_content: str, default_lang: str = "json") -> str:
    """Format string to pretty JSON if possible, else return as-is."""
    if not raw_content:
        return ""
    parsed, _ = extract_json(raw_content)
    if parsed:
        return json.dumps(parsed, indent=2)
    return raw_content

# Generate
if generate:
    if not user_prompt.strip():
        st.error("Please describe an application first.")
        st.stop()

    try:
        with st.spinner("Compiling application blueprint..."):
            result = run_pipeline(user_prompt)
    except Exception as e:
        st.error(f"Pipeline error during execution: {e}")
        st.stop()

    st.divider()

    if result.get("repaired"):
        st.info("ℹ️ Schema auto-repair was triggered to fix syntax or structural formatting.")

    if result["valid"]:
        st.success("Your Application Blueprint is Ready!")
    else:
        st.error(f"Schema Validation Warning: {result['message']}")

    tab1, tab2, tab3, tab4 = st.tabs(
        ["Requirements", "Architecture", "Specification", "Application"]
    )

    with tab1:
        st.code(
            _format_display(result["intent"]),
            language="json"
        )

    with tab2:
        st.code(
            _format_display(result["design"]),
            language="json"
        )

    with tab3:
        st.code(
            _format_display(result["schema"]),
            language="json"
        )

    with tab4:
        if result["generated_code"]:
            st.code(
                result["generated_code"],
                language="python"
            )
            st.download_button(
                label="Download Application Code",
                data=result["generated_code"],
                file_name="application.py",
                mime="text/plain"
            )
        else:
            st.warning("Code generation was skipped because schema validation could not be resolved.")