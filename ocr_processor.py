"""
Legacy OCR processor module - maintained for backward compatibility.
New implementations should use core.document_processor.DocumentProcessor directly.
"""

from core.document_processor import DocumentProcessor


def classify_document(file_path, return_id=False):
    """
    Legacy function for backward compatibility.
    Processes a document and returns category and optional identifier.
    
    Args:
        file_path: Path to the document file
        return_id: Whether to return extracted TC/VKN identifier
        
    Returns:
        tuple: (category, identifier) if return_id=True, else category only
    """
    processor = DocumentProcessor()
    return processor.process_document(file_path, return_id)