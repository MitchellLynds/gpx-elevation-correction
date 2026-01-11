#!/usr/bin/env python3
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from cli_utils import parse_args, get_output_path, find_gpx_files
from main import process_gpx_file 

def main():
    args = parse_args()

    if args.batch:
        # Batch mode
        if not Path(args.input).is_dir():
            print(f"Error: {args.input} is not a directory")
            sys.exit(1)

        gpx_files = find_gpx_files(args.input)

        if not gpx_files:
            print(f"No GPX files found in {args.input}")
            sys.exit(1)

        print(f"Found {len(gpx_files)} GPX files to process/n")

        for i, gpx_file in enumerate(gpx_files, 1):
            print(f"[{i}/{len(gpx_files)}] Processing {gpx_file.name}...")
            output_path = get_output_path(gpx_file, None)
            process_gpx_file(str(gpx_file), str(output_path), args)
            print()

    else:
        # Single file mode
        if not Path(args.input).exists():
            print(f"Error: {args.input} not found")
            sys.exit(1)

        output_path = get_output_path(args.input, args.output)
        process_gpx_file(args.input, str(output_path), args)

if __name__ == '__main__':
    main()