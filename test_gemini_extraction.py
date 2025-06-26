#!/usr/bin/env python3
"""
Test script for Gemini cheque extraction functionality.
This script tests a single cheque image to verify the integration works.
"""

import os
import sys
from dotenv import load_dotenv
from core.gemini_extractor import GeminiChequeExtractor

# Load environment variables from .env file
load_dotenv()


def test_single_cheque():
    """Test extraction on a single cheque image."""
    
    # Get API key from environment (loaded from .env)
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ GEMINI_API_KEY not set. Please check your .env file.")
        return False
    
    # Find a test image
    cheque_folder = "uploads/cheque"
    if not os.path.exists(cheque_folder):
        print(f"❌ Cheque folder not found: {cheque_folder}")
        return False
    
    # Get first image file
    test_image = None
    for file in os.listdir(cheque_folder):
        if file.lower().endswith(('.jpg', '.jpeg', '.png')):
            test_image = os.path.join(cheque_folder, file)
            break
    
    if not test_image:
        print("❌ No image files found in cheque folder")
        return False
    
    print(f"🧪 Testing with image: {os.path.basename(test_image)}")
    
    try:
        # Initialize extractor
        extractor = GeminiChequeExtractor(api_key)
        
        # Extract information
        result = extractor.extract_cheque_info(test_image)
        
        # Display results
        print("\n📋 Extraction Results:")
        print("-" * 40)
        for key, value in result.items():
            status = "✅" if value is not None else "❌"
            print(f"{status} {key}: {value}")
        
        print("\n✅ Test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


if __name__ == "__main__":
    success = test_single_cheque()
    sys.exit(0 if success else 1)
