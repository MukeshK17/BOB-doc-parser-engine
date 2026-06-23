import os
import shutil
from src.extraction.native_text import extract_text_from_pdf
from src.extraction.image_to_text import extract_text_from_image
from src.reporting.reporting import generate_interactive_report, generate_interactive_csv_summary
from src.reporting.pdf_reporter import generate_final_pdf_report

INPUT_DIR = "data/input"
REPORT_DIR = "data/output"
SORTED_DIR = "data/sorted"
SUMMARY_DIR = "data/summary"

SUMMARY_CSV_PATH = os.path.join(SUMMARY_DIR, "final_interactive_summary.csv")
SUMMARY_PDF_PATH = os.path.join(SUMMARY_DIR, "Executive_Audit_Report.pdf")

def main():
    print("=====================================================")
    print("      DOC-PARSER INTERACTIVE QUERY ENGINE            ")
    print("=====================================================")
    
    user_prompt = input("Enter your custom text query constraint: \n> ")
    if not user_prompt.strip():
        user_prompt = "Whether the account is identified as fraud?"
        print(f"[INFO] Empty input. Standard default fallback triggered.")

    # Reset directory outputs cleanly to block cross-run data poisoning
    for path in [REPORT_DIR, SUMMARY_DIR, f"{SORTED_DIR}/flagged", f"{SORTED_DIR}/clean"]:
        if os.path.exists(path):
            shutil.rmtree(path)
        os.makedirs(path, exist_ok=True)

    all_processed_reports = []
    
    for filename in os.listdir(INPUT_DIR):
        file_path = os.path.join(INPUT_DIR, filename)
        extracted_text = ""

        # Step 1: Attempt native high-fidelity text extraction via PyMuPDF
        if filename.lower().endswith(".pdf"):
            extracted_text = extract_text_from_pdf(file_path)

        # Step 2: FALLBACK TRIGGER - Image or flattened scan handling via PaddleOCR
        if not extracted_text or not filename.lower().endswith(".pdf"):
            print(f"[INFO] Path A yielded no text for {filename}. Triggering PaddleOCR Fallback.")
            extracted_text = extract_text_from_image(file_path)

        if not extracted_text:
            print(f"[WARNING] No text could be extracted from {filename}. Skipping.")
            continue

        # Step 3: Run the interactive reporting engine (Dual-Stream Isolation)
        report = generate_interactive_report(extracted_text, filename, user_prompt, REPORT_DIR)
        all_processed_reports.append(report)

        # Step 4: Sorting Matrix Alignment
        is_flagged = len(report["primary_keywords"]) > 0 or report["fraud_answer"] == "YES"
        target_folder = "flagged" if is_flagged else "clean"
        shutil.copy(file_path, os.path.join(SORTED_DIR, target_folder, filename))
        
        print(f"[SUCCESS] Processed: {filename} ({target_folder.upper()}) | Query Ans: {report['query_answer']}")

    if all_processed_reports:
        # Step 5: Deliverables Matrix Buildout
        generate_interactive_csv_summary(all_processed_reports, SUMMARY_CSV_PATH)
        generate_final_pdf_report(REPORT_DIR, SUMMARY_PDF_PATH)
        print(f"\n[DONE] Audit Summary Spreadsheet saved to: {SUMMARY_CSV_PATH}")
        print(f"[DONE] Executive Report Canvas saved to:     {SUMMARY_PDF_PATH}")

if __name__ == "__main__":
    main()
