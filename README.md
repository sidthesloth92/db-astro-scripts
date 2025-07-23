# Group By Date Script

## Overview

This script organizes FITS image files that come out of ASIAIR into a structured folder hierarchy based on metadata extracted from their filenames. It groups files by camera model, target name, frame type, date, and filter. This script is particularly useful for astrophotography enthusiasts who need to manage large datasets of images.

## ASIAIR Instructions

### When using a Filter Wheel

When using a filter wheel, ASIAIR will automatically add the filter name to the file name. Just make sure to turn on adding the camera model, gain and temperature to the file name in the settings.

### When not using a Filter Wheel

When not using a filter wheel, ASIAIR will not add filter name to the file name. Instead, you can go to camera settings and then add a suffix `_f_<filtername>`. This will allow the script to detect the filter used. Also, make sure to turn on adding the camera model, gain and temperature to the file name in the settings.

## Notes

- Files are grouped by date, with adjustments for times after 16:00:00 (considered the next day).
- Hidden files (those starting with `.`) are ignored.

## Prerequisites

This script requires **Python 3** to be installed on your system.

### Installing Python

- **Mac**:  
  Python 3 is often pre-installed on macOS. To install or update, use [Homebrew](https://brew.sh/):

  ```bash
  brew install python
  ```

- **Windows**:  
  Download and install Python from the [official Python website](https://www.python.org/downloads/). Ensure you check the box to add Python to your PATH during installation.

- **Linux**:  
  Use your package manager to install Python 3:
  ```bash
  sudo apt update
  sudo apt install python3
  ```

## How to Use the Script

### 1. Download the Script

You can obtain the script in two ways:

#### a. Download as ZIP

- Visit [https://github.com/yourusername/db-astro-scripts](https://github.com/yourusername/db-astro-scripts).
- Click the **"Code"** button and select **"Download ZIP"**.
- Extract the ZIP file to your desired location.

#### b. Clone Using Git

If you have `git` installed, you can clone the repository:

- **Mac/Linux:**

  ```bash
  git clone https://github.com/yourusername/db-astro-scripts.git
  cd db-astro-scripts
  ```

- **Windows:**
  ```cmd
  git clone https://github.com/yourusername/db-astro-scripts.git
  cd db-astro-scripts
  ```

2. **Open a terminal or command prompt in the extracted folder:**

- **Windows users:**
  - Open the folder containing the script in File Explorer.
  - Hold `Shift` and right-click inside the folder, then select **"Open PowerShell window here"** or **"Open Command window here"**.
  - Alternatively, open Command Prompt or PowerShell and use the `cd` command to navigate to the script directory. For example:
    ```cmd
    cd C:\Users\yourusername\Downloads\db-astro-scripts
    ```
- **Mac/Linux users:**
  - Open the Terminal application.
  - Use the `cd` command to navigate to the extracted folder. For example:
    ```bash
    cd ~/Downloads/db-astro-scripts
    ```

3. Run the script with the following command:
   ```bash
   python group_by_date.py <directory_path> [output_directory]
   ```
   - `<directory_path>`: The path to the directory containing the FITS files to organize.
   - `[output_directory]` (optional): The path to the output directory where the organized files will be stored. If not provided, the script will create an `output` folder in the current working directory.

### Example

Suppose you have a directory of FITS files located at `/Users/username/images` and want to organize them into `/Users/username/organized_images`. Run the following command:

```bash
python group_by_date.py /Users/username/images /Users/username/organized_images
```

> **Note:** If your folder paths contain spaces, enclose them in quotes. For example:
>
> ```bash
> python group_by_date.py "/Users/username/My Images" "/Users/username/organized images"
> ```

## Sample Input Files

Here is an example of the input files:

```
Light_Target1_20250721-012502_Camera1_L.fits
Light_Target1_20250721-162502_Camera1_R.fits
Light_Target2_20250722-012502_Camera2_Ha.fits
Light_Target2_20250722-162502_Camera2_OIII.fits
```

## Output Structure

After running the script, the files will be organized as follows:

```
organized_images/
├── Camera1/
│   ├── Target1/
│   │   ├── Light/
│   │   │   ├── 2025-07-21 - L/
│   │   │   │   └── Light_Target1_20250721-012502_Camera1_L.fits
│   │   │   ├── 2025-07-22 - R/
│   │   │       └── Light_Target1_20250721-162502_Camera1_R.fits
├── Camera2/
│   ├── Target2/
│   │   ├── Light/
│   │   │   ├── 2025-07-22 - Ha/
│   │   │   │   └── Light_Target2_20250722-012502_Camera2_Ha.fits
│   │   │   ├── 2025-07-23 - OIII/
│   │   │       └── Light_Target2_20250722-162502_Camera2_OIII.fits
```

Feel free to modify the script to suit your specific needs!
