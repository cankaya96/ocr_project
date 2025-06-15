from .config import CATEGORIES


class DocumentClassifier:
    """Classifies documents based on extracted text content."""
    
    def __init__(self, categories: dict = None):
        """Initialize classifier with categories."""
        self.categories = categories or CATEGORIES
    
    def classify_text(self, text: str) -> str:
        """Classify text into document category based on keywords."""
        text_lower = text.lower()
        
        for category, keywords in self.categories.items():
            if any(keyword in text_lower for keyword in keywords):
                return category
        
        return 'others'
    
    def get_category_keywords(self, category: str) -> list:
        """Get keywords for specific category."""
        return self.categories.get(category, [])
