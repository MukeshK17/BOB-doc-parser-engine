# import os
# import shutil
# import zipfile
# import base64
# import pandas as pd
# import streamlit as st
# import streamlit.components.v1 as components
# import altair as alt


# # ==========================================================
# # INTERNAL EXTRACTION & REPORTING PIPELINES
# # ==========================================================
# from src.extraction.native_text import extract_text_from_pdf
# from src.extraction.image_to_text import extract_text_from_image
# from src.reporting.reporting import (
#     generate_interactive_report,
#     generate_interactive_csv_summary,
# )
# from src.reporting.pdf_reporter import generate_final_pdf_report


# # ==========================================================
# # WORKSPACE CONFIGURATION
# # ==========================================================
# INPUT_DIR = "data/input"
# REPORT_DIR = "data/output"
# SORTED_DIR = "data/sorted"
# SUMMARY_DIR = "data/summary"

# SUMMARY_CSV_PATH = os.path.join(
#     SUMMARY_DIR,
#     "final_interactive_summary.csv",
# )

# SUMMARY_PDF_PATH = os.path.join(
#     SUMMARY_DIR,
#     "Executive_Audit_Report.pdf",
# )

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# BOB_LOGO_PATH = os.path.join(BASE_DIR, "boblogo.jpg")


# # ==========================================================
# # PAGE CONFIGURATION
# # ==========================================================
# st.set_page_config(
#     page_title="BoB Sentinel AI",
#     page_icon="🏦",
#     layout="wide",
#     initial_sidebar_state="collapsed",
# )


# # ==========================================================
# # SESSION STATE INITIALIZATION
# # ==========================================================

# # Reset uploader widget
# if "uploader_key" not in st.session_state:
#     st.session_state.uploader_key = 0

# # KPI values shown on dashboard
# if "metrics" not in st.session_state:
#     st.session_state.metrics = {
#         "total": "-",
#         "flagged": "-",
#         "clean": "-",
#         "query": "-",
#     }

# # Analysis completion flag
# if "analysis_completed" not in st.session_state:
#     st.session_state.analysis_completed = False

# # Keeps reports visible after reruns
# if "reports_ready" not in st.session_state:
#     st.session_state.reports_ready = False


# def inject_custom_ui():
#     st.markdown(
#         """
#         <style>

#         :root{
#             --bob-orange:#f36f21;
#             --bob-blue:#102b55;
#             --bg:#f4f7fb;
#             --card:#ffffff;
#             --border:#e6ecf3;
#             --muted:#667085;
#         }

#         /* ================================================= */
#         /* GLOBAL */
#         /* ================================================= */

#         .stApp{
#             background:linear-gradient(
#                 180deg,
#                 #eef2f7 0%,
#                 #f8fafc 100%
#             );
#         }

#         .main .block-container{
#             max-width:1500px;
#             padding-top:1.5rem;
#             padding-bottom:2rem;
#         }

#         /* ================================================= */
#         /* HEADER */
#         /* ================================================= */

#         .hero-wrap{
#             background:var(--card);
#             border-radius:28px;
#             padding:2.5rem;
#             min-height:220px;

#             border:1px solid var(--border);

#             box-shadow:
#                 0 8px 32px rgba(16,43,85,0.05);

#             text-align:center;
#         }

#         .hero-title{
#             color:var(--bob-blue);
#             font-size:3.2rem;
#             font-weight:900;
#             line-height:1.05;
#             margin:0;
#         }

#         .hero-sub{
#             margin-top:0.8rem;
#             color:var(--muted);
#             font-size:1.25rem;
#             font-weight:500;
#         }

#         .clock-card{
#             background:white;
#             border-radius:18px;
#             border:1px solid var(--border);
#             padding:0.8rem;
#             margin-top:1rem;

#             text-align:center;

#             box-shadow:
#                 0 6px 18px rgba(16,43,85,0.04);
#         }

#         /* ================================================= */
#         /* KPI CARDS */
#         /* ================================================= */

#         .metric-card{
#             background:white;

#             border-radius:22px;

#             padding:1.5rem;

#             border:1px solid var(--border);

#             box-shadow:
#                 0 6px 18px rgba(16,43,85,0.05);

#             text-align:center;

#             min-height:130px;
#         }

#         .metric-title{
#             color:#475467;
#             font-size:1rem;
#             font-weight:700;
#         }

#         .metric-value{
#             margin-top:0.4rem;
#             color:#102b55;
#             font-size:3rem;
#             font-weight:900;
#         }

#         /* ================================================= */
#         /* SECTION CARDS */
#         /* ================================================= */

#         .section-card{
#             background:white;

#             border-radius:24px;

#             padding:1.6rem;

#             border:1px solid var(--border);

#             box-shadow:
#                 0 6px 18px rgba(16,43,85,0.05);
#         }

#         .section-title{
#             color:#102b55;
#             font-size:2rem;
#             font-weight:900;
#             margin-bottom:0.3rem;
#         }

#         .section-sub{
#             color:var(--muted);
#             font-size:0.95rem;
#             margin-bottom:1rem;
#         }

#         /* ================================================= */
#         /* TEXT AREA */
#         /* ================================================= */

#         .stTextArea textarea,
#         div[data-testid="stTextArea"] textarea,
#         textarea{

#             font-size:22px !important;
#             font-weight:600 !important;

#             color:#102b55 !important;

#             line-height:1.6 !important;

#             border-radius:18px !important;

#             background:#fcfdff !important;
#         }

#         /* ================================================= */
#         /* FILE UPLOADER */
#         /* ================================================= */

#         [data-testid="stFileUploader"]{
#             background:#fcfdff;
#             border-radius:18px;
#             padding:1rem;
#         }

#         /* ================================================= */
#         /* BUTTONS */
#         /* ================================================= */

#         .stButton > button{

#             border:none !important;

#             border-radius:14px !important;

#             min-height:2.5rem !important;

#             font-size:1rem !important;

#             font-weight:700 !important;

#             box-shadow:
#                 0 4px 12px rgba(0,0,0,0.08);

#             transition:0.25s;
#         }

#         .stButton > button:hover{
#             transform:translateY(-1px);
#         }

#         /* ================================================= */
#         /* DOWNLOAD BUTTONS */
#         /* ================================================= */

#         .stDownloadButton > button{

#             background:linear-gradient(
#                 90deg,
#                 #102b55,
#                 #183c74
#             ) !important;

#             color:white !important;

#             border:none !important;

#             border-radius:14px !important;

#             min-height:2.8rem !important;

#             font-weight:700 !important;
#         }

#         /* ================================================= */
#         /* SUCCESS CARD */
#         /* ================================================= */

#         .success-card{

#             background:#eefbf3;

#             border:1px solid #b7e4c7;

#             border-radius:18px;

#             padding:1rem 1.5rem;

#             color:#0f7b35;

#             font-size:1.1rem;

#             font-weight:700;

#             text-align:center;

#             margin-top:1rem;
#             margin-bottom:1rem;
#         }

#         /* ================================================= */
#         /* TABS */
#         /* ================================================= */

#         button[data-baseweb="tab"]{

#             font-size:1rem !important;
#             font-weight:700 !important;
#         }

#         /* ================================================= */
#         /* DATAFRAME */
#         /* ================================================= */

#         [data-testid="stDataFrame"]{

#             border-radius:18px;
#             overflow:hidden;

#             border:1px solid var(--border);
#         }

#         /* ================================================= */
#         /* FOOTER */
#         /* ================================================= */

#         .footer-bob{

#             margin-top:50px;

#             text-align:center;

#             color:#667085;

#             padding:1rem;
#         }

#         .footer-title{

#             color:#102b55;

#             font-size:1.1rem;

#             font-weight:800;
#         }

#         .footer-sub{

#             margin-top:0.4rem;

#             font-size:0.9rem;
#         }

#         </style>
#         """,
#         unsafe_allow_html=True,
#     )





# def render_live_clock():
#     components.html(
#         """
#         <div class="clock-card">
#             <div style="
#                 color:#102b55;
#                 font-size:15px;
#                 font-weight:800;
#                 margin-bottom:6px;
#             ">
#                 Dashboard Time
#             </div>

#             <div id="bob-clock"
#                  style="
#                     color:#102b55;
#                     font-size:18px;
#                     font-weight:700;
#                     font-family:system-ui,-apple-system,sans-serif;
#                  ">
#                 --
#             </div>
#         </div>

#         <script>

#             const el = document.getElementById("bob-clock");

#             function tick(){

#                 const now = new Date();

#                 const opts = {
#                     hour:'2-digit',
#                     minute:'2-digit',
#                     second:'2-digit',
#                     day:'2-digit',
#                     month:'short',
#                     year:'numeric'
#                 };

#                 el.innerText =
#                     now.toLocaleString(undefined, opts);
#             }

#             tick();
#             setInterval(tick, 1000);

#         </script>
#         """,
#         height=90,
#     )

# def reset_workspace():
#     """Clears generated outputs while preserving locally stored input files."""
#     for path in [REPORT_DIR, SUMMARY_DIR, f"{SORTED_DIR}/flagged", f"{SORTED_DIR}/clean"]:
#         if os.path.exists(path):
#             shutil.rmtree(path)
#         os.makedirs(path, exist_ok=True)
#     os.makedirs(INPUT_DIR, exist_ok=True)

# def handle_uploaded_files(uploaded_files):
#     """Saves uploaded files and returns the exact PDF file paths to process."""
#     target_pdf_paths = []
#     for uploaded_file in uploaded_files:
#         file_path = os.path.join(INPUT_DIR, uploaded_file.name)
#         with open(file_path, "wb") as f:
#             f.write(uploaded_file.getbuffer())
        
#         # If it's a zip, extract it and remove the base zip file
#         if uploaded_file.name.lower().endswith(".zip"):
#             with zipfile.ZipFile(file_path, 'r') as zip_ref:
#                 pdf_members = [
#                     member for member in zip_ref.namelist()
#                     if member.lower().endswith(".pdf") and not member.endswith("/")
#                 ]
#                 zip_ref.extractall(INPUT_DIR)
#                 for member in pdf_members:
#                     extracted_pdf = os.path.normpath(os.path.join(INPUT_DIR, member))
#                     if os.path.exists(extracted_pdf):
#                         target_pdf_paths.append(extracted_pdf)
#             os.remove(file_path)
#         elif uploaded_file.name.lower().endswith(".pdf"):
#             target_pdf_paths.append(file_path)
#     return target_pdf_paths

# def display_pdf(file_path):
#     """Renders the generated PDF directly inside the Streamlit dashboard via base64 iframe."""
#     with open(file_path, "rb") as f:
#         base64_pdf = base64.b64encode(f.read()).decode('utf-8')
#     pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800px" type="application/pdf"></iframe>'
#     st.markdown(pdf_display, unsafe_allow_html=True)


# # ==========================================
# # STREAMLIT DASHBOARD UI
# # ==========================================

# inject_custom_ui()

# # ==================================================
# # HEADER SECTION
# # ==================================================

# # header_left, header_right = st.columns([0.78, 0.22])
# header_left, header_right = st.columns([0.82, 0.18])
# # with header_left:

# #     st.markdown(
# #         """
# #         <div class="hero-wrap">

# #             <h1 class="hero-title">
# #                 BoB Sentinel AI
# #             </h1>

# #             <div class="hero-sub">
# #                 AI-Powered Compliance & Fraud Intelligence Platform
# #             </div>

# #         </div>
# #         """,
# #         unsafe_allow_html=True,
# #     )

# with header_left:
#     st.markdown(
#         """
#         <div style="
#             background:white;
#             border-radius:28px;
#             padding:40px;
#             border:1px solid #e6ecf3;
#             text-align:center;
#             box-shadow:0 8px 24px rgba(0,0,0,0.06);
#         ">

#             <h1 style="
#                 color:#102b55;
#                 font-size:54px;
#                 font-weight:900;
#                 margin-bottom:8px;
#             ">
#                 BoB Sentinel AI
#             </h1>

#             <p style="
#                 color:#667085;
#                 font-size:22px;
#             ">
#                 AI-Powered Compliance & Fraud Intelligence Platform
#             </p>

#         </div>
#         """,
#         unsafe_allow_html=True
#     )
# with header_right:

#     if os.path.exists(BOB_LOGO_PATH):

#         st.markdown(
#             """
#             <div style="
#                 background:white;
#                 border-radius:24px;
#                 padding:1rem;
#                 border:1px solid #e6ecf3;
#                 box-shadow:0 8px 24px rgba(16,43,85,0.05);
#                 text-align:center;
#             ">
#             """,
#             unsafe_allow_html=True,
#         )

#         st.image(
#             BOB_LOGO_PATH,
#             width=260,
#         )

#         st.markdown("</div>", unsafe_allow_html=True)

#     render_live_clock()

# st.markdown("<br>", unsafe_allow_html=True)

# # ==================================================
# # KPI DASHBOARD
# # ==================================================

# st.markdown("<br>", unsafe_allow_html=True)

# k1, k2, k3, k4 = st.columns(4)

# cards = [
#     ("Total Scanned", st.session_state.metrics["total"]),
#     ("Flagged Documents", st.session_state.metrics["flagged"]),
#     ("Clean Documents", st.session_state.metrics["clean"]),
#     ("Query Matches", st.session_state.metrics["query"]),
# ]

# for col, (title, value) in zip([k1, k2, k3, k4], cards):

#     with col:

#         # st.markdown(
#         #     f"""
#         #     <div class="metric-card">

#         #         <div class="metric-title">
#         #             {title}
#         #         </div>

#         #         <div class="metric-value">
#         #             {value}
#         #         </div>

#         #     </div>
#         #     """,
#         #     unsafe_allow_html=True,
#         # )
#         st.markdown(
#             f"""
#             <div style="
#                 background:white;
#                 border-radius:22px;
#                 padding:25px;
#                 text-align:center;
#                 border:1px solid #e6ecf3;
#                 box-shadow:0 4px 12px rgba(0,0,0,0.05);
#             ">

#                 <div style="
#                     color:#667085;
#                     font-size:18px;
#                     font-weight:700;
#                 ">
#                     {title}
#                 </div>

#                 <div style="
#                     color:#102b55;
#                     font-size:48px;
#                     font-weight:900;
#                     margin-top:12px;
#                 ">
#                     {value}
#                 </div>

#             </div>
#             """,
#             unsafe_allow_html=True
#         )
# # ==================================================
# # INPUT SECTION
# # ==================================================

# st.markdown("<br>", unsafe_allow_html=True)

# left, right = st.columns([1, 1], gap="large")

# # --------------------------------------------------
# # RISK QUERY CARD
# # --------------------------------------------------

# # with left:

# #     st.markdown(
# #         """
# #         <div class="section-card">
# #             <div class="section-title">
# #                 Risk Query
# #             </div>

# #             <div class="section-sub">
# #                 Ask a focused compliance or fraud-related question.
# #             </div>
# #         </div>
# #         """,
# #         unsafe_allow_html=True,
# #     )

# #     user_prompt = st.text_area(
# #         "",
# #         value="Whether the account is identified as fraud?",
# #         height=120,
# #         label_visibility="collapsed",
# #     )

# with left:

#     with st.container(border=True):

#         st.markdown(
#             """
#             <div class="section-title">
#                 Risk Query
#             </div>
#             """,
#             unsafe_allow_html=True,
#         )

#         st.caption(
#             "Ask a focused compliance or fraud-related question."
#         )

#         user_prompt = st.text_area(
#             "",
#             value="Whether the account is identified as fraud?",
#             height=110,
#             label_visibility="collapsed",
#         )
# # --------------------------------------------------
# # DOCUMENT UPLOAD CARD
# # --------------------------------------------------

# with right:

#     st.markdown(
#         """
#         <div class="section-card">
#             <div class="section-title">
#                 Upload Documents
#             </div>

#             <div class="section-sub">
#                 Upload PDF files or ZIP bundles for analysis.
#             </div>
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )

#     uploaded_files = st.file_uploader(
#         "",
#         type=["pdf", "zip"],
#         accept_multiple_files=True,
#         key=f"uploader_{st.session_state.uploader_key}",
#         label_visibility="collapsed",
#     )

#     if uploaded_files:

#         pdf_count = sum(
#             1
#             for f in uploaded_files
#             if f.name.lower().endswith(".pdf")
#         )

#         zip_count = sum(
#             1
#             for f in uploaded_files
#             if f.name.lower().endswith(".zip")
#         )

#         st.info(
#             f"Selected Files: {len(uploaded_files)} | "
#             f"PDF: {pdf_count} | ZIP: {zip_count}"
#         )

# # ==================================================
# # ACTION BUTTONS
# # ==================================================

# st.markdown("<br>", unsafe_allow_html=True)

# space1, b1, b2, space2 = st.columns([1.3, 1, 1, 1.3])

# with b1:

#     run_btn = st.button(
#         "▶ Run Analysis",
#         use_container_width=True,
#     )

# with b2:

#     clear_btn = st.button(
#         "🗑 Reset Session",
#         use_container_width=True,
#     )

# # ==================================================
# # RESET SESSION
# # ==================================================

# if clear_btn:

#     reset_workspace()

#     st.session_state.uploader_key += 1

#     st.session_state.metrics = {
#         "total": "-",
#         "flagged": "-",
#         "clean": "-",
#         "query": "-",
#     }

#     st.session_state.analysis_completed = False
#     st.session_state.reports_ready = False

#     st.rerun()

# # ==================================================
# # INFORMATION CARD
# # ==================================================

# # if not run_btn:
# #     st.info(
# #         """
# #         Upload financial documents, define a focused risk query,
# #         and run AI-powered analysis to generate compliance-ready reports.
# #         """
# #     )

# # ==================================================
# # MAIN EXECUTION
# # ==================================================

# if run_btn:

#     if not uploaded_files:
#         st.warning(
#             "Please upload at least one PDF or ZIP file to begin analysis."
#         )

#     else:

#         # ------------------------------------------------
#         # WORKSPACE INITIALIZATION
#         # ------------------------------------------------

#         reset_workspace()

#         target_pdf_paths = handle_uploaded_files(
#             uploaded_files
#         )

#         if not target_pdf_paths:

#             st.error(
#                 "No valid PDF files were detected in the uploaded batch."
#             )

#         else:

#             all_processed_reports = []

#             progress_bar = st.progress(0)

#             status_text = st.empty()

#             # ------------------------------------------------
#             # DOCUMENT PROCESSING
#             # ------------------------------------------------

#             for i, file_path in enumerate(target_pdf_paths):

#                 filename = os.path.basename(file_path)

#                 status_text.markdown(
#                     f"""
#                     **Processing Document {i+1}/{len(target_pdf_paths)}**

#                     `{filename}`
#                     """
#                 )

#                 # Native text extraction
#                 extracted_text = extract_text_from_pdf(
#                     file_path
#                 )

#                 # OCR fallback
#                 if not extracted_text:
#                     extracted_text = extract_text_from_image(
#                         file_path
#                     )

#                 if not extracted_text:
#                     continue

#                 report = generate_interactive_report(
#                     extracted_text,
#                     filename,
#                     user_prompt,
#                     REPORT_DIR,
#                 )

#                 all_processed_reports.append(report)

#                 # Output segregation
#                 is_flagged = (
#                     len(report["primary_keywords"]) > 0
#                     or report["fraud_answer"] == "YES"
#                 )

#                 target_folder = (
#                     "flagged"
#                     if is_flagged
#                     else "clean"
#                 )

#                 shutil.copy(
#                     file_path,
#                     os.path.join(
#                         SORTED_DIR,
#                         target_folder,
#                         filename,
#                     ),
#                 )

#                 progress_bar.progress(
#                     (i + 1) / len(target_pdf_paths)
#                 )

#             status_text.text(
#                 "Building final reports..."
#             )

#             # ------------------------------------------------
#             # REPORT GENERATION
#             # ------------------------------------------------

#             if all_processed_reports:

#                 generate_interactive_csv_summary(
#                     all_processed_reports,
#                     SUMMARY_CSV_PATH,
#                 )

#                 generate_final_pdf_report(
#                     REPORT_DIR,
#                     SUMMARY_PDF_PATH,
#                 )

#                 total_docs = len(
#                     all_processed_reports
#                 )

#                 total_flagged = sum(
#                     1
#                     for r in all_processed_reports
#                     if len(r["primary_keywords"]) > 0
#                     or r["fraud_answer"] == "YES"
#                 )

#                 total_clean = (
#                     total_docs - total_flagged
#                 )

#                 total_query_matches = sum(
#                     1
#                     for r in all_processed_reports
#                     if r.get("query_answer") == "YES"
#                 )

#                 # --------------------------------------------
#                 # UPDATE KPI CARDS
#                 # --------------------------------------------

#                 st.session_state.metrics = {
#                     "total": total_docs,
#                     "flagged": total_flagged,
#                     "clean": total_clean,
#                     "query": total_query_matches,
#                 }

#                 st.session_state.analysis_completed = True

#                 st.session_state.reports_ready = True

#                 progress_bar.empty()
#                 status_text.empty()

#                 st.rerun()

#             else:

#                 progress_bar.empty()

#                 status_text.empty()

#                 st.error(
#                     "No valid text could be extracted from the uploaded documents."
#                 )

# # ==================================================
# # SUCCESS MESSAGE
# # ==================================================

# if st.session_state.analysis_completed:

#     st.markdown(
#         """
#         <div class="success-card">
#             ✓ Audit completed successfully.
#             Reports are ready for review and download.
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )

# # ==================================================
# # REPORT DOWNLOADS + PREVIEWS
# # ==================================================

# if st.session_state.reports_ready:

#     st.markdown("<br>", unsafe_allow_html=True)

#     st.markdown(
#         """
#         <div class="section-title">
#             Reports & Deliverables
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )

#     d1, d2 = st.columns(2)

#     with d1:

#         with open(
#             SUMMARY_CSV_PATH,
#             "rb",
#         ) as csv_file:

#             st.download_button(
#                 "📥 Download CSV Report",
#                 data=csv_file,
#                 file_name="Audit_Summary.csv",
#                 mime="text/csv",
#                 use_container_width=True,
#             )

#     with d2:

#         with open(
#             SUMMARY_PDF_PATH,
#             "rb",
#         ) as pdf_file:

#             st.download_button(
#                 "📥 Download PDF Report",
#                 data=pdf_file,
#                 file_name="Executive_Audit_Report.pdf",
#                 mime="application/pdf",
#                 use_container_width=True,
#             )

#     st.markdown("<br>", unsafe_allow_html=True)

#     tab1, tab2 = st.tabs(
#         [
#             "📊 CSV Preview",
#             "📑 PDF Preview",
#         ]
#     )

#     with tab1:

#         df = pd.read_csv(
#             SUMMARY_CSV_PATH,
#             skiprows=5,
#         )

#         st.dataframe(
#             df,
#             use_container_width=True,
#             height=450,
#         )

#     with tab2:

#         display_pdf(
#             SUMMARY_PDF_PATH
#         )


# # st.markdown("<div class='footer-bob'>BANK OF BARODA</div>", unsafe_allow_html=True)
# st.markdown(
#     """
#     <div class="footer-bob">
#         <div style="font-size:18px; font-weight:700;">
#             BANK OF BARODA
#         </div>
#         <p style="
#             margin-top:8px;
#             font-size:13px;
#             color:#6b7280;
#             font-weight:500;
#         ">
#             Developed by Mukesh Dewangan
#         </p>
#     </div>
#     """,
#     unsafe_allow_html=True,
# )


















































# # ________________________________________________________________________
# import os
# import shutil
# import zipfile
# import base64
# import pandas as pd
# import streamlit as st
# import streamlit.components.v1 as components


# # ==========================================================
# # INTERNAL EXTRACTION & REPORTING PIPELINES
# # ==========================================================
# from src.extraction.native_text import extract_text_from_pdf
# from src.extraction.image_to_text import extract_text_from_image
# from src.reporting.reporting import (
#     generate_interactive_report,
#     generate_interactive_csv_summary,
# )
# from src.reporting.pdf_reporter import generate_final_pdf_report


# # ==========================================================
# # WORKSPACE CONFIGURATION
# # ==========================================================
# INPUT_DIR = "data/input"
# REPORT_DIR = "data/output"
# SORTED_DIR = "data/sorted"
# SUMMARY_DIR = "data/summary"

# SUMMARY_CSV_PATH = os.path.join(SUMMARY_DIR, "final_interactive_summary.csv")
# SUMMARY_PDF_PATH = os.path.join(SUMMARY_DIR, "Executive_Audit_Report.pdf")

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# BOB_LOGO_PATH = os.path.join(BASE_DIR, "boblogo.jpg")


# # ==========================================================
# # PAGE CONFIGURATION
# # ==========================================================
# st.set_page_config(
#     page_title="BOB IR SCAN",
#     page_icon="🏦",
#     layout="wide",
#     initial_sidebar_state="collapsed",
# )

# for _d in (
#     INPUT_DIR,
#     REPORT_DIR,
#     f"{SORTED_DIR}/flagged",
#     f"{SORTED_DIR}/clean",
#     SUMMARY_DIR,
# ):
#     os.makedirs(_d, exist_ok=True)


# # ==========================================================
# # SESSION STATE INITIALIZATION
# # ==========================================================

# if "uploader_key" not in st.session_state:
#     st.session_state.uploader_key = 0

# if "metrics" not in st.session_state:
#     st.session_state.metrics = {
#         "total": "-",
#         "flagged": "-",
#         "clean": "-",
#         "query": "-",
#     }

# if "analysis_completed" not in st.session_state:
#     st.session_state.analysis_completed = False

# if "reports_ready" not in st.session_state:
#     st.session_state.reports_ready = False


# # ==========================================================
# # ICONS (inline SVG so they render identically everywhere -
# # no dependence on the OS/browser emoji font)
# # ==========================================================

# ICON_FILE = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>'
# ICON_FLAG = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1z"/><line x1="4" y1="22" x2="4" y2="15"/></svg>'
# ICON_CHECK = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>'
# ICON_SEARCH = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>'
# ICON_SHIELD = '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>'
# ICON_UPLOAD = '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>'
# ICON_PLAY = '<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><polygon points="6 3 20 12 6 21 6 3"/></svg>'
# ICON_TRASH = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>'


# # ==========================================================
# # STYLING
# # ==========================================================

# def inject_custom_ui():
#     st.markdown(
#         """
#         <style>

#         :root{
#             --bob-orange:#f36f21;
#             --bob-blue:#102b55;
#             --bg:#f4f7fb;
#             --card:#ffffff;
#             --border:#e6ecf3;
#             --muted:#667085;
#         }

#         .stApp{
#             background:linear-gradient(180deg, #eef2f7 0%, #f8fafc 100%);
#         }

#         .main .block-container{
#             max-width:1500px;
#             padding-top:1.5rem;
#             padding-bottom:2rem;
#         }

#         /* HEADER */
#         .hero-wrap{
#             background:var(--card);
#             border-radius:28px;
#             padding:2.5rem;
#             min-height:220px;
#             border:1px solid var(--border);
#             box-shadow:0 8px 32px rgba(16,43,85,0.05);
#             text-align:center;
#             display:flex;
#             flex-direction:column;
#             justify-content:center;
#         }
#         .hero-title{
#             color:var(--bob-blue);
#             font-size:3.2rem;
#             font-weight:900;
#             line-height:1.05;
#             margin:0;
#         }
#         .hero-sub{
#             margin-top:0.8rem;
#             color:var(--muted);
#             font-size:1.25rem;
#             font-weight:500;
#         }

#         /* LOGO + CLOCK (right column) - single self-contained blocks,
#            no split div/image markup, so no stray empty boxes */
#         .logo-card{
#             background:white;
#             border-radius:24px;
#             padding:1rem;
#             border:1px solid var(--border);
#             box-shadow:0 8px 24px rgba(16,43,85,0.05);
#             text-align:center;
#         }
#         .logo-card img{
#             width:220px;
#             display:block;
#             margin:0 auto;
#         }
#         .clock-card{
#             background:white;
#             border-radius:18px;
#             border:1px solid var(--border);
#             padding:0.7rem 1rem;
#             margin-top:1rem;
#             text-align:center;
#             box-shadow:0 6px 18px rgba(16,43,85,0.04);
#         }

#         /* Kill the default vertical gap Streamlit puts between
#            stacked elements in the header column, so logo + clock
#            sit tightly together like the target design */
#         div[data-testid="column"]:has(.logo-card) div[data-testid="stVerticalBlock"]{
#             gap:0.4rem;
#         }

#         /* KPI CARDS */
#         .metric-card{
#             background:white;
#             border-radius:22px;
#             padding:1.5rem;
#             border:1px solid var(--border);
#             box-shadow:0 6px 18px rgba(16,43,85,0.05);
#             text-align:center;
#             min-height:160px;
#         }
#         .metric-icon{
#             width:44px;
#             height:44px;
#             border-radius:50%;
#             display:flex;
#             align-items:center;
#             justify-content:center;
#             margin:0 auto 0.6rem auto;
#         }
#         .metric-title{
#             color:#475467;
#             font-size:1rem;
#             font-weight:700;
#         }
#         .metric-value{
#             margin-top:0.3rem;
#             color:#102b55;
#             font-size:2.6rem;
#             font-weight:900;
#         }
#         .metric-sub{
#             margin-top:0.2rem;
#             color:#98a2b3;
#             font-size:0.85rem;
#             font-weight:500;
#         }

#         /* SECTION CARDS */
#         .section-title-row{
#             display:flex;
#             align-items:center;
#             gap:0.5rem;
#             margin-bottom:0.2rem;
#         }
#         .section-title-row svg{ color:var(--bob-blue); flex-shrink:0; }
#         .section-title{
#             color:#102b55;
#             font-size:1.4rem;
#             font-weight:900;
#         }
#         .section-sub{
#             color:var(--muted);
#             font-size:0.9rem;
#             margin-bottom:0.8rem;
#         }

#         /* TEXT AREA */
#         .stTextArea textarea, div[data-testid="stTextArea"] textarea, textarea{
#             font-size:20px !important;
#             font-weight:600 !important;
#             color:#102b55 !important;
#             line-height:1.6 !important;
#             border-radius:18px !important;
#             background:#fcfdff !important;
#         }

#         /* FILE UPLOADER - restyled to look like a centered drag & drop card */
#         [data-testid="stFileUploaderDropzone"]{
#             background:#fcfdff !important;
#             border:2px dashed #cfd9e8 !important;
#             border-radius:18px !important;
#             padding:1.4rem !important;
#             justify-content:center !important;
#         }
#         [data-testid="stFileUploaderDropzoneInstructions"]{
#             justify-content:center !important;
#             text-align:center !important;
#         }
#         [data-testid="stFileUploaderDropzone"] > div > svg,
#         [data-testid="stFileUploaderDropzoneInstructions"] svg{
#             color:var(--bob-orange) !important;
#             fill:var(--bob-orange) !important;
#         }
#         /* Only the "Browse files" button (plain text, no icon) gets the
#            orange treatment. The small per-file remove (x) buttons contain
#            only an svg icon and are deliberately excluded via :has(svg),
#            otherwise they get stretched into orange pills. */
#         [data-testid="stFileUploaderDropzone"] button:not(:has(svg)){
#             background:var(--bob-orange) !important;
#             color:white !important;
#             border:none !important;
#             border-radius:12px !important;
#             font-weight:700 !important;
#             padding:0.5rem 1.2rem !important;
#         }
#         [data-testid="stFileUploaderDropzone"] button:not(:has(svg)):hover{
#             background:#d95f16 !important;
#         }
#         [data-testid="stFileUploaderDropzone"] small{
#             color:#98a2b3 !important;
#         }
#         /* Keep the per-file remove buttons small and unstyled */
#         [data-testid="stFileUploaderDropzone"] button:has(svg){
#             background:transparent !important;
#             border:none !important;
#             padding:0.2rem !important;
#             box-shadow:none !important;
#         }

#         /* BUTTONS */
#         .stButton > button{
#             border-radius:14px !important;
#             min-height:2.8rem !important;
#             font-size:1rem !important;
#             font-weight:700 !important;
#             box-shadow:0 4px 12px rgba(0,0,0,0.08);
#             transition:0.25s;
#         }
#         .stButton > button:hover{ transform:translateY(-1px); }

#         /* Run Analysis -> primary, filled orange */
#         div[data-testid="stButton"] button[kind="primary"]{
#             background:linear-gradient(90deg, var(--bob-orange), #ff8c42) !important;
#             color:white !important;
#             border:none !important;
#         }
#         div[data-testid="stButton"] button[kind="primary"]:hover{
#             background:linear-gradient(90deg, #d95f16, var(--bob-orange)) !important;
#         }

#         /* Reset Session -> secondary, outlined orange */
#         div[data-testid="stButton"] button[kind="secondary"]{
#             background:white !important;
#             color:var(--bob-orange) !important;
#             border:2px solid var(--bob-orange) !important;
#         }
#         div[data-testid="stButton"] button[kind="secondary"]:hover{
#             background:#fff5ee !important;
#         }

#         /* DOWNLOAD BUTTONS */
#         .stDownloadButton > button{
#             background:linear-gradient(90deg, #102b55, #183c74) !important;
#             color:white !important;
#             border:none !important;
#             border-radius:14px !important;
#             min-height:2.8rem !important;
#             font-weight:700 !important;
#         }

#         /* SUCCESS CARD */
#         .success-card{
#             background:#eefbf3;
#             border:1px solid #b7e4c7;
#             border-radius:18px;
#             padding:1rem 1.5rem;
#             color:#0f7b35;
#             font-size:1.1rem;
#             font-weight:700;
#             text-align:center;
#             margin-top:1rem;
#             margin-bottom:1rem;
#         }

#         /* TABS */
#         button[data-baseweb="tab"]{
#             font-size:1rem !important;
#             font-weight:700 !important;
#         }

#         /* DATAFRAME */
#         [data-testid="stDataFrame"]{
#             border-radius:18px;
#             overflow:hidden;
#             border:1px solid var(--border);
#         }

#         /* FOOTER */
#         .footer-bob{ margin-top:50px; text-align:center; color:#667085; padding:1rem; }
#         .footer-title{ color:#102b55; font-size:1.1rem; font-weight:800; }
#         .footer-sub{ margin-top:0.4rem; font-size:0.9rem; }

#         </style>
#         """,
#         unsafe_allow_html=True,
#     )


# def render_logo_card():
#     """
#     Renders the logo inside its bordered card as ONE self-contained HTML
#     block (image is base64-embedded directly in the markdown string).
#     This avoids the earlier bug where opening a <div> in one st.markdown
#     call and closing it in another left an empty, separately-styled box
#     floating above the real logo.
#     """
#     if not os.path.exists(BOB_LOGO_PATH):
#         return
#     with open(BOB_LOGO_PATH, "rb") as f:
#         b64_logo = base64.b64encode(f.read()).decode("utf-8")
#     st.markdown(
#         f"""
#         <div class="logo-card">
#             <img src="data:image/jpeg;base64,{b64_logo}" />
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )


# def render_live_clock():
#     components.html(
#         """
#         <div class="clock-card">
#             <div style="color:#102b55; font-size:14px; font-weight:800; margin-bottom:6px;">
#                 Dashboard Time
#             </div>
#             <div id="bob-clock" style="color:#102b55; font-size:16px; font-weight:700;
#                  font-family:system-ui,-apple-system,sans-serif;">
#                 --
#             </div>
#         </div>
#         <script>
#             const el = document.getElementById("bob-clock");
#             function tick(){
#                 const now = new Date();
#                 const opts = {hour:'2-digit', minute:'2-digit', second:'2-digit',
#                                day:'2-digit', month:'short', year:'numeric'};
#                 el.innerText = now.toLocaleString(undefined, opts);
#             }
#             tick();
#             setInterval(tick, 1000);
#         </script>
#         """,
#         height=80,
#     )


# # ==========================================================
# # WORKSPACE HELPERS
# # ==========================================================

# def clear_run_outputs():
#     """
#     Called ONLY right before a new 'Run Analysis' pass.
#     Clears the previous run's generated reports / sorted folders so the
#     new batch doesn't mix with old results. Never touches the raw files
#     already saved in data/input.
#     """
#     for path in (REPORT_DIR, SUMMARY_DIR, f"{SORTED_DIR}/flagged", f"{SORTED_DIR}/clean"):
#         if os.path.exists(path):
#             shutil.rmtree(path)
#         os.makedirs(path, exist_ok=True)


# def handle_uploaded_files(uploaded_files):
#     """Saves uploaded files to disk and returns the PDF paths to process."""
#     target_pdf_paths = []
#     for uploaded_file in uploaded_files:
#         file_path = os.path.join(INPUT_DIR, uploaded_file.name)
#         with open(file_path, "wb") as f:
#             f.write(uploaded_file.getbuffer())

#         if uploaded_file.name.lower().endswith(".zip"):
#             with zipfile.ZipFile(file_path, "r") as zip_ref:
#                 pdf_members = [
#                     member for member in zip_ref.namelist()
#                     if member.lower().endswith(".pdf") and not member.endswith("/")
#                 ]
#                 zip_ref.extractall(INPUT_DIR)
#                 for member in pdf_members:
#                     extracted_pdf = os.path.normpath(os.path.join(INPUT_DIR, member))
#                     if os.path.exists(extracted_pdf):
#                         target_pdf_paths.append(extracted_pdf)
#             os.remove(file_path)
#         elif uploaded_file.name.lower().endswith(".pdf"):
#             target_pdf_paths.append(file_path)
#     return target_pdf_paths


# def display_pdf(file_path):
#     with open(file_path, "rb") as f:
#         base64_pdf = base64.b64encode(f.read()).decode("utf-8")
#     pdf_display = (
#         f'<iframe src="data:application/pdf;base64,{base64_pdf}" '
#         f'width="100%" height="800px" type="application/pdf"></iframe>'
#     )
#     st.markdown(pdf_display, unsafe_allow_html=True)


# # ==========================================================
# # STREAMLIT DASHBOARD UI
# # ==========================================================

# inject_custom_ui()

# # ------------------------------------------------
# # HEADER
# # ------------------------------------------------
# header_left, header_right = st.columns([0.78, 0.22])

# with header_left:
#     st.markdown(
#         """
#         <div class="hero-wrap">
#             <h1 class="hero-title">BOB IR SCAN</h1>
#             <p class="hero-sub">AI-Powered Compliance &amp; Fraud Intelligence Platform</p>
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )

# with header_right:
#     render_logo_card()
#     render_live_clock()

# st.markdown("<br>", unsafe_allow_html=True)

# # ------------------------------------------------
# # KPI DASHBOARD
# # ------------------------------------------------
# k1, k2, k3, k4 = st.columns(4)

# cards = [
#     (ICON_FILE, "#e7f0ff", "#2f6fed", "Total Scanned", st.session_state.metrics["total"], "Documents processed"),
#     (ICON_FLAG, "#fdeee3", "#f36f21", "Flagged Documents", st.session_state.metrics["flagged"], "Potential risk detected"),
#     (ICON_CHECK, "#e6f8ee", "#12b76a", "Clean Documents", st.session_state.metrics["clean"], "No risk detected"),
#     (ICON_SEARCH, "#f3ecfd", "#7f56d9", "Query Matches (YES)", st.session_state.metrics["query"], "Direct matches found"),
# ]

# for col, (icon, bg, fg, title, value, sub) in zip([k1, k2, k3, k4], cards):
#     with col:
#         st.markdown(
#             f"""
#             <div class="metric-card">
#                 <div class="metric-icon" style="background:{bg}; color:{fg};">{icon}</div>
#                 <div class="metric-title">{title}</div>
#                 <div class="metric-value">{value}</div>
#                 <div class="metric-sub">{sub}</div>
#             </div>
#             """,
#             unsafe_allow_html=True,
#         )

# # ------------------------------------------------
# # INPUT SECTION
# # ------------------------------------------------
# st.markdown("<br>", unsafe_allow_html=True)

# left, right = st.columns([1, 1], gap="large")

# with left:
#     with st.container(border=True):
#         st.markdown(
#             f"""
#             <div class="section-title-row">{ICON_SHIELD}<span class="section-title">Risk Query</span></div>
#             <div class="section-sub">Ask a focused question to get a clear risk intelligence.</div>
#             """,
#             unsafe_allow_html=True,
#         )
#         user_prompt = st.text_area(
#             "",
#             value="Whether the account is identified as fraud?",
#             height=110,
#             label_visibility="collapsed",
#         )

# with right:
#     with st.container(border=True):
#         st.markdown(
#             f"""
#             <div class="section-title-row">{ICON_UPLOAD}<span class="section-title">Upload Documents</span></div>
#             <div class="section-sub">Upload PDF or ZIP bundles for instant screening.</div>
#             """,
#             unsafe_allow_html=True,
#         )
#         uploaded_files = st.file_uploader(
#             "",
#             type=["pdf", "zip"],
#             accept_multiple_files=True,
#             key=f"uploader_{st.session_state.uploader_key}",
#             label_visibility="collapsed",
#         )
#         st.caption("Supported formats: PDF, ZIP  •  Max file size: 500MB")

#         if uploaded_files:
#             pdf_count = sum(1 for f in uploaded_files if f.name.lower().endswith(".pdf"))
#             zip_count = sum(1 for f in uploaded_files if f.name.lower().endswith(".zip"))
#             st.info(f"Selected Files: {len(uploaded_files)} | PDF: {pdf_count} | ZIP: {zip_count}")

# # ------------------------------------------------
# # ACTION BUTTONS
# # ------------------------------------------------
# st.markdown("<br>", unsafe_allow_html=True)

# space1, b1, b2, space2 = st.columns([1.3, 1, 1, 1.3])

# with b1:
#     # st.button() renders its label as plain text, not HTML - inline SVG
#     # would print as a raw string, so a plain unicode glyph is used here.
#     run_btn = st.button("▶ Run Analysis", use_container_width=True, type="primary")

# with b2:
#     clear_btn = st.button("🗑 Reset Session", use_container_width=True, type="secondary")

# # ------------------------------------------------
# # RESET SESSION — dashboard only, NOTHING is deleted from disk
# # ------------------------------------------------
# if clear_btn:
#     st.session_state.uploader_key += 1
#     st.session_state.metrics = {
#         "total": "-",
#         "flagged": "-",
#         "clean": "-",
#         "query": "-",
#     }
#     st.session_state.analysis_completed = False
#     st.session_state.reports_ready = False
#     st.rerun()

# # ------------------------------------------------
# # MAIN EXECUTION
# # ------------------------------------------------
# if run_btn:

#     if not uploaded_files:
#         st.warning("Please upload at least one PDF or ZIP file to begin analysis.")

#     else:
#         clear_run_outputs()

#         target_pdf_paths = handle_uploaded_files(uploaded_files)

#         if not target_pdf_paths:
#             st.error("No valid PDF files were detected in the uploaded batch.")

#         else:
#             all_processed_reports = []
#             progress_bar = st.progress(0)
#             status_text = st.empty()

#             for i, file_path in enumerate(target_pdf_paths):
#                 filename = os.path.basename(file_path)
#                 status_text.markdown(f"**Processing Document {i+1}/{len(target_pdf_paths)}**  \n`{filename}`")

#                 extracted_text = extract_text_from_pdf(file_path)
#                 if not extracted_text:
#                     extracted_text = extract_text_from_image(file_path)
#                 if not extracted_text:
#                     continue

#                 report = generate_interactive_report(extracted_text, filename, user_prompt, REPORT_DIR)
#                 all_processed_reports.append(report)

#                 is_flagged = len(report["primary_keywords"]) > 0 or report["fraud_answer"] == "YES"
#                 target_folder = "flagged" if is_flagged else "clean"
#                 shutil.copy(file_path, os.path.join(SORTED_DIR, target_folder, filename))

#                 progress_bar.progress((i + 1) / len(target_pdf_paths))

#             status_text.text("Building final reports...")

#             if all_processed_reports:
#                 generate_interactive_csv_summary(all_processed_reports, SUMMARY_CSV_PATH)
#                 generate_final_pdf_report(REPORT_DIR, SUMMARY_PDF_PATH)

#                 total_docs = len(all_processed_reports)
#                 total_flagged = sum(
#                     1 for r in all_processed_reports
#                     if len(r["primary_keywords"]) > 0 or r["fraud_answer"] == "YES"
#                 )
#                 total_clean = total_docs - total_flagged
#                 total_query_matches = sum(1 for r in all_processed_reports if r.get("query_answer") == "YES")

#                 st.session_state.metrics = {
#                     "total": total_docs,
#                     "flagged": total_flagged,
#                     "clean": total_clean,
#                     "query": total_query_matches,
#                 }
#                 st.session_state.analysis_completed = True
#                 st.session_state.reports_ready = True

#                 progress_bar.empty()
#                 status_text.empty()
#                 st.rerun()

#             else:
#                 progress_bar.empty()
#                 status_text.empty()
#                 st.error("No valid text could be extracted from the uploaded documents.")

# # ------------------------------------------------
# # SUCCESS MESSAGE
# # ------------------------------------------------
# if st.session_state.analysis_completed:
#     st.markdown(
#         """
#         <div class="success-card">
#             ✓ Audit completed successfully. Reports are ready for review and download.
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )

# # ------------------------------------------------
# # REPORT PREVIEWS — each download button sits at the
# # top of its own tab, so placement is always consistent.
# # ------------------------------------------------
# if st.session_state.reports_ready:

#     st.markdown("<br>", unsafe_allow_html=True)
#     st.markdown('<div class="section-title">Reports &amp; Deliverables</div>', unsafe_allow_html=True)

#     tab1, tab2 = st.tabs(["📊 Live CSV Data", "📑 Executive PDF Report"])

#     with tab1:
#         with open(SUMMARY_CSV_PATH, "rb") as csv_file:
#             st.download_button(
#                 "📥 Download CSV Report",
#                 data=csv_file,
#                 file_name="Audit_Summary.csv",
#                 mime="text/csv",
#                 use_container_width=True,
#             )
#         df = pd.read_csv(SUMMARY_CSV_PATH, skiprows=5)
#         st.dataframe(df, use_container_width=True, height=450)

#     with tab2:
#         with open(SUMMARY_PDF_PATH, "rb") as pdf_file:
#             st.download_button(
#                 "📥 Download PDF Report",
#                 data=pdf_file,
#                 file_name="Executive_Audit_Report.pdf",
#                 mime="application/pdf",
#                 use_container_width=True,
#             )
#         display_pdf(SUMMARY_PDF_PATH)


# # ------------------------------------------------
# # FOOTER
# # ------------------------------------------------
# st.markdown(
#     """
#     <div class="footer-bob">
#         <div class="footer-title">BANK OF BARODA</div>
#         <p class="footer-sub">Developed by Mukesh Dewangan</p>
#     </div>
#     """,
#     unsafe_allow_html=True,
# )






import os
import shutil
import zipfile
import base64
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components


# ==========================================================
# INTERNAL EXTRACTION & REPORTING PIPELINES
# ==========================================================
from src.extraction.native_text import extract_text_from_pdf
from src.extraction.image_to_text import extract_text_from_image
from src.reporting.reporting import (
    generate_interactive_report,
    generate_interactive_csv_summary,
)
from src.reporting.pdf_reporter import generate_final_pdf_report


# ==========================================================
# WORKSPACE CONFIGURATION
# ==========================================================
INPUT_DIR = "data/input"
REPORT_DIR = "data/output"
SORTED_DIR = "data/sorted"
SUMMARY_DIR = "data/summary"

SUMMARY_CSV_PATH = os.path.join(SUMMARY_DIR, "final_interactive_summary.csv")
SUMMARY_PDF_PATH = os.path.join(SUMMARY_DIR, "Executive_Audit_Report.pdf")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BOB_LOGO_PATH = os.path.join(BASE_DIR, "boblogo.jpg")


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================
st.set_page_config(
    page_title="BOB SCANNER",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

for _d in (
    INPUT_DIR,
    REPORT_DIR,
    f"{SORTED_DIR}/flagged",
    f"{SORTED_DIR}/clean",
    SUMMARY_DIR,
):
    os.makedirs(_d, exist_ok=True)


# ==========================================================
# SESSION STATE INITIALIZATION
# ==========================================================

if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0

if "metrics" not in st.session_state:
    st.session_state.metrics = {
        "total": "-",
        "flagged": "-",
        "clean": "-",
        "query": "-",
    }

if "analysis_completed" not in st.session_state:
    st.session_state.analysis_completed = False

if "reports_ready" not in st.session_state:
    st.session_state.reports_ready = False


# ==========================================================
# ICONS (inline SVG so they render identically everywhere -
# no dependence on the OS/browser emoji font)
# ==========================================================

ICON_FILE = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>'
ICON_FLAG = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1z"/><line x1="4" y1="22" x2="4" y2="15"/></svg>'
ICON_CHECK = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>'
ICON_SEARCH = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>'
ICON_SHIELD = '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>'
ICON_UPLOAD = '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>'
ICON_PLAY = '<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><polygon points="6 3 20 12 6 21 6 3"/></svg>'
ICON_TRASH = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>'


# ==========================================================
# STYLING
# ==========================================================

def inject_custom_ui():
    st.markdown(
        """
        <style>

        :root{
            --bob-orange:#f36f21;
            --bob-blue:#102b55;
            --bg:#f4f7fb;
            --card:#ffffff;
            --border:#e6ecf3;
            --muted:#667085;
        }

        .stApp{
            background:linear-gradient(180deg, #eef2f7 0%, #f8fafc 100%);
        }

        .main .block-container{
            max-width:1500px;
            padding-top:1.5rem;
            padding-bottom:2rem;
        }

        /* HEADER */
        .hero-wrap{
            position:relative;
            overflow:hidden;
            background:var(--card);
            border-radius:28px;
            padding:2.5rem;
            min-height:220px;
            border:1px solid var(--border);
            box-shadow:0 8px 32px rgba(16,43,85,0.05);
            text-align:center;
            display:flex;
            flex-direction:column;
            justify-content:center;
        }
        .hero-wrap-content{
            position:relative;
            z-index:1;
        }
        .hero-wave{
            position:absolute;
            top:0;
            left:0;
            width:60%;
            height:100%;
            z-index:0;
            pointer-events:none;
        }
        .hero-title{
            color:var(--bob-blue);
            font-size:3.2rem;
            font-weight:900;
            line-height:1.05;
            margin:0;
        }
        .hero-sub{
            margin-top:0.8rem;
            color:var(--muted);
            font-size:1.25rem;
            font-weight:500;
        }

        /* LOGO + CLOCK (right column) - single self-contained blocks,
           no split div/image markup, so no stray empty boxes */
        .logo-card{
            background:white;
            border-radius:24px;
            padding:1rem;
            border:1px solid var(--border);
            box-shadow:0 8px 24px rgba(16,43,85,0.05);
            text-align:center;
        }
        .logo-card img{
            width:220px;
            display:block;
            margin:0 auto;
        }
        .clock-card{
            background:white;
            border-radius:18px;
            border:1px solid var(--border);
            padding:0.7rem 1rem;
            margin-top:1rem;
            text-align:center;
            box-shadow:0 6px 18px rgba(16,43,85,0.04);
        }

        /* Kill the default vertical gap Streamlit puts between
           stacked elements in the header column, so logo + clock
           sit tightly together like the target design */
        div[data-testid="column"]:has(.logo-card) div[data-testid="stVerticalBlock"]{
            gap:0.4rem;
        }

        /* KPI CARDS */
        .metric-card{
            background:white;
            border-radius:22px;
            padding:1.5rem;
            border:1px solid var(--border);
            box-shadow:0 6px 18px rgba(16,43,85,0.05);
            text-align:center;
            min-height:160px;
        }
        .metric-icon{
            width:44px;
            height:44px;
            border-radius:50%;
            display:flex;
            align-items:center;
            justify-content:center;
            margin:0 auto 0.6rem auto;
        }
        .metric-title{
            color:#475467;
            font-size:1rem;
            font-weight:700;
        }
        .metric-value{
            margin-top:0.3rem;
            color:#102b55;
            font-size:2.6rem;
            font-weight:900;
        }
        .metric-sub{
            margin-top:0.2rem;
            color:#98a2b3;
            font-size:0.85rem;
            font-weight:500;
        }

        /* SECTION CARDS */
        .section-title-row{
            display:flex;
            align-items:center;
            gap:0.5rem;
            margin-bottom:0.2rem;
        }
        .section-title-row svg{ color:var(--bob-blue); flex-shrink:0; }
        .section-title{
            color:#102b55;
            font-size:1.4rem;
            font-weight:900;
        }
        .section-sub{
            color:var(--muted);
            font-size:0.9rem;
            margin-bottom:0.8rem;
        }

        /* TEXT AREA */
        .stTextArea textarea, div[data-testid="stTextArea"] textarea, textarea{
            font-size:20px !important;
            font-weight:600 !important;
            color:#102b55 !important;
            line-height:1.6 !important;
            border-radius:18px !important;
            background:#fcfdff !important;
        }

        /* FILE UPLOADER - restyled to look like a centered drag & drop card */
        [data-testid="stFileUploaderDropzone"]{
            background:#fcfdff !important;
            border:2px dashed #cfd9e8 !important;
            border-radius:18px !important;
            padding:1.4rem !important;
            display:flex !important;
            align-items:center !important;
            justify-content:center !important;
        }
        [data-testid="stFileUploaderDropzoneInstructions"]{
            justify-content:center !important;
            text-align:center !important;
            flex-grow:0 !important;
        }
        /* Streamlit's own "200MB per file..." caption is hidden - we show
           our own "Supported formats / Max file size" caption underneath
           the dropzone instead, so there's only one size note, not two. */
        [data-testid="stFileUploaderDropzone"] small{
            display:none !important;
        }
        [data-testid="stFileUploaderDropzone"] > div > svg,
        [data-testid="stFileUploaderDropzoneInstructions"] svg{
            color:var(--bob-orange) !important;
            fill:var(--bob-orange) !important;
        }
        /* Only the "Browse files" button (plain text, no icon) gets the
           orange treatment. The small per-file remove (x) buttons contain
           only an svg icon and are deliberately excluded via :has(svg),
           otherwise they get stretched into orange pills. */
        [data-testid="stFileUploaderDropzone"] button:not(:has(svg)){
            background:var(--bob-orange) !important;
            color:white !important;
            border:none !important;
            border-radius:12px !important;
            font-weight:700 !important;
            padding:0.5rem 1.2rem !important;
        }
        [data-testid="stFileUploaderDropzone"] button:not(:has(svg)):hover{
            background:#d95f16 !important;
        }
        [data-testid="stFileUploaderDropzone"] small{
            color:#98a2b3 !important;
        }
        /* Keep the per-file remove buttons small and unstyled */
        [data-testid="stFileUploaderDropzone"] button:has(svg){
            background:transparent !important;
            border:none !important;
            padding:0.2rem !important;
            box-shadow:none !important;
        }

        /* BUTTONS */
        .stButton > button{
            border-radius:14px !important;
            min-height:2.8rem !important;
            font-size:1rem !important;
            font-weight:700 !important;
            box-shadow:0 4px 12px rgba(0,0,0,0.08);
            transition:0.25s;
        }
        .stButton > button:hover{ transform:translateY(-1px); }

        /* Run Analysis -> primary, filled orange */
        div[data-testid="stButton"] button[kind="primary"]{
            background:linear-gradient(90deg, var(--bob-orange), #ff8c42) !important;
            color:white !important;
            border:none !important;
        }
        div[data-testid="stButton"] button[kind="primary"]:hover{
            background:linear-gradient(90deg, #d95f16, var(--bob-orange)) !important;
        }

        /* Reset Session -> secondary, outlined orange */
        div[data-testid="stButton"] button[kind="secondary"]{
            background:white !important;
            color:var(--bob-orange) !important;
            border:2px solid var(--bob-orange) !important;
        }
        div[data-testid="stButton"] button[kind="secondary"]:hover{
            background:#fff5ee !important;
        }

        /* DOWNLOAD BUTTONS */
        .stDownloadButton > button{
            background:linear-gradient(90deg, #102b55, #183c74) !important;
            color:white !important;
            border:none !important;
            border-radius:14px !important;
            min-height:2.8rem !important;
            font-weight:700 !important;
        }

        /* SUCCESS CARD */
        .success-card{
            background:#eefbf3;
            border:1px solid #b7e4c7;
            border-radius:18px;
            padding:1rem 1.5rem;
            color:#0f7b35;
            font-size:1.1rem;
            font-weight:700;
            text-align:center;
            margin-top:1rem;
            margin-bottom:1rem;
        }

        /* TABS */
        button[data-baseweb="tab"]{
            font-size:1rem !important;
            font-weight:700 !important;
        }

        /* DATAFRAME */
        [data-testid="stDataFrame"]{
            border-radius:18px;
            overflow:hidden;
            border:1px solid var(--border);
        }

        /* FOOTER */
        .footer-bob{ margin-top:50px; text-align:center; color:#667085; padding:1rem; }
        .footer-title{ color:#102b55; font-size:1.1rem; font-weight:800; }
        .footer-sub{ margin-top:0.4rem; font-size:0.9rem; }

        </style>
        """,
        unsafe_allow_html=True,
    )


def render_logo_card():
    """
    Renders the logo inside its bordered card as ONE self-contained HTML
    block (image is base64-embedded directly in the markdown string).
    This avoids the earlier bug where opening a <div> in one st.markdown
    call and closing it in another left an empty, separately-styled box
    floating above the real logo.
    """
    if not os.path.exists(BOB_LOGO_PATH):
        return
    with open(BOB_LOGO_PATH, "rb") as f:
        b64_logo = base64.b64encode(f.read()).decode("utf-8")
    st.markdown(
        f"""
        <div class="logo-card">
            <img src="data:image/jpeg;base64,{b64_logo}" />
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_live_clock():
    components.html(
        """
        <div class="clock-card">
            <div style="color:#102b55; font-size:14px; font-weight:800; margin-bottom:6px;">
                Dashboard Time
            </div>
            <div id="bob-clock" style="color:#102b55; font-size:16px; font-weight:700;
                 font-family:system-ui,-apple-system,sans-serif;">
                --
            </div>
        </div>
        <script>
            const el = document.getElementById("bob-clock");
            function tick(){
                const now = new Date();
                const opts = {hour:'2-digit', minute:'2-digit', second:'2-digit',
                               day:'2-digit', month:'short', year:'numeric'};
                el.innerText = now.toLocaleString(undefined, opts);
            }
            tick();
            setInterval(tick, 1000);
        </script>
        """,
        height=80,
    )


# ==========================================================
# WORKSPACE HELPERS
# ==========================================================

def clear_run_outputs():
    """
    Called ONLY right before a new 'Run Analysis' pass.
    Clears the previous run's generated reports / sorted folders so the
    new batch doesn't mix with old results. Never touches the raw files
    already saved in data/input.
    """
    for path in (REPORT_DIR, SUMMARY_DIR, f"{SORTED_DIR}/flagged", f"{SORTED_DIR}/clean"):
        if os.path.exists(path):
            shutil.rmtree(path)
        os.makedirs(path, exist_ok=True)


def handle_uploaded_files(uploaded_files):
    """Saves uploaded files to disk and returns the PDF paths to process."""
    target_pdf_paths = []
    for uploaded_file in uploaded_files:
        file_path = os.path.join(INPUT_DIR, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        if uploaded_file.name.lower().endswith(".zip"):
            with zipfile.ZipFile(file_path, "r") as zip_ref:
                pdf_members = [
                    member for member in zip_ref.namelist()
                    if member.lower().endswith(".pdf") and not member.endswith("/")
                ]
                zip_ref.extractall(INPUT_DIR)
                for member in pdf_members:
                    extracted_pdf = os.path.normpath(os.path.join(INPUT_DIR, member))
                    if os.path.exists(extracted_pdf):
                        target_pdf_paths.append(extracted_pdf)
            os.remove(file_path)
        elif uploaded_file.name.lower().endswith(".pdf"):
            target_pdf_paths.append(file_path)
    return target_pdf_paths


def display_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode("utf-8")
    pdf_display = (
        f'<iframe src="data:application/pdf;base64,{base64_pdf}" '
        f'width="100%" height="800px" type="application/pdf"></iframe>'
    )
    st.markdown(pdf_display, unsafe_allow_html=True)


# ==========================================================
# STREAMLIT DASHBOARD UI
# ==========================================================

inject_custom_ui()

# ------------------------------------------------
# HEADER
# ------------------------------------------------
header_left, header_right = st.columns([0.78, 0.22])

with header_left:
    st.markdown(
        """
        <div class="hero-wrap">
            <svg class="hero-wave" viewBox="0 0 500 300" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M-20,220 C60,180 100,260 180,210 C260,160 300,240 380,190 C440,155 470,190 520,160"
                      fill="none" stroke="#f36f21" stroke-width="2" opacity="0.18"/>
                <path d="M-20,180 C60,140 100,220 180,170 C260,120 300,200 380,150 C440,115 470,150 520,120"
                      fill="none" stroke="#f36f21" stroke-width="2" opacity="0.14"/>
                <path d="M-20,140 C60,100 100,180 180,130 C260,80 300,160 380,110 C440,75 470,110 520,80"
                      fill="none" stroke="#f36f21" stroke-width="2" opacity="0.10"/>
                <path d="M-20,260 C60,220 100,300 180,250 C260,200 300,280 380,230 C440,195 470,230 520,200"
                      fill="none" stroke="#102b55" stroke-width="1.5" opacity="0.06"/>
            </svg>
            <div class="hero-wrap-content">
                <h1 class="hero-title">BOB SCANNER</h1>
                <p class="hero-sub">AI-Powered Compliance &amp; Fraud Intelligence Platform</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with header_right:
    render_logo_card()
    render_live_clock()

st.markdown("<br>", unsafe_allow_html=True)

# ------------------------------------------------
# KPI DASHBOARD
# ------------------------------------------------
k1, k2, k3, k4 = st.columns(4)

cards = [
    (ICON_FILE, "#e7f0ff", "#2f6fed", "Total Scanned", st.session_state.metrics["total"], "Documents processed"),
    (ICON_FLAG, "#fdeee3", "#f36f21", "Flagged Documents", st.session_state.metrics["flagged"], "Potential risk detected"),
    (ICON_CHECK, "#e6f8ee", "#12b76a", "Clean Documents", st.session_state.metrics["clean"], "No risk detected"),
    (ICON_SEARCH, "#f3ecfd", "#7f56d9", "Query Matches (YES)", st.session_state.metrics["query"], "Direct matches found"),
]

for col, (icon, bg, fg, title, value, sub) in zip([k1, k2, k3, k4], cards):
    with col:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-icon" style="background:{bg}; color:{fg};">{icon}</div>
                <div class="metric-title">{title}</div>
                <div class="metric-value">{value}</div>
                <div class="metric-sub">{sub}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ------------------------------------------------
# INPUT SECTION
# ------------------------------------------------
st.markdown("<br>", unsafe_allow_html=True)

left, right = st.columns([1, 1], gap="large")

with left:
    with st.container(border=True):
        st.markdown(
            f"""
            <div class="section-title-row">{ICON_SHIELD}<span class="section-title">Risk Query</span></div>
            <div class="section-sub">Ask a focused question to get a clear risk intelligence.</div>
            """,
            unsafe_allow_html=True,
        )
        user_prompt = st.text_area(
            "",
            value="Whether the account is identified as fraud?",
            height=110,
            label_visibility="collapsed",
        )

with right:
    with st.container(border=True):
        st.markdown(
            f"""
            <div class="section-title-row">{ICON_UPLOAD}<span class="section-title">Upload Documents</span></div>
            <div class="section-sub">Upload PDF or ZIP bundles for instant screening.</div>
            """,
            unsafe_allow_html=True,
        )
        uploaded_files = st.file_uploader(
            "",
            type=["pdf", "zip"],
            accept_multiple_files=True,
            key=f"uploader_{st.session_state.uploader_key}",
            label_visibility="collapsed",
        )
        st.caption("Supported formats: PDF, ZIP  •  Max file size: 500MB")

        if uploaded_files:
            pdf_count = sum(1 for f in uploaded_files if f.name.lower().endswith(".pdf"))
            zip_count = sum(1 for f in uploaded_files if f.name.lower().endswith(".zip"))
            st.info(f"Selected Files: {len(uploaded_files)} | PDF: {pdf_count} | ZIP: {zip_count}")

# ------------------------------------------------
# ACTION BUTTONS
# ------------------------------------------------
st.markdown("<br>", unsafe_allow_html=True)

space1, b1, b2, space2 = st.columns([1.3, 1, 1, 1.3])

with b1:
    # st.button() renders its label as plain text, not HTML - inline SVG
    # would print as a raw string, so a plain unicode glyph is used here.
    run_btn = st.button("▶ Run Analysis", use_container_width=True, type="primary")

with b2:
    clear_btn = st.button("🗑 Reset Session", use_container_width=True, type="secondary")

# ------------------------------------------------
# RESET SESSION — dashboard only, NOTHING is deleted from disk
# ------------------------------------------------
if clear_btn:
    st.session_state.uploader_key += 1
    st.session_state.metrics = {
        "total": "-",
        "flagged": "-",
        "clean": "-",
        "query": "-",
    }
    st.session_state.analysis_completed = False
    st.session_state.reports_ready = False
    st.rerun()

# ------------------------------------------------
# MAIN EXECUTION
# ------------------------------------------------
if run_btn:

    if not uploaded_files:
        st.warning("Please upload at least one PDF or ZIP file to begin analysis.")

    else:
        clear_run_outputs()

        target_pdf_paths = handle_uploaded_files(uploaded_files)

        if not target_pdf_paths:
            st.error("No valid PDF files were detected in the uploaded batch.")

        else:
            all_processed_reports = []
            progress_bar = st.progress(0)
            status_text = st.empty()

            for i, file_path in enumerate(target_pdf_paths):
                filename = os.path.basename(file_path)
                status_text.markdown(f"**Processing Document {i+1}/{len(target_pdf_paths)}**  \n`{filename}`")

                extracted_text = extract_text_from_pdf(file_path)
                if not extracted_text:
                    extracted_text = extract_text_from_image(file_path)
                if not extracted_text:
                    continue

                report = generate_interactive_report(extracted_text, filename, user_prompt, REPORT_DIR)
                all_processed_reports.append(report)

                is_flagged = len(report["primary_keywords"]) > 0 or report["fraud_answer"] == "YES"
                target_folder = "flagged" if is_flagged else "clean"
                shutil.copy(file_path, os.path.join(SORTED_DIR, target_folder, filename))

                progress_bar.progress((i + 1) / len(target_pdf_paths))

            status_text.text("Building final reports...")

            if all_processed_reports:
                generate_interactive_csv_summary(all_processed_reports, SUMMARY_CSV_PATH)
                generate_final_pdf_report(REPORT_DIR, SUMMARY_PDF_PATH)

                total_docs = len(all_processed_reports)
                total_flagged = sum(
                    1 for r in all_processed_reports
                    if len(r["primary_keywords"]) > 0 or r["fraud_answer"] == "YES"
                )
                total_clean = total_docs - total_flagged
                total_query_matches = sum(1 for r in all_processed_reports if r.get("query_answer") == "YES")

                st.session_state.metrics = {
                    "total": total_docs,
                    "flagged": total_flagged,
                    "clean": total_clean,
                    "query": total_query_matches,
                }
                st.session_state.analysis_completed = True
                st.session_state.reports_ready = True

                progress_bar.empty()
                status_text.empty()
                st.rerun()

            else:
                progress_bar.empty()
                status_text.empty()
                st.error("No valid text could be extracted from the uploaded documents.")

# ------------------------------------------------
# SUCCESS MESSAGE
# ------------------------------------------------
if st.session_state.analysis_completed:
    st.markdown(
        """
        <div class="success-card">
            ✓ Audit completed successfully. Reports are ready for review and download.
        </div>
        """,
        unsafe_allow_html=True,
    )

# ------------------------------------------------
# REPORT PREVIEWS — each download button sits at the
# top of its own tab, so placement is always consistent.
# ------------------------------------------------
if st.session_state.reports_ready:

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">Reports &amp; Deliverables</div>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📊 Live CSV Data", "📑 Executive PDF Report"])

    with tab1:
        with open(SUMMARY_CSV_PATH, "rb") as csv_file:
            st.download_button(
                "📥 Download CSV Report",
                data=csv_file,
                file_name="Audit_Summary.csv",
                mime="text/csv",
                use_container_width=True,
            )
        df = pd.read_csv(SUMMARY_CSV_PATH, skiprows=5)
        st.dataframe(df, use_container_width=True, height=450)

    with tab2:
        with open(SUMMARY_PDF_PATH, "rb") as pdf_file:
            st.download_button(
                "📥 Download PDF Report",
                data=pdf_file,
                file_name="Executive_Audit_Report.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
        display_pdf(SUMMARY_PDF_PATH)


# ------------------------------------------------
# FOOTER
# ------------------------------------------------
st.markdown(
    """
    <div class="footer-bob">
        <div class="footer-title">BANK OF BARODA</div>
        <p class="footer-sub">Developed by Mukesh Dewangan</p>
    </div>
    """,
    unsafe_allow_html=True,
)