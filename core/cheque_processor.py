import json
import os
from typing import List, Dict, Any
from .file_operations import FileOperations
from .config import UPLOAD_FOLDER
from .gemini_extractor import GeminiChequeExtractor


class ChequeProcessor:
    """Process all cheque files and extract information using Gemini."""
    
    def __init__(self, gemini_api_key: str = None):
        """Initialize cheque processor with Gemini extractor."""
        self.extractor = GeminiChequeExtractor(gemini_api_key)
        self.cheque_folder = os.path.join(UPLOAD_FOLDER, 'cheque')
    
    def process_all_cheques(self) -> List[Dict[str, Any]]:
        """
        Process all cheque files and extract information.
        
        Returns:
            List[Dict]: List of extracted cheque information
        """
        if not os.path.exists(self.cheque_folder):
            print(f"Cheque folder not found: {self.cheque_folder}")
            return []
        
        # Get all files in cheque folder
        cheque_files = self._get_cheque_files()
        
        if not cheque_files:
            print("No cheque files found.")
            return []
        
        print(f"Found {len(cheque_files)} cheque files. Processing...")
        
        results = []
        for i, file_path in enumerate(cheque_files, 1):
            print(f"Processing {i}/{len(cheque_files)}: {os.path.basename(file_path)}")
            
            # Extract information using Gemini
            cheque_info = self.extractor.extract_cheque_info(file_path)
            results.append(cheque_info)
        
        return results
    
    def process_and_save_json(self, output_file: str = "cheque_extraction_results.json") -> str:
        """
        Process all cheques and save results to JSON file.
        
        Args:
            output_file (str): Output JSON file name
            
        Returns:
            str: Path to the saved JSON file
        """
        results = self.process_all_cheques()
        
        # Create output path
        output_path = os.path.join(os.getcwd(), output_file)
        
        # Save to JSON
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"\nResults saved to: {output_path}")
        print(f"Total processed files: {len(results)}")
        
        # Print summary
        self._print_summary(results)
        
        return output_path
    
    def _get_cheque_files(self) -> List[str]:
        """Get all image files from cheque folder."""
        supported_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif'}
        
        all_files = FileOperations.get_all_files_in_directory(self.cheque_folder)
        
        cheque_files = []
        for file_path in all_files:
            file_ext = os.path.splitext(file_path)[1].lower()
            if file_ext in supported_extensions:
                cheque_files.append(file_path)
        
        return sorted(cheque_files)
    
    def _print_summary(self, results: List[Dict[str, Any]]):
        """Print a summary of extraction results."""
        print("\n" + "="*50)
        print("EXTRACTION SUMMARY")
        print("="*50)
        
        total_files = len(results)
        successful_extractions = 0
        
        # Count successful extractions (files with at least one non-null field)
        for result in results:
            has_data = any(
                result.get(field) is not None 
                for field in ['_iban', '_checkNo', '_branchCode', '_accountNumber', 
                             '_tcknVkn', '_bankCode', '_micrCode', '_checkAmount']
            )
            if has_data:
                successful_extractions += 1
        
        print(f"Total files processed: {total_files}")
        print(f"Successful extractions: {successful_extractions}")
        print(f"Failed extractions: {total_files - successful_extractions}")
        print(f"Success rate: {(successful_extractions/total_files*100):.1f}%" if total_files > 0 else "N/A")
        
        # Show sample results
        print("\nSample Results:")
        for i, result in enumerate(results[:3]):  # Show first 3 results
            print(f"\n{i+1}. {result.get('_fileName', 'Unknown')}")
            for key, value in result.items():
                if key != '_fileName' and value is not None:
                    print(f"   {key}: {value}")
        
        if len(results) > 3:
            print(f"\n... and {len(results) - 3} more files")


def extract_cheque_information(gemini_api_key: str = None, output_file: str = "cheque_extraction_results.json") -> str:
    """
    Convenience function to extract cheque information from all files.
    
    Args:
        gemini_api_key (str): Gemini API key (optional if set in environment)
        output_file (str): Output JSON file name
        
    Returns:
        str: Path to the saved JSON file
    """
    processor = ChequeProcessor(gemini_api_key)
    return processor.process_and_save_json(output_file)
