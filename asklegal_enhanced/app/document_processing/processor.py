from typing import List, Dict, Any
import os
from PyPDF2 import PdfReader
from docx import Document as DocxDocument
from app.document_processing.parsers.advanced_parser import advanced_parser
from app.document_processing.preprocessors.ocr import ocr_preprocessor

class DocumentProcessor:
    """Enhanced document processor with layout awareness and advanced parsing"""
    
    def __init__(self):
        self.supported_types = ['pdf', 'docx', 'txt']
        self.advanced_parser = advanced_parser
        self.ocr_preprocessor = ocr_preprocessor
    
    def process_document(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Process a document and return structured elements
        
        Args:
            file_path (str): Path to the document file
            
        Returns:
            List[Dict[str, Any]]: List of document elements with metadata
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Document not found: {file_path}")
        
        # Get file extension
        _, ext = os.path.splitext(file_path)
        file_type = ext.lower().lstrip('.')
        
        if file_type not in self.supported_types:
            raise ValueError(f"Unsupported file type: {file_type}")
        
        # Process based on file type with advanced parsing
        if file_type == 'pdf':
            return self._process_pdf_advanced(file_path)
        elif file_type == 'docx':
            return self._process_docx_advanced(file_path)
        elif file_type == 'txt':
            return self._process_txt(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
    
    def _process_pdf_advanced(self, file_path: str) -> List[Dict[str, Any]]:
        """Process a PDF document with advanced parsing"""
        try:
            # Try advanced parsing first
            elements = self.advanced_parser.parse_pdf(file_path)
            return elements
        except Exception as e:
            print(f"Advanced PDF parsing failed: {e}")
            # Fallback to basic processing
            return self._process_pdf_basic(file_path)
    
    def _process_pdf_basic(self, file_path: str) -> List[Dict[str, Any]]:
        """Basic PDF processing as fallback"""
        reader = PdfReader(file_path)
        elements = []
        
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text.strip():
                elements.append({
                    "id": f"page_{i}",
                    "text": text,
                    "type": "page",
                    "metadata": {
                        "page_number": i + 1,
                        "source": "pdf_basic"
                    }
                })
        
        return elements
    
    def _process_docx_advanced(self, file_path: str) -> List[Dict[str, Any]]:
        """Process a DOCX document with advanced parsing"""
        try:
            # Try advanced parsing first
            elements = self.advanced_parser.parse_docx(file_path)
            return elements
        except Exception as e:
            print(f"Advanced DOCX parsing failed: {e}")
            # Fallback to basic processing
            return self._process_docx_basic(file_path)
    
    def _process_docx_basic(self, file_path: str) -> List[Dict[str, Any]]:
        """Basic DOCX processing as fallback"""
        doc = DocxDocument(file_path)
        elements = []
        
        # Process paragraphs
        for i, paragraph in enumerate(doc.paragraphs):
            if paragraph.text.strip():
                elements.append({
                    "id": f"paragraph_{i}",
                    "text": paragraph.text,
                    "type": "paragraph",
                    "metadata": {
                        "style": paragraph.style.name if paragraph.style else "Normal",
                        "source": "docx_basic"
                    }
                })
        
        return elements
    
    def _process_txt(self, file_path: str) -> List[Dict[str, Any]]:
        """Process a TXT document"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split into paragraphs (separated by double newlines)
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
        
        elements = []
        for i, paragraph in enumerate(paragraphs):
            elements.append({
                "id": f"paragraph_{i}",
                "text": paragraph,
                "type": "paragraph",
                "metadata": {
                    "source": "txt"
                }
            })
        
        return elements
    
    def process_scanned_document(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Process a scanned document using OCR
        
        Args:
            file_path (str): Path to the scanned document
            
        Returns:
            List[Dict[str, Any]]: List of document elements with OCR text
        """
        _, ext = os.path.splitext(file_path)
        file_type = ext.lower().lstrip('.')
        
        if file_type == 'pdf':
            # Process scanned PDF
            result = self.ocr_preprocessor.process_scanned_pdf(file_path)
            return result.get("elements", [])
        else:
            # Process image file
            ocr_result = self.ocr_preprocessor.extract_text_with_layout(file_path)
            return [{
                "id": "ocr_result",
                "text": ocr_result["text"],
                "type": "ocr_text",
                "metadata": {
                    "confidence": ocr_result["confidence"],
                    "layout_blocks": ocr_result["layout_blocks"],
                    "source": "ocr"
                }
            }]
    
    def extract_metadata(self, file_path: str) -> Dict[str, Any]:
        """
        Extract enhanced metadata from a document
        
        Args:
            file_path (str): Path to the document file
            
        Returns:
            Dict[str, Any]: Document metadata
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Document not found: {file_path}")
        
        # Try advanced metadata extraction
        try:
            metadata = self.advanced_parser.extract_metadata(file_path)
            return metadata
        except Exception as e:
            print(f"Advanced metadata extraction failed: {e}")
            # Fallback to basic metadata extraction
            return self._extract_metadata_basic(file_path)
    
    def _extract_metadata_basic(self, file_path: str) -> Dict[str, Any]:
        """Basic metadata extraction as fallback"""
        import os
        from datetime import datetime
        
        # Get file extension
        _, ext = os.path.splitext(file_path)
        file_type = ext.lower().lstrip('.')
        
        stat = os.stat(file_path)
        
        return {
            "file_name": os.path.basename(file_path),
            "file_type": file_type,
            "file_size": stat.st_size,
            "created_time": datetime.fromtimestamp(stat.st_ctime).isoformat(),
            "modified_time": datetime.fromtimestamp(stat.st_mtime).isoformat()
        }

# Global instance
document_processor = DocumentProcessor()