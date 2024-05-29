import os
import subprocess
import sys

# Set the directory paths
input_dir = '/files/data/imagesBookshelf'  # Directory containing the input images
output_dir = '/files/data'  # Directory for storing the script's output
camera_file_params = '/files/data/sensor_width_camera_database.txt'  # Path to the camera sensor width database file

# Define the directories for matches and reconstruction
matches_dir = os.path.join(output_dir, 'matches')
reconstruction_dir = os.path.join(output_dir, 'reconstruction')

# Create directories if they do not exist
if not os.path.exists(output_dir):
    os.mkdir(output_dir)
if not os.path.exists(matches_dir):
    os.mkdir(matches_dir)
if not os.path.exists(reconstruction_dir):
    os.mkdir(reconstruction_dir)

# Step 1: Intrinsics analysis
print('1. Intrinsics analysis')
command = [
    'openMVG_main_SfMInit_ImageListing',  # Command for image listing
    '-i', input_dir,  # Input directory
    '-o', matches_dir,  # Output directory for matches
    '-d', camera_file_params  # Camera database file
]
result = subprocess.run(command, text=True, check=True)

# Step 2: Compute features
print('\n2. Compute features')
command = [
    'openMVG_main_ComputeFeatures',  # Command for computing features
    '-i', matches_dir + '/sfm_data.json',  # Input data
    '-o', matches_dir,  # Output directory
    '-m', 'SIFT'  # Feature extraction method
]
result = subprocess.run(command, text=True, check=True)

# Step 3: Compute matching pairs
print('\n3. Compute matching pairs')
command = [
    'openMVG_main_PairGenerator',  # Command for generating pairs
    '-i', matches_dir + '/sfm_data.json',  # Input data
    '-o', matches_dir + '/pairs.bin'  # Output pairs file
]
result = subprocess.run(command, text=True, check=True)

# Step 4: Compute matches
print('\n4. Compute matches')
command = [
    'openMVG_main_ComputeMatches',  # Command for computing matches
    '-i', matches_dir + '/sfm_data.json',  # Input data
    '-p', matches_dir + '/pairs.bin',  # Input pairs file
    '-o', matches_dir + '/matches.putative.bin'  # Output matches file
]
result = subprocess.run(command, text=True, check=True)

# Step 5: Filter matches
print('\n5. Filter matches')
command = [
    'openMVG_main_GeometricFilter',  # Command for filtering matches
    '-i', matches_dir + '/sfm_data.json',  # Input data
    '-m', matches_dir + '/matches.putative.bin',  # Input matches file
    '-g', 'f',  # Geometric filter type
    '-o', matches_dir + '/matches.f.bin'  # Output filtered matches file
]
result = subprocess.run(command, text=True, check=True)

# Step 6: Sequential/Incremental reconstruction
print('\n6. Do Sequential/Incremental reconstruction')
command = [
    'openMVG_main_SfM',  # Command for Structure from Motion (SfM)
    '--sfm_engine', 'INCREMENTAL',  # SfM engine type
    '-i', matches_dir + '/sfm_data.json',  # Input data
    '-m', matches_dir,  # Input matches directory
    '-o', reconstruction_dir  # Output reconstruction directory
]
result = subprocess.run(command, text=True, check=True)

# Step 7: Colorize Structure
print('\n7. Colorize Structure')
command = [
    'openMVG_main_ComputeSfM_DataColor',  # Command for colorizing the structure
    '-i', reconstruction_dir + '/sfm_data.bin',  # Input data
    '-o', reconstruction_dir + '/colorized.ply'  # Output colorized file
]
result = subprocess.run(command, text=True, check=True)

# Step 8: Store the data as JSON file
print('\n8. Store the data as JSON file')
command = [
    'openMVG_main_ConvertSfM_DataFormat',  # Command for converting data format
    '-i', reconstruction_dir + '/sfm_data.bin',  # Input data
    '-o', reconstruction_dir + '/sfm_data.json'  # Output JSON file
]
result = subprocess.run(command, text=True, check=True)