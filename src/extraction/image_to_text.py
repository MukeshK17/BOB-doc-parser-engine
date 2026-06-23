from paddleocr import PaddleOCR
import logging
import fitz  # PyMuPDF
import os

# Initialize the model once globally
ocr_engine = PaddleOCR(use_angle_cls=True, lang='en')

def extract_text_from_image(image_path):
    """
    Path B: Uses PaddleOCR to extract text from flat scans and handwriting.
    """
    logging.info(f"Running PaddleOCR on: {image_path}")
    
    try:
        # If it's a scanned PDF, convert pages to temporary images first
        if image_path.lower().endswith('.pdf'):
            combined_text = []
            doc = fitz.open(image_path)
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                pix = page.get_pixmap(dpi=200)
                
                temp_img = f"temp_page_{page_num}.png"
                pix.save(temp_img)
                
                # Run PaddleOCR on the temporary image slice
                result = ocr_engine.ocr(temp_img, cls=True)
                if result and result[0]:
                    for line in result[0]:
                        combined_text.append(line[1][0])
                
                # Clean up the temp image immediately
                if os.path.exists(temp_img):
                    os.remove(temp_img)
            doc.close()
            return " ".join(combined_text).strip()
            
        # If it's a regular flat image (.png, .jpg)
        else:
            result = ocr_engine.ocr(image_path, cls=True)
            extracted_text = []
            if result and result[0]:
                for line in result[0]:
                    text = line[1][0]
                    extracted_text.append(text)
                    
            return " ".join(extracted_text).strip()
        
    except Exception as e:
        logging.error(f"PaddleOCR failed on {image_path}: {e}")
        return ""
