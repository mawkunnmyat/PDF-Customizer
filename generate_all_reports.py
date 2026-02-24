import os
from pypdf import PdfReader, PdfWriter

def generate_personality_report(personality_type, input_filename):
    """
    Generates a specific AI Readiness Report based on the personality type.
    """
    
    # Configuration: Maps the Personality Name to its specific Page Index
    # Note: PDF Page 12 is Index 11
    personality_map = {
        "Exploring":   9,   # Page 10
        "Building":    10,  # Page 11
        "Integrating": 11,  # Page 12 (The one you asked for!)
        "Leading":     12   # Page 13
    }
    
    if personality_type not in personality_map:
        print(f"❌ Error: Unknown personality '{personality_type}'")
        return

    target_page_index = personality_map[personality_type]
    output_filename = f"STT25_Personalised_{personality_type}_AI.pdf"

    if not os.path.exists(input_filename):
        print(f"❌ Error: Input file '{input_filename}' not found.")
        return

    try:
        reader = PdfReader(input_filename)
        writer = PdfWriter()
        total_pages = len(reader.pages)

        # 1. Add Common Intro (Pages 1-9 / Indices 0-8)
        for i in range(0, 9):
            writer.add_page(reader.pages[i])
            
        # 2. Add The Specific Personality Summary
        print(f"   -> Inserting '{personality_type} AI' Summary (Page {target_page_index + 1})...")
        writer.add_page(reader.pages[target_page_index])
        
        # 3. Add Deep Dives & Outro (Page 14 to End / Index 13+)
        for i in range(13, total_pages):
            writer.add_page(reader.pages[i])

        # 4. Save
        with open(output_filename, "wb") as f_out:
            writer.write(f_out)
            
        print(f"✅ Success! Generated: {output_filename}")

    except Exception as e:
        print(f"❌ Error: {e}")

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    SOURCE_FILE = "STT25_7806_AI_Readiness_Report_v2.pdf"
    
    # Run for all three types you have requested so far:
    generate_personality_report("Exploring", SOURCE_FILE)
    generate_personality_report("Building", SOURCE_FILE)
    generate_personality_report("Integrating", SOURCE_FILE)