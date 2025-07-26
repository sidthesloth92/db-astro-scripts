import os
from datetime import datetime, timedelta
import shutil
import sys

if len(sys.argv) < 2:
  print("Usage: python split_by_date.py <directory_path>")
  sys.exit(1)

directory_path = sys.argv[1]

fits_files = []
for root, _, files in os.walk(directory_path):
  for file in files:
    if file.endswith('.fit') and not file.startswith('.'):
      fits_files.append(os.path.join(root, file))


for filepath in fits_files:
  filename = os.path.basename(filepath)


  if not filename.startswith('.') and filename.endswith('.fit'):
    
    print(f"\nProcessing file: {filename}")

    parts = filename.split('_')

    frame_type = parts[0]

    is_calibration_frame = False
    if frame_type in ["Flat", "Dark", "Bias"]:
      is_calibration_frame = True
  
    is_mono = False   
    if parts[5] in ['L', 'R', 'G', 'B', 'Ha', 'OIII', 'SII', 'H', 'O', 'S']:
      is_mono = True

    print(f"Is Calibration Frame: {is_calibration_frame} Is Mono: {is_mono}")

    if is_calibration_frame:
      target_name = "_Calibration Frames"
      camera_model = parts[3]
      filter = parts[4] if is_mono else "No_Filter"
      date = parts[5].split('-')[0]  # e.g., '20250721'
      time = parts[5].split('-')[1]
    else:
      offset = 0 if is_mono else -1

      target_name = parts[1]
      camera_model = parts[4]
      filter = parts[5] if is_mono else parts[len(parts) - 1].split(".")[0]  # Last part for color images
        
      date = parts[7 + offset].split('-')[0]  # e.g., '20250721'
      time = parts[7 + offset].split('-')[1]  # e.g., '012502'
   
    print(f"Frame Type: {frame_type}, Target Name: {target_name}, Camera Model: {camera_model}, Filter: {filter} Date: {date}, Time: {time}")
    
    if len(sys.argv) >= 3:
      output_dir = os.path.abspath(sys.argv[2])
    else:
      output_dir = os.path.join(os.getcwd(), 'output')

    camera_dir = os.path.join(output_dir, camera_model)
    target_dir = os.path.join(camera_dir, target_name)
    frame_dir = os.path.join(target_dir, frame_type)

    os.makedirs(frame_dir, exist_ok=True)

    date_offset = 0 if int(time) < 160000 else 1

    date_obj = datetime.strptime(date, "%Y%m%d") + timedelta(days=date_offset)
    date = date_obj.strftime("%Y-%m-%d")
    print(f"Adjusted date: {date}")

    date_dir = os.path.join(frame_dir, f"{date} - {filter}")

    os.makedirs(date_dir, exist_ok=True)

    src_path = os.path.join(filepath)
    dst_path = os.path.join(date_dir, filename)
    if not os.path.exists(dst_path):
      shutil.copy2(src_path, dst_path)

      if not is_mono:
        with fits.open(dst_path, mode='update') as hdul:
          hdul[0].header['FILTER'] = filter
          hdul.flush()

      
