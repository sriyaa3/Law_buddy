import pytesseract
from PIL import Image
import cv2
import numpy as np
from typing import Dict, Any
import pdfplumber
import io

class OCRPreprocessor:
    """Advanced OCR preprocessing for scanned documents"""
    
    def __init__(self):
        # Initialize layout model for document structure detection
        try:
            import layoutparser as lp
            self.layout_model = lp.Detectron2LayoutModel(
                'lp://PubLayNet/faster_rcnn_R_50_FPN_3x/config',
                extra_config=["MODEL.ROI_HEADS.SCORE_THRESH_TEST", 0.8],
                label_map={0: "Text", 1: "Title", 2: "List", 3: "Table", 4: "Figure"}
            )
        except:
            self.layout_model = None
            print("Warning: Layout model not available. Using basic OCR.")
    
    def preprocess_image(self, image_path: str) -> np.ndarray:
        """
        Preprocess image for better OCR accuracy
        
        Args:
            image_path (str): Path to the image file
            
        Returns:
            np.ndarray: Preprocessed image
        """
        # Load image
        image = cv2.imread(image_path)
        
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply noise reduction
        denoised = cv2.medianBlur(gray, 3)
        
        # Apply thresholding
        _, thresh = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        return thresh
    
    def extract_text_with_layout(self, image_path: str) -> Dict[str, Any]:
        """
        Extract text with layout information using OCR and layout detection
        
        Args:
            image_path (str): Path to the image file
            
        Returns:
            Dict[str, Any]: Extracted text with layout information
        """
        # Preprocess image
        processed_image = self.preprocess_image(image_path)
        
        # Save processed image temporarily
        temp_path = image_path.replace('.', '_processed.')
        cv2.imwrite(temp_path, processed_image)
        
        # Extract text with pytesseract
        ocr_result = pytesseract.image_to_data(processed_image, output_type=pytesseract.Output.DICT)
        
        # Extract layout blocks if model is available
        layout_blocks = []
        if self.layout_model:
            try:
                image_pil = Image.open(image_path)
                layout = self.layout_model.detect(image_pil)
                layout_blocks = [(block.type, block.coordinates) for block in layout]
            except Exception as e:
                print(f"Layout detection failed: {e}")
        
        # Clean up temporary file
        try:
            import os
            os.remove(temp_path)
        except:
            pass
        
        return {
            "text": " ".join(ocr_result["text"]),
            "layout_blocks": layout_blocks,
            "confidence": np.mean([conf for conf in ocr_result["conf"] if conf > 0]) if ocr_result["conf"] else 0
        }
    
    def process_scanned_pdf(self, pdf_path: str) -> Dict[str, Any]:
        """
        Process scanned PDF using OCR
        
        Args:
            pdf_path (str): Path to the PDF file
            
        Returns:
            Dict[str, Any]: Extracted text with metadata
        """
        elements = []
        
        try:
            # Use pdfplumber as fallback
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    # Extract images from page
                    images = page.images
                    
                    for img_num, img in enumerate(images):
                        # Extract image and apply OCR
                        try:
                            # Get image bytes
                            img_bytes = img["stream"].get_data()
                            
                            # Convert to PIL Image
                            img_pil = Image.open(io.BytesIO(img_bytes))
                            
                            # Apply OCR
                            text = pytesseract.image_to_string(img_pil)
                            
                            if text.strip():
                                elements.append({
                                    "id": f"page_{page_num}_img_{img_num}",
                                    "text": text,
                                    "type": "image_text",
                                    "metadata": {
                                        "page_number": page_num + 1,
                                        "bbox": img["bbox"]
                                    }
                                })
                        except Exception as img_error:
                            print(f"Error processing image on page {page_num}: {img_error}")
        except Exception as e:
            print(f"PDF processing failed, using basic OCR: {e}")
            
            # Fallback to basic OCR on the PDF
            try:
                # Extract text with pytesseract directly on PDF
                text = pytesseract.image_to_string(pdf_path)
                if text.strip():
                    elements.append({
                        "id": "pdf_ocr",
                        "text": text,
                        "type": "pdf_text",
                        "metadata": {
                            "source": "pdf_ocr"
                        }
                    })
            except Exception as ocr_error:
                print(f"Basic OCR failed: {ocr_error}")
        
        return {
            "elements": elements,
            "total_elements": len(elements),
            "source": "scanned_pdf"
        }

# Global instance
ocr_preprocessor = OCRPreprocessor()