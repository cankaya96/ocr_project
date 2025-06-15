import unicodedata


def normalize_filename(filename):
    """Normalize Unicode characters for Windows/macOS compatibility."""
    return unicodedata.normalize('NFKC', filename)


def print_results(folder_counts):
    """Print the processing results summary."""
    print("\n📊 Process completed:")
    for cat, count in folder_counts.items():
        print(f"- {cat}: {count} files")
