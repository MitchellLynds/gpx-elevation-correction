import argparse
import os
from pathlib import Path
def parse_args():
    parser = argparse.ArgumentParser(
        description='Correct GPX elevation data using high-resolution elevation sources',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Process single file with USGS data
    python cli.py input.gpx --source usgs
    
    # Process with SRTM and specify output locaation
    python cli.py input.gpx --output corrected.gpx --source srtm
    
    # Process all GPX files in a directory
    python cli.py data/input/ --batch
    """
    )

    parser.add_argument('input',
                        help='Input GPX file or directory (for batch mode)')
    
    parser.add_argument('-o', '--output',
                        help='Output file path (default: data/output/corrected_<filename>)')
    
    parser.add_argument('-s', '--source',
                        choices=['srtm', 'usgs'],
                        default='usgs',
                        help='Elevation data source (default: usgs)')
    
    parser.add_argument('-b', '--batch',
                        action='store_true',
                        help='Batch rocess all GPX files in input directory')

    parser.add_argument('--no-viz',
                       action='store_true',
                       help='Skip visualization generation')

    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        help='Enable verbose output')
    return parser.parse_args()

def get_output_path(input_path, output_arg):
    """Generate output path if not specified"""
    if output_arg:
        return output_arg
    
    input_file = Path(input_path)
    output_dir = Path('data/output')
    output_dir.mkdir(parents=True, exist_ok=True)

    return output_dir / f"corrected_{input_file.name}"

def find_gpx_files(directory):
    """Find all GPX files in directory"""
    return list(Path(directory).glob('*.gpx'))