import os
import shutil
import zipfile
import base64
import pandas as pd
import streamlit as st

# Internal extraction and reporting pipelines
from src.extraction.native_text import extract_text_from_pdf
from src.extraction.image_to_text import extract_text_from_image
from src.reporting.reporting import generate_interactive_report, generate_interactive_csv_summary
from src.reporting.pdf_reporter import generate_final_pdf_report

# Workspace Directory Configurations
INPUT_DIR = "data/input"
REPORT_DIR = "data/output"
SORTED_DIR = "data/sorted"
SUMMARY_DIR = "data/summary"

SUMMARY_CSV_PATH = os.path.join(SUMMARY_DIR, "final_interactive_summary.csv")
SUMMARY_PDF_PATH = os.path.join(SUMMARY_DIR, "Executive_Audit_Report.pdf")

# Set wide layout and professional title
st.set_page_config(page_title="Automated Fraud Risk Parser", page_icon="🏦", layout="wide")

def reset_workspace():
    """Clears and rebuilds system tracking directories to prevent cross-contamination."""
    for path in [INPUT_DIR, REPORT_DIR, SUMMARY_DIR, f"{SORTED_DIR}/flagged", f"{SORTED_DIR}/clean"]:
        if os.path.exists(path):
            shutil.rmtree(path)
        os.makedirs(path, exist_ok=True)

def handle_uploaded_files(uploaded_files):
    """Saves PDFs and extracts ZIP archives directly into the input target matrix."""
    for uploaded_file in uploaded_files:
        file_path = os.path.join(INPUT_DIR, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # If it's a zip, extract it and remove the base zip file
        if uploaded_file.name.lower().endswith(".zip"):
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(INPUT_DIR)
            os.remove(file_path)

def display_pdf(file_path):
    """Renders the generated PDF directly inside the Streamlit dashboard via base64 iframe."""
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800px" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

# ==========================================
# STREAMLIT DASHBOARD UI
# ==========================================

# Bank of Baroda Logo and Title Header
col1, col2 = st.columns([1, 6])
with col1:
    bob_logo_png = "/home/mukesh/GITHUB/doc-parser-update/boblogo.jpg"
    st.image(bob_logo_png, use_container_width=True)
with col2:
    st.title("Automated Fraud Risk Parser")
    # st.markdown("Intelligent FMR parsing with dual-stream token tracking, fuzzy query mapping, and deep text recognition fallbacks.")
st.write("---")

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    user_prompt = st.text_area(
        "Interactive Text Query Constraint:", 
        value="Whether the account is identified as fraud?",
        height=100
    )
    
    st.markdown("### 📄 Upload Document")
    uploaded_files = st.file_uploader(
        "Upload PDF files or a ZIP archive", 
        type=["pdf", "zip"], 
        accept_multiple_files=True
    )
    
    run_btn = st.button(" Run Audit Pipeline", use_container_width=True)
    

# Main Execution Trigger
if run_btn:
    if not uploaded_files:
        st.warning("⚠️ Please upload at least one PDF or ZIP file to begin.")
    else:
        # 1. Initialize Pipeline Workspace
        reset_workspace()
        handle_uploaded_files(uploaded_files)
        
        target_pdfs = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(".pdf")]
        
        if not target_pdfs:
            st.error("❌ No valid PDF files found inside the upload matrix.")
        else:
            all_processed_reports = []
            
            # 2. Execution Processing Ring
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i, filename in enumerate(target_pdfs):
                status_text.text(f"Processing: {filename} ({i+1}/{len(target_pdfs)})...")
                file_path = os.path.join(INPUT_DIR, filename)
                
                # Stream A: Native Text Extraction
                extracted_text = extract_text_from_pdf(file_path)
                
                # Stream B: OCR Fallback for flattened images
                if not extracted_text:
                    extracted_text = extract_text_from_image(file_path)
                
                if not extracted_text:
                    continue
                
                # Dual-Stream Tracking Engine Execution
                report = generate_interactive_report(extracted_text, filename, user_prompt, REPORT_DIR)
                all_processed_reports.append(report)
                
                # Segregate Outputs
                is_flagged = len(report["primary_keywords"]) > 0 or report["fraud_answer"] == "YES"
                target_folder = "flagged" if is_flagged else "clean"
                shutil.copy(file_path, os.path.join(SORTED_DIR, target_folder, filename))
                
                progress_bar.progress((i + 1) / len(target_pdfs))

            status_text.text("Building final audit summary deliverables...")

            # 3. Deliverables Compilation
            if all_processed_reports:
                generate_interactive_csv_summary(all_processed_reports, SUMMARY_CSV_PATH)
                generate_final_pdf_report(REPORT_DIR, SUMMARY_PDF_PATH)
                
                # Calculate Core Metrics
                total_docs = len(all_processed_reports)
                total_flagged = sum(1 for r in all_processed_reports if len(r["primary_keywords"]) > 0 or r["fraud_answer"] == "YES")
                total_clean = total_docs - total_flagged
                
                # Calculate the NEW dynamic query metric
                total_query_matches = sum(1 for r in all_processed_reports if r.get("query_answer") == "YES")
                
                status_text.empty()
                progress_bar.empty()
                
                st.success("✅ Audit process complete!")
                
                # 4. Metric Dashboard Columns (Updated to 4 columns)
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Total Scanned", total_docs)
                c2.metric("Flagged Documents", total_flagged)
                c3.metric("Clean Documents", total_clean)
                c4.metric("Query Matches (YES)", total_query_matches, delta="Dynamic Hit", delta_color="off")
                
                st.write("---")
                
                # 5. Display Reports & Download Buttons Matrix
                tab1, tab2 = st.tabs(["📊 Live CSV Data", "📑 Executive PDF Report"])
                
                with tab1:
                    df = pd.read_csv(SUMMARY_CSV_PATH, skiprows=5) # Skips the custom report header to show clean grid
                    st.dataframe(df, use_container_width=True)
                    
                    with open(SUMMARY_CSV_PATH, "rb") as csv_file:
                        st.download_button(
                            label="📥 Download Full CSV Audit",
                            data=csv_file,
                            file_name="Audit_Summary.csv",
                            mime="text/csv",
                            use_container_width=True
                        )
                
                with tab2:
                    with open(SUMMARY_PDF_PATH, "rb") as pdf_file:
                        st.download_button(
                            label="📥 Download Executive PDF",
                            data=pdf_file,
                            file_name="Executive_Audit_Report.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                    st.markdown("### Report Preview:")
                    display_pdf(SUMMARY_PDF_PATH)
            else:
                st.error("No valid text could be processed from the uploaded files.")
st.markdown("---")
st.markdown("<div style='text-align: center; color: gray; padding-top: 20px; padding-bottom: 20px;'><b>BANK OF BARODA</b></div>", unsafe_allow_html=True)