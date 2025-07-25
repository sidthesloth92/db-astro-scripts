import os
from datetime import datetime, timedelta
import shutil
import sys
from astropy.io import fits

# This script organizes FITS image files from a specified directory into a structured folder hierarchy
# based on camera model, target name, frame type, date, and filter. It parses filenames to extract metadata,
# determines if the image is mono or color, adjusts the date based on the time, and copies files into
# the appropriate output directories without overwriting existing files.

# Check if the user provided a directory path as an argument
if len(sys.argv) < 2:
  print("Usage: python split_by_date.py <directory_path>")
  sys.exit(1)

# Path to the directory containing the FITS files to be organized
directory_path = sys.argv[1]

# Recursively collect all FITS files in the directory and subdirectories
fits_files = []
for root, _, files in os.walk(directory_path):
  for file in files:
    if file.endswith('.fit') and not file.startswith('.'):
      fits_files.append(os.path.join(root, file))


# Iterate over each file in the directory
for filepath in fits_files:
  filename = os.path.basename(filepath)


  # Ignore hidden files (those starting with '.') and ensure they have the correct extension
  if not filename.startswith('.') and filename.endswith('.fit'):

    # Split the filename into parts using underscore as the delimiter
    parts = filename.split('_')

    is_mono = False
    # Check if the sixth part of the filename indicates a mono filter
    # Mono filters: L, R, G, B, Ha, OIII, SII, H, O, S
    if parts[5] in ['L', 'R', 'G', 'B', 'Ha', 'OIII', 'SII', 'H', 'O', 'S']:
      is_mono = True

    # Set offset for parsing date and time based on mono or color image
    offset = 0 if is_mono else -1

    # Extract metadata from filename parts
    frame_type = parts[0]  # e.g., 'Light'
    target_name = parts[1]
    camera_model = parts[4]
    filter = parts[5] if is_mono else parts[len(parts) - 1].split(".")[0]  # Last part for color images

    # Print extracted metadata for debugging
    print(f"Processing file: {filename}")
    
    print(f"Frame Type: {frame_type}, Target Name: {target_name}, Camera Model: {camera_model}, Filter: {filter}")
    
    # Determine the output directory structure
    # Default output directory is 'output' in the current working directory
    if len(sys.argv) >= 3:
      output_dir = os.path.abspath(sys.argv[2])
    else:
      output_dir = os.path.join(os.getcwd(), 'output')

    camera_dir = os.path.join(output_dir, camera_model)
    target_dir = os.path.join(camera_dir, target_name)
    frame_dir = os.path.join(target_dir, frame_type)

    # Create the directory structure if it doesn't exist
    os.makedirs(frame_dir, exist_ok=True)

    # Extract date and time from the filename
    date = parts[7 + offset].split('-')[0]  # e.g., '20250721'
    time = parts[7 + offset].split('-')[1]  # e.g., '012502'

    # Print extracted date and time for debugging
    print(f"Date: {date}, Time: {time}")

    # Determine if the date should be offset by one day based on the time (after 16:00:00)
    date_offset = 0 if int(time) < 160000 else 1

    # Adjust the date if necessary and format it as YYYY-MM-DD
    date_obj = datetime.strptime(date, "%Y%m%d") + timedelta(days=date_offset)
    date = date_obj.strftime("%Y-%m-%d")
    print(f"Adjusted date: {date}")

    # Build the final directory path including the date and filter
    date_dir = os.path.join(frame_dir, f"{date} - {filter}")

    # Create the date/filter directory if it doesn't exist
    os.makedirs(date_dir, exist_ok=True)

    # Copy the file to the appropriate directory. Do not overwrite if it already exists.
    src_path = os.path.join(filepath)
    dst_path = os.path.join(date_dir, filename)
    if not os.path.exists(dst_path):
      shutil.copy2(src_path, dst_path)

      # If the file is not mono, update the FITS header with the filter name
      if not is_mono:
        with fits.open(dst_path, mode='update') as hdul:
          hdul[0].header['FILTER'] = filter
          hdul.flush()

      
