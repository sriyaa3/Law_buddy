from typing import Dict, Any

class OCRPreprocessor:
    """Simplified OCR preprocessor (OCR disabled)"""
    
    def __init__(self):
        print("Initialized simplified OCR preprocessor (OCR disabled)")
    
    def preprocess_image(self, image_path: str):
        """Simplified preprocess image (no-op)"""
        return None
    
    def extract_text_with_layout(self, image_path: str) -> Dict[str, Any]:
        """
        Extract text with layout (simplified, returns placeholder)
        
        Args:
            image_path (str): Path to the image file
            
        Returns:
            Dict[str, Any]: Placeholder result
        """
        return {
            "text": "OCR not available - please use text-based documents",
            "layout_blocks": [],
            "confidence": 0
        }
    
    def process_scanned_pdf(self, pdf_path: str) -> Dict[str, Any]:
        """
        Process scanned PDF (simplified, returns placeholder)
        
        Args:
            pdf_path (str): Path to the PDF file
            
        Returns:
            Dict[str, Any]: Placeholder result
        """
        return {
            "elements": [{
                "id": "placeholder",
                "text": "OCR not available - please use text-based PDF documents",
                "type": "placeholder",
                "metadata": {"source": "ocr_disabled"}
            }],
            "total_elements": 1,
            "source": "ocr_disabled"
        }

# Global instance
ocr_preprocessor = OCRPreprocessor()