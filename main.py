import os
import unicodedata
from ocr_processor import classify_document, generate_unique_filename

UPLOAD_FOLDER = 'uploads'

CATEGORY_FOLDERS = [
    'invoices', 'ids', 'cheque', 'signature_declaration',
    'residence_certificate', 'trade_registry_gazette',
    'driver_license', 'population_register', 'tax_plate',
    'contracts', 'kvkk_explicit_consent', 'digital_abf_commitment',
    'power_of_attorney', 'abf', 'cheque_customer_screening',
    'promissory_note', 'offset_and_payment_order',
    'unprocessed_return_payment_order', 'others', 'error_files',
    'factoring_agreement', 'tax_plate', 'activity_certificate', 'independent_audit_certificate'
]

# Create folders
for folder in CATEGORY_FOLDERS:
    os.makedirs(os.path.join(UPLOAD_FOLDER, folder), exist_ok=True)

# Normalize Unicode characters (Windows/macOS compatibility)
def normalize_filename(filename):
    return unicodedata.normalize('NFKC', filename)

def process_files_in_directory(directory_path):
    results = []
    folder_counts = {folder: 0 for folder in CATEGORY_FOLDERS}

    all_files = []
    for root, _, files in os.walk(directory_path):
        for file in files:
            all_files.append(os.path.join(root, file))

    total = len(all_files)

    for idx, file_path in enumerate(all_files, start=1):
        file_name = normalize_filename(os.path.basename(file_path))  # normalize
        file_root, file_ext = os.path.splitext(file_name)

        try:
            # OCR process and TC/VKN detection
            category, detected_id = classify_document(file_path, return_id=True)
            dest_folder = os.path.join(UPLOAD_FOLDER, category)
            os.makedirs(dest_folder, exist_ok=True)

            if detected_id:
                new_file_name = generate_unique_filename(detected_id, dest_folder, file_ext[1:])
                final_path = os.path.join(dest_folder, new_file_name)
                print(f"[{idx}/{total}] {file_name} → {category} (NEW NAME: {new_file_name})")
            else:
                new_file_name = file_name
                final_path = os.path.join(dest_folder, new_file_name)
                print(f"[{idx}/{total}] {file_name} → {category}")

            os.rename(file_path, final_path)
            folder_counts[category] += 1
            results.append((file_name, category))

        except Exception as e:
            error_folder = os.path.join(UPLOAD_FOLDER, 'error_files')
            os.makedirs(error_folder, exist_ok=True)

            base_name, ext = os.path.splitext(file_name)
            error_path = os.path.join(error_folder, file_name)
            counter = 1
            while os.path.exists(error_path):
                error_path = os.path.join(error_folder, f"{base_name}({counter}){ext}")
                counter += 1

            os.rename(file_path, error_path)
            folder_counts["error_files"] += 1
            print(f"[{idx}/{total}] {file_name} → error_files ❌ {str(e)[:50]}")

    print("\n📊 Process completed:")
    for cat, count in folder_counts.items():
        print(f"- {cat}: {count} files")

if __name__ == "__main__":
    directory_path = "Documents"
    if not os.path.exists(directory_path):
        print(f"ERROR: '{directory_path}' folder not found.")
    else:
        process_files_in_directory(directory_path)
