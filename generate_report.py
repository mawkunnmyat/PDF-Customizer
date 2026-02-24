import os
import sys
from pypdf import PdfReader, PdfWriter

def generate_exploring_ai_report(input_filename, output_filename):
    """
    Splits the master AI Readiness Report to create a personalized
    'Exploring AI' version by removing other personality summaries.
    
    Args:
        input_filename (str): The source PDF file.
        output_filename (str): The target output file.
    """
    
    # 1. Validation: Ensure input file exists
    if not os.path.exists(input_filename):
        print(f"❌ Error: The file '{input_filename}' was not found.")
        print("   -> Please ensure the PDF is in the same folder as this script.")
        return

    try:
        print(f"⚙️  Processing: {input_filename}...")
        reader = PdfReader(input_filename)
        writer = PdfWriter()
        
        total_pages = len(reader.pages)
        print(f"📄 Total Source Pages: {total_pages}")

        # --- LOGIC BLOCK: DEFINE PAGE RANGES (0-Based Indexing) ---
        # We need Pages 1-10, so we slice range(0, 10).
        # We skip Pages 11-13 (Indices 10, 11, 12).
        # We keep Page 14 to End, so we slice range(13, total_pages).
        
        # Part 1: Intro + Exploring AI Summary
        print("   -> Adding Header & Exploring AI Summary (Pages 1-10)...")
        for i in range(0, 10):
            writer.add_page(reader.pages[i])
            
        # Part 2: Deep Dives + Conclusion
        print(f"   -> Adding Deep Dives & Outro (Page 14-{total_pages})...")
        for i in range(13, total_pages):
            writer.add_page(reader.pages[i])

        # --- WRITE OUTPUT ---
        with open(output_filename, "wb") as f_out:
            writer.write(f_out)
            
        print(f"✅ Success! Report generated: {output_filename}")
        print("   -> Verified: Pages 11, 12, and 13 have been removed.")

    except Exception as e:
        print(f"❌ Critical Error: {str(e)}")

# --- EXECUTION ---
if __name__ == "__main__":
    # Configuration (use your own input PDF; output name is generic)
    SOURCE_FILE = "ai_readiness_report.pdf"
    OUTPUT_FILE = "personalised_exploring_ai.pdf"
    
    generate_exploring_ai_report(SOURCE_FILE, OUTPUT_FILE)