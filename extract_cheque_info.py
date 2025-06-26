#!/usr/bin/env python3
"""
Cheque Information Extraction Script

This script processes all cheque images in the uploads/cheque folder using Google Gemini AI
to extract the following information:
- IBAN number
- Check number
- Branch code  
- Account number
- TC/VKN number
- Bank code
- MICR code
- Check amount

Requirements:
1. Install required packages: pip install google-generativeai pillow
2. Set your Gemini API key: export GEMINI_API_KEY="your_api_key_here"
3. Run: python extract_cheque_info.py

The results will be saved to cheque_extraction_results.json
"""

import os
import sys
from dotenv import load_dotenv
from core import extract_cheque_information

# Load environment variables from .env file
load_dotenv()


def main():
    """Main function to run cheque information extraction."""
    
    # Get API key from environment (loaded from .env)
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ Error: GEMINI_API_KEY not found in .env file!")
        print("\nTo set your API key:")
        print("1. Get a free API key from: https://makersuite.google.com/app/apikey")
        print("2. Add it to .env file: GEMINI_API_KEY=your_api_key_here")
        print("3. Run this script again")
        sys.exit(1)
    
    print("🚀 Starting Cheque Information Extraction...")
    print("=" * 60)
    
    try:
        # Extract information from all cheque files
        output_file = extract_cheque_information(
            gemini_api_key=api_key,
            output_file="cheque_extraction_results.json"
        )
        
        print(f"\n✅ Extraction completed successfully!")
        print(f"📄 Results saved to: {output_file}")
        
        # Show instructions for viewing results
        print("\n📋 Next steps:")
        print("1. Open the JSON file to view extracted data")
        print("2. Import the data into your application")
        print("3. Manually verify critical information")
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("\nMissing dependencies. Please install:")
        print("pip install google-generativeai pillow")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nPlease check:")
        print("1. Your Gemini API key is valid")
        print("2. The uploads/cheque folder exists")
        print("3. There are image files in the cheque folder")


if __name__ == "__main__":
    main()
