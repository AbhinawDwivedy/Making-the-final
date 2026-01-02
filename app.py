
# import streamlit as st
# import json, os
# import yaml
# from dotenv import load_dotenv
# from generate import GenerateEmail
# from judge import EmailJudge

# load_dotenv()

# st.set_page_config(page_title="AI Email Editor", page_icon="📧", layout="wide")

# def load_jsonl(p):
#     d=[]
#     with open(p,"r",encoding="utf-8") as f:
#         for l in f:
#             if l.strip():
#                 d.append(json.loads(l))
#     return d

# DATASETS={
#     "Lengthen":"datasets/lengthen.jsonl",
#     "Shorten":"datasets/shorten.jsonl",
#     "Tone":"datasets/tone.jsonl"
# }

# gen=GenerateEmail(os.getenv("OPENAI_MODEL"))
# judge=EmailJudge()

# with open("prompts.yaml","r",encoding="utf-8") as f:
#     prompts=yaml.safe_load(f)

# eval_system_prompt=prompts["evaluate"]["system"]
# eval_user_prompt=prompts["evaluate"]["user"]

# if "generated_text" not in st.session_state:
#     st.session_state.generated_text=""
# if "show_tone_dropdown" not in st.session_state:
#     st.session_state.show_tone_dropdown=False
# if "eval_result" not in st.session_state:
#     st.session_state.eval_result=None

# st.title("📧 AI Email Editing Tool")

# dataset=st.sidebar.selectbox("Select Dataset",DATASETS.keys())
# emails=load_jsonl(DATASETS[dataset])
# if not emails:
#     st.stop()

# ids=[e["id"] for e in emails]
# eid=st.sidebar.selectbox("Select Email ID",ids)
# email=next(e for e in emails if e["id"]==eid)

# st.markdown(f"### ✉️ Email ID: `{eid}`")
# st.markdown(f"**From:** {email['sender']}")
# st.markdown(f"**Subject:** {email['subject']}")

# text=st.text_area("Email Content",email["content"],height=250)

# c1,c2,c3=st.columns(3)

# with c1:
#     if st.button("Elaborate"):
#         st.session_state.generated_text=gen.generate("lengthen",text)
#         st.session_state.eval_result=None

# with c2:
#     if st.button("Shorten"):
#         st.session_state.generated_text=gen.generate("shorten",text)
#         st.session_state.eval_result=None

# with c3:
#     if st.button("Change tone"):
#         st.session_state.show_tone_dropdown=True
#     if st.session_state.show_tone_dropdown:
#         tone=st.selectbox(
#             "Select tone",
#             ["Friendly","Sympathetic","Professional"],
#             index=None,
#             placeholder="Choose tone"
#         )
#         if tone:
#             st.session_state.generated_text=gen.generate("tone",text,tone)
#             st.session_state.show_tone_dropdown=False
#             st.session_state.eval_result=None

# if st.session_state.generated_text:
#     st.text_area("Result",st.session_state.generated_text,height=250)

#     if st.button("🔍 Evaluate Response"):
#         st.session_state.eval_result=judge.evaluate(
#             original=text,
#             edited=st.session_state.generated_text,
#             system_prompt=eval_system_prompt,
#             user_prompt=eval_user_prompt
#         )

# if st.session_state.eval_result:
#     r=st.session_state.eval_result

#     st.subheader("Evaluation Result")

#     st.metric(
#         "Faithfulness",
#         f"{r['faithfulness']['score']} / 5"
#     )

#     with st.expander("Why this score?"):
#         st.write(r["faithfulness"]["reason"])
import streamlit as st
import json, os
import yaml
from dotenv import load_dotenv
from generate import GenerateEmail
from judge import EmailJudge

load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Email Editor",
    page_icon="📧",
    layout="wide"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .selection-mode-active {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 10px 15px;
        border-radius: 10px;
        margin-bottom: 15px;
    }
    .full-mode-active {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 10px 15px;
        border-radius: 10px;
        margin-bottom: 15px;
    }
    .stTextArea textarea {
        font-family: 'Segoe UI', sans-serif;
    }
    .preview-box {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #667eea;
    }
    div[data-testid="stRadio"] > label {
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)


def load_jsonl(path):
    data = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                data.append(json.loads(line))
    return data


DATASETS = {
    "Lengthen": "datasets/lengthen.jsonl",
    "Shorten": "datasets/shorten.jsonl",
    "Tone": "datasets/tone.jsonl"
}

gen = GenerateEmail(os.getenv("OPENAI_MODEL"))
judge = EmailJudge()

with open("prompts.yaml", "r", encoding="utf-8") as f:
    prompts = yaml.safe_load(f)

# Session state initialization
if "generated_text" not in st.session_state:
    st.session_state.generated_text = ""
if "eval_result" not in st.session_state:
    st.session_state.eval_result = None
if "show_tone" not in st.session_state:
    st.session_state.show_tone = False
if "selection_mode" not in st.session_state:
    st.session_state.selection_mode = False
if "selected_text_input" not in st.session_state:
    st.session_state.selected_text_input = ""
if "original_selection" not in st.session_state:
    st.session_state.original_selection = ""
if "email_content_override" not in st.session_state:
    st.session_state.email_content_override = None
if "applied_message" not in st.session_state:
    st.session_state.applied_message = False
if "email_refresh_counter" not in st.session_state:
    st.session_state.email_refresh_counter = 0

# Header
st.title("📧 AI Email Editing Tool")

# Sidebar - Dataset and Email Selection
dataset = st.sidebar.selectbox("Select Dataset", DATASETS.keys())
emails = load_jsonl(DATASETS[dataset])

ids = [e["id"] for e in emails]
eid = st.sidebar.selectbox("Select Email ID", ids)
email = next(e for e in emails if e["id"] == eid)

# Track current email to detect changes and reset override
current_email_key = f"{dataset}_{eid}"
if "current_email_key" not in st.session_state:
    st.session_state.current_email_key = current_email_key

# Reset override when email selection changes
if st.session_state.current_email_key != current_email_key:
    st.session_state.email_content_override = None
    st.session_state.generated_text = ""
    st.session_state.selected_text_input = ""
    st.session_state.original_selection = ""
    st.session_state.eval_result = None
    st.session_state.current_email_key = current_email_key

# Main content
st.markdown(f"### ✉️ Email ID `{eid}`")
st.markdown(f"**From:** {email['sender']}")
st.markdown(f"**Subject:** {email['subject']}")

# Email content text area - use override if available, otherwise use original
current_email_content = st.session_state.email_content_override if st.session_state.email_content_override else email["content"]

# Show success message if just applied
if st.session_state.applied_message:
    st.success("✅ Changes applied to email!")
    st.session_state.applied_message = False

text = st.text_area(
    "Email Content",
    current_email_content,
    height=200,
    help="This is the full email content. You can edit it directly or select specific text below.",
    key=f"email_content_{current_email_key}_{st.session_state.email_refresh_counter}"
)

st.divider()

# ==========================================
# EDITING MODE SELECTION
# ==========================================

col_mode1, col_mode2 = st.columns(2)

with col_mode1:
    if st.button("📝 Edit Full Email", use_container_width=True, 
                 type="primary" if not st.session_state.selection_mode else "secondary"):
        st.session_state.selection_mode = False
        st.session_state.selected_text_input = ""
        st.session_state.generated_text = ""
        st.session_state.eval_result = None

with col_mode2:
    if st.button("✂️ Edit Selected Text", use_container_width=True,
                 type="primary" if st.session_state.selection_mode else "secondary"):
        st.session_state.selection_mode = True
        st.session_state.generated_text = ""
        st.session_state.eval_result = None

# Mode indicator
if st.session_state.selection_mode:
    st.markdown("""
    <div class="selection-mode-active">
        ✂️ <strong>Selection Mode Active</strong> — Paste or type the specific text you want to edit below
    </div>
    """, unsafe_allow_html=True)
    
    # Selected text input
    st.session_state.selected_text_input = st.text_area(
        "Text to Edit",
        st.session_state.selected_text_input,
        height=100,
        placeholder="Paste or type the specific portion of the email you want to shorten, elaborate, or change tone...",
        help="Copy a portion from the email above and paste it here. Only this text will be edited."
    )
    
    # Validation
    if st.session_state.selected_text_input:
        if st.session_state.selected_text_input.strip() not in text:
            st.warning("⚠️ The selected text doesn't match exactly with the email content. Make sure to copy it exactly.")
        else:
            st.success("✓ Selected text found in email")
else:
    st.markdown("""
    <div class="full-mode-active">
        📝 <strong>Full Email Mode</strong> — Actions will apply to the entire email
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ==========================================
# ACTION BUTTONS
# ==========================================

st.markdown("### 🛠️ Actions")
c1, c2, c3 = st.columns(3)

# Get the text to edit
text_to_edit = st.session_state.selected_text_input if st.session_state.selection_mode else None
can_edit = not st.session_state.selection_mode or (st.session_state.selected_text_input.strip() != "")

with c1:
    if st.button("📖 Elaborate", use_container_width=True, disabled=not can_edit):
        if st.session_state.selection_mode:
            st.session_state.original_selection = st.session_state.selected_text_input
            st.session_state.generated_text = gen.generate(
                "lengthen", 
                text, 
                selected_text=st.session_state.selected_text_input
            )
        else:
            st.session_state.generated_text = gen.generate("lengthen", text)
        st.session_state.eval_result = None
        st.session_state.show_tone = False

with c2:
    if st.button("✂️ Shorten", use_container_width=True, disabled=not can_edit):
        if st.session_state.selection_mode:
            st.session_state.original_selection = st.session_state.selected_text_input
            st.session_state.generated_text = gen.generate(
                "shorten", 
                text, 
                selected_text=st.session_state.selected_text_input
            )
        else:
            st.session_state.generated_text = gen.generate("shorten", text)
        st.session_state.eval_result = None
        st.session_state.show_tone = False

with c3:
    if st.button("🎭 Change Tone", use_container_width=True, disabled=not can_edit):
        st.session_state.show_tone = True
        st.session_state.generated_text = ""
        st.session_state.eval_result = None

# Tone selection dropdown
if st.session_state.show_tone:
    tone = st.selectbox(
        "Select Tone",
        ["Friendly", "Sympathetic", "Professional"],
        index=None,
        placeholder="Choose a tone..."
    )
    if tone:
        if st.session_state.selection_mode:
            st.session_state.original_selection = st.session_state.selected_text_input
            st.session_state.generated_text = gen.generate(
                "tone", 
                text, 
                tone=tone,
                selected_text=st.session_state.selected_text_input
            )
        else:
            st.session_state.generated_text = gen.generate("tone", text, tone=tone)
        st.session_state.show_tone = False
        st.session_state.eval_result = None

# ==========================================
# RESULTS DISPLAY
# ==========================================

if st.session_state.generated_text:
    st.divider()
    st.markdown("### 📄 Result")
    
    if st.session_state.selection_mode and st.session_state.original_selection:
        # Show both the edited selection AND preview in context
        tab1, tab2 = st.tabs(["✏️ Edited Selection", "📋 Preview in Context"])
        
        # Get the base email content for replacement
        base_content = st.session_state.email_content_override if st.session_state.email_content_override else email["content"]
        
        with tab1:
            st.text_area(
                "Edited Text",
                st.session_state.generated_text,
                height=150
            )
            
            # APPLY BUTTON - Updates the main email content
            if st.button("✅ Apply to Main Email", type="primary", use_container_width=True):
                full_edited = base_content.replace(
                    st.session_state.original_selection,
                    st.session_state.generated_text
                )
                st.session_state.email_content_override = full_edited
                st.session_state.email_refresh_counter += 1  # Force text_area to refresh
                st.session_state.generated_text = ""
                st.session_state.original_selection = ""
                st.session_state.selected_text_input = ""
                st.session_state.applied_message = True
                st.rerun()
        
        with tab2:
            # Show how it looks in the full email
            preview_text = base_content.replace(
                st.session_state.original_selection, 
                f"**→ {st.session_state.generated_text} ←**"
            )
            st.markdown("*Preview showing where your edited text fits in the email:*")
            st.markdown(f"""```
{base_content.replace(st.session_state.original_selection, f">>> {st.session_state.generated_text} <<<")}
```""")
            
            # Full edited email preview
            full_edited = base_content.replace(
                st.session_state.original_selection,
                st.session_state.generated_text
            )
            st.text_area(
                "Full Email with Replacement",
                full_edited,
                height=200,
                help="This is the complete email with your selected text replaced"
            )
    else:
        # Full email mode - show result directly
        st.text_area(
            "Edited Email",
            st.session_state.generated_text,
            height=250
        )

    # Evaluate button
    if st.button("🔍 Evaluate"):
        if st.session_state.selection_mode and st.session_state.original_selection:
            # Evaluate the selection edit
            st.session_state.eval_result = judge.evaluate(
                original=st.session_state.original_selection,
                edited=st.session_state.generated_text
            )
        else:
            st.session_state.eval_result = judge.evaluate(
                original=text,
                edited=st.session_state.generated_text
            )

# ==========================================
# EVALUATION DISPLAY
# ==========================================

if st.session_state.eval_result:
    r = st.session_state.eval_result

    st.subheader("📊 Evaluation")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Faithfulness", f"{r['faithfulness']['score']} / 5")
    col2.metric("Completeness", f"{r['completeness']['score']} / 5")
    col3.metric("Robustness", f"{r['robustness']['score']} / 5")
    col4.metric("Overall", f"{r['overall']['score']} / 5")

    with st.expander("📝 Why these scores?"):
        st.write("**Faithfulness:**", r["faithfulness"]["reason"])
        st.write("**Completeness:**", r["completeness"]["reason"])
        st.write("**Robustness:**", r["robustness"]["reason"])
        st.write("**Overall:**", r["overall"]["reason"])

