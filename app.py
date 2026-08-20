import streamlit as st
from PyPDF2 import PdfReader
from PIL import Image
import pytesseract

# Page Configuration
st.set_page_config(
    page_title="Social Media Content Analyzer",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (Scoped safely)
st.markdown("""
    <style>
    /* Prevent container misalignment */
    div[data-testid="column"] {
        width: 100%;
    }
    /* Clean text area display */
    textarea {
        font-family: monospace;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("⚡ Analyzer Hub")
    st.markdown("---")
    st.markdown("**Supported Formats:**")
    st.write("• 📄 PDF Documents")
    st.write("• 🖼️ PNG, JPG, JPEG Images")
    st.markdown("---")
    st.info("💡 **Pro-Tip:** Upload high-resolution images for maximum OCR accuracy.")

# Header
st.title("Social Media Content Analyzer")
st.caption("Upload documents or image posts to extract text and analyze engagement strategies.")
st.markdown("---")

# Main Split Layout
col_upload, col_preview = st.columns([1, 1], gap="large")

with col_upload:
    with st.container(border=True):
        st.subheader("📤 Document Upload")
        uploaded_file = st.file_uploader(
            "Drop your post file here",
            type=["pdf", "png", "jpg", "jpeg"],
            help="Upload post drafts, infographics, or screenshot graphics."
        )

    extracted_text = ""
    
    if uploaded_file is not None:
        file_type = uploaded_file.name.split(".")[-1].lower()
        
        with st.container(border=True):
            st.subheader("🖼️ Media Preview")
            if file_type in ["png", "jpg", "jpeg"]:
                image = Image.open(uploaded_file)
                st.image(image, use_container_width=True)
                
                with st.spinner("Running OCR text extraction..."):
                    try:
                        extracted_text = pytesseract.image_to_string(image)
                    except Exception as e:
                        st.error(f"OCR Error: {str(e)}")
                        
            elif file_type == "pdf":
                st.info(f"📄 Loaded PDF: **{uploaded_file.name}**")
                with st.spinner("Extracting text from PDF..."):
                    try:
                        pdf_reader = PdfReader(uploaded_file)
                        for page in pdf_reader.pages:
                            text = page.extract_text()
                            if text:
                                extracted_text += text + "\n"
                    except Exception as e:
                        st.error(f"PDF Extraction Error: {str(e)}")

with col_preview:
    with st.container(border=True):
        st.subheader("📊 Content & Engagement Analysis")
        
        if uploaded_file is None:
            st.info("👈 Upload a file on the left to display analysis.")
        elif not extracted_text.strip():
            st.warning("⚠️ No readable text could be extracted from this file.")
        else:
            word_count = len(extracted_text.split())
            char_count = len(extracted_text)
            read_time = max(1, word_count // 200)

            # Native Metric Row Alignment
            m1, m2, m3 = st.columns(3)
            m1.metric("Words", word_count)
            m2.metric("Characters", char_count)
            m3.metric("Est. Read Time", f"{read_time} min")
            
            st.markdown("---")
            
            # Tabbed interface
            tab_suggestions, tab_text = st.tabs(["💡 Engagement Feedback", "📄 Extracted Text"])
            
            with tab_suggestions:
                st.markdown("### Actionable Recommendations")
                
                suggestions = []
                if "?" not in extracted_text:
                    suggestions.append(("❓ Add a Question", "Posts with open questions increase comment engagement."))
                if "http" not in extracted_text and "www" not in extracted_text:
                    suggestions.append(("🔗 Include a CTA", "Add a link or direct readers to your bio to capture traffic."))
                if "#" not in extracted_text:
                    suggestions.append(("🏷️ Add Hashtags", "Include 3 to 5 targeted hashtags to improve post reach."))
                if word_count > 150:
                    suggestions.append(("✂️ Trim Length", "Social posts usually perform best when under 100-120 words."))
                elif word_count < 10:
                    suggestions.append(("📝 Expand Content", "This post is very short. Provide more context for value."))

                if suggestions:
                    for title, desc in suggestions:
                        with st.container(border=True):
                            st.markdown(f"**{title}**")
                            st.caption(desc)
                else:
                    st.success("✨ Great job! Your content contains strong engagement elements.")

            with tab_text:
                st.text_area("Extracted Content", extracted_text, height=300)