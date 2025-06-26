import google.generativeai as genai
import json
import base64
from PIL import Image
from typing import Optional, Dict, Any
import os


class GeminiChequeExtractor:
    """Gemini model for extracting cheque information."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize Gemini extractor with API key."""
        if api_key is None:
            api_key = os.getenv('GEMINI_API_KEY')
        
        if not api_key:
            raise ValueError("Gemini API key is required. Set GEMINI_API_KEY environment variable or pass api_key parameter.")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def extract_cheque_info(self, image_path: str) -> Dict[str, Any]:
        """
        Extract cheque information from image using Gemini.
        
        Args:
            image_path (str): Path to the cheque image
            
        Returns:
            dict: Extracted cheque information
        """
        try:
            # Load and prepare image
            image = Image.open(image_path)
            
            # Create prompt for Gemini
            prompt = self._create_extraction_prompt()
            
            # Generate content with Gemini
            response = self.model.generate_content([prompt, image])
            
            # Parse JSON response
            extracted_info = self._parse_response(response.text)
            
            # Add filename to result
            extracted_info['fileName'] = os.path.basename(image_path)
            
            return extracted_info
            
        except Exception as e:
            print(f"Error extracting info from {image_path}: {str(e)}")
            return self._create_null_response(os.path.basename(image_path))
    
    def _create_extraction_prompt(self) -> str:
        """Create the prompt for Gemini to extract cheque information."""
        return """
Bu görüntüdeki Türk çeki/bankacılık belgesinden aşağıdaki bilgileri çıkar ve JSON formatında döndür.
Eğer bir bilgi görüntüde yoksa veya okunamazsa, o alan için null değeri kullan.

Çıkaracağın bilgiler:
- iban: IBAN numarası (TR ile başlayan 26 haneli kod)
- checkNumber: Çek numarası 
- branchCode: Şube kodu
- accountNumber: Hesap numarası
- customerIdNumber: TC Kimlik numarası (11 haneli) veya VKN (10 haneli)
- bankCode: Banka kodu
- micrCode: MICR kodu (çekin altındaki manyetik kod)
- checkAmount: Çek tutarı (sadece sayısal değer, para birimi olmadan)

Lütfen sadece JSON formatında yanıt ver, başka açıklama ekleme:

{
    "iban": null,
    "checkNumber": null,
    "branchCode": null,
    "accountNumber": null,
    "customerIdNumber": null,
    "bankCode": null,
    "micrCode": null,
    "checkAmount": null
}
"""
    
    def _parse_response(self, response_text: str) -> Dict[str, Any]:
        """Parse Gemini response and extract JSON."""
        try:
            # Clean the response text
            cleaned_text = response_text.strip()
            
            # Remove markdown code blocks if present
            if cleaned_text.startswith('```json'):
                cleaned_text = cleaned_text[7:]
            if cleaned_text.startswith('```'):
                cleaned_text = cleaned_text[3:]
            if cleaned_text.endswith('```'):
                cleaned_text = cleaned_text[:-3]
            
            cleaned_text = cleaned_text.strip()
            
            # Parse JSON
            result = json.loads(cleaned_text)
            
            # Ensure all required fields exist
            required_fields = [
                'iban', 'checkNumber', 'branchCode', 'accountNumber',
                'customerIdNumber', 'bankCode', 'micrCode', 'checkAmount'
            ]
            
            for field in required_fields:
                if field not in result:
                    result[field] = None
            
            return result
            
        except Exception as e:
            print(f"Error parsing Gemini response: {str(e)}")
            print(f"Response text: {response_text}")
            return self._create_null_response()
    
    def _create_null_response(self, filename: str = None) -> Dict[str, Any]:
        """Create a response with all null values."""
        return {
            'fileName': filename,
            'iban': None,
            'checkNumber': None,
            'branchCode': None,
            'accountNumber': None,
            'customerIdNumber': None,
            'bankCode': None,
            'micrCode': None,
            'checkAmount': None
        }
