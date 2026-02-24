#!/usr/bin/env python3
"""
PDF Splitter - Extract specific pages from a PDF document.

This script extracts pages 1-10 and pages 14-end from a PDF file,
skipping pages 11-13, to create a new PDF document.
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

# Default configuration
DEFAULT_INPUT_FILE = "STT25_7806_AI_Readiness_Report_v2.pdf"
DEFAULT_OUTPUT_FILE = "STT25_Exploring_AI_Report.pdf"

try:
    from pypdf import PdfReader, PdfWriter
except ImportError as e:
    print(
        "Error: pypdf library is not installed.\n"
        "Please install it using: pip install -r requirements.txt",
        file=sys.stderr,
    )
    sys.exit(1)


def validate_input_file(input_path: Path) -> None:
    """
    Validate that the input file exists and is a PDF file.
    
    Args:
        input_path: Path to the input PDF file
        
    Raises:
        FileNotFoundError: If the input file doesn't exist
        ValueError: If the file is not a PDF
    """
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    if not input_path.is_file():
        raise ValueError(f"Input path is not a file: {input_path}")
    
    if input_path.suffix.lower() != ".pdf":
        raise ValueError(f"Input file must be a PDF: {input_path}")


def create_exploring_ai_report(
    input_path: Path,
    output_path: Path,
    pages_first_range: tuple[int, int] = (1, 10),
    pages_skip_range: tuple[int, int] = (11, 13),
    verbose: bool = True,
) -> bool:
    """
    Extract specific page ranges from a PDF file.
    
    This function creates a new PDF containing:
    - Pages from pages_first_range (default: 1-10)
    - All pages after pages_skip_range (default: 14-end)
    - Pages in pages_skip_range are excluded
    
    Args:
        input_path: Path to the input PDF file
        output_path: Path where the output PDF will be saved
        pages_first_range: Tuple of (start, end) for first page range (1-indexed)
        pages_skip_range: Tuple of (start, end) for pages to skip (1-indexed)
        verbose: If True, print progress messages
        
    Returns:
        True if successful, False otherwise
        
    Raises:
        FileNotFoundError: If input file doesn't exist
        ValueError: If input file is invalid or page ranges are invalid
        IOError: If there's an error reading/writing files
    """
    # Validate input file
    validate_input_file(input_path)
    
    # Convert 1-indexed page ranges to 0-indexed
    first_start_idx = pages_first_range[0] - 1
    first_end_idx = pages_first_range[1]  # Exclusive end
    skip_start_idx = pages_skip_range[0] - 1
    skip_end_idx = pages_skip_range[1]  # Exclusive end
    
    try:
        if verbose:
            print(f"Reading PDF: {input_path}")
        
        reader = PdfReader(str(input_path))
        total_pages = len(reader.pages)
        
        if verbose:
            print(f"Total pages in input: {total_pages}")
        
        # Validate page ranges
        if first_end_idx > total_pages:
            raise ValueError(
                f"First range end ({pages_first_range[1]}) exceeds total pages ({total_pages})"
            )
        
        if first_start_idx < 0:
            raise ValueError(f"First range start ({pages_first_range[0]}) must be >= 1")
        
        if skip_start_idx >= total_pages:
            raise ValueError(
                f"Skip range start ({pages_skip_range[0]}) exceeds total pages ({total_pages})"
            )
        
        writer = PdfWriter()
        pages_added = 0
        
        # Add Part 1: First page range (e.g., pages 1-10)
        if verbose:
            print(f"Adding pages {pages_first_range[0]}-{pages_first_range[1]}...")
        for i in range(first_start_idx, first_end_idx):
            writer.add_page(reader.pages[i])
            pages_added += 1
        
        # Add Part 2: Pages after skip range (e.g., pages 14-end)
        second_start_idx = skip_end_idx
        if second_start_idx < total_pages:
            if verbose:
                print(f"Adding pages {skip_end_idx + 1}-{total_pages}...")
            for i in range(second_start_idx, total_pages):
                writer.add_page(reader.pages[i])
                pages_added += 1
        
        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write the output file
        if verbose:
            print(f"Writing output PDF: {output_path}")
        
        with open(output_path, "wb") as f_out:
            writer.write(f_out)
        
        if verbose:
            print(f"\n✅ Success! Created: {output_path}")
            print(f"   - Pages kept: {pages_first_range[0]}-{pages_first_range[1]} "
                  f"(Intro + Exploring Summary)")
            print(f"   - Pages removed: {pages_skip_range[0]}-{pages_skip_range[1]} "
                  f"(Other Personalities)")
            if second_start_idx < total_pages:
                print(f"   - Pages kept: {skip_end_idx + 1}-{total_pages} "
                      f"(Deep Dives + Outro)")
            print(f"   - Total pages in output: {pages_added}")
        
        return True
        
    except FileNotFoundError:
        raise
    except ValueError as e:
        if verbose:
            print(f"❌ Validation Error: {e}", file=sys.stderr)
        raise
    except Exception as e:
        if verbose:
            print(f"❌ Unexpected Error: {type(e).__name__}: {e}", file=sys.stderr)
        raise IOError(f"Failed to process PDF: {e}") from e


def main() -> int:
    """
    Main entry point for the script.
    
    Supports both simple usage (no arguments, uses defaults) and
    advanced usage (with command-line arguments).
    """
    parser = argparse.ArgumentParser(
        description="Extract specific pages from a PDF document.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Examples:
  # Simple usage with default filenames
  %(prog)s
  
  # Custom input/output files
  %(prog)s input.pdf output.pdf
  
  # Custom page ranges
  %(prog)s input.pdf output.pdf --first-range 1 10 --skip-range 11 13
  
  # Quiet mode
  %(prog)s --quiet

Default input file: {DEFAULT_INPUT_FILE}
Default output file: {DEFAULT_OUTPUT_FILE}
        """,
    )
    
    parser.add_argument(
        "input_file",
        type=Path,
        nargs="?",
        default=None,
        help=f"Path to the input PDF file (default: {DEFAULT_INPUT_FILE})",
    )
    parser.add_argument(
        "output_file",
        type=Path,
        nargs="?",
        default=None,
        help=f"Path for the output PDF file (default: {DEFAULT_OUTPUT_FILE})",
    )
    parser.add_argument(
        "--first-range",
        type=int,
        nargs=2,
        metavar=("START", "END"),
        default=[1, 10],
        help="First page range to include (default: 1 10)",
    )
    parser.add_argument(
        "--skip-range",
        type=int,
        nargs=2,
        metavar=("START", "END"),
        default=[11, 13],
        help="Page range to skip (default: 11 13)",
    )
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Suppress progress messages",
    )
    
    args = parser.parse_args()
    
    # Use defaults if arguments not provided
    input_file = args.input_file if args.input_file is not None else Path(DEFAULT_INPUT_FILE)
    output_file = args.output_file if args.output_file is not None else Path(DEFAULT_OUTPUT_FILE)
    
    try:
        success = create_exploring_ai_report(
            input_path=input_file,
            output_path=output_file,
            pages_first_range=tuple(args.first_range),
            pages_skip_range=tuple(args.skip_range),
            verbose=not args.quiet,
        )
        return 0 if success else 1
    except (FileNotFoundError, ValueError, IOError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.", file=sys.stderr)
        return 130
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
