import os
import subprocess
import sys


input_dir = '/files/data/imagesBookshelf' # The directory of the images to to use 
output_dir = '/files/data' # The directory of the script output
camera_file_params = '/files/openMVG/src/openMVG/exif/sensor_width_database/sensor_width_camera_database.txt' # The diectory of the database file with sensor widths

matches_dir = os.path.join(output_dir, 'matches')
reconstruction_dir = os.path.join(output_dir, 'reconstruction')

if not os.path.exists(output_dir):
  os.mkdir(output_dir)
if not os.path.exists(matches_dir):
  os.mkdir(matches_dir)
if not os.path.exists(reconstruction_dir):
  os.mkdir(reconstruction_dir)

print ('1. Intrinsics analysis')
command = [
    'openMVG_main_SfMInit_ImageListing',
    '-i', input_dir,
    '-o', matches_dir,
    '-d', camera_file_params
]
result = subprocess.run(command, text=True, check=True)

print ('\n2. Compute features')
command = [
    'openMVG_main_ComputeFeatures',
    '-i', matches_dir+'/sfm_data.json', 
    '-o', matches_dir, 
    '-m', 'SIFT'
]
result = subprocess.run(command, text=True, check=True)

print ("\n3. Compute matching pairs")
command = [
    'openMVG_main_PairGenerator',
    "-i", matches_dir+"/sfm_data.json", 
    "-o" , matches_dir + "/pairs.bin"
]
result = subprocess.run(command, text=True, check=True)

print ("\n4. Compute matches")
command = [
    'openMVG_main_ComputeMatches',
    "-i", matches_dir+"/sfm_data.json", 
    "-p", matches_dir+ "/pairs.bin", 
    "-o", matches_dir + "/matches.putative.bin"
]
result = subprocess.run(command, text=True, check=True)

print ("\n5. Filter matches" )
command = [
    'openMVG_main_GeometricFilter',
    "-i", matches_dir+"/sfm_data.json", 
    "-m", matches_dir+"/matches.putative.bin" , 
    "-g" , "f" , 
    "-o" , matches_dir+"/matches.f.bin"
]
result = subprocess.run(command, text=True, check=True)

print ("\n6. Do Sequential/Incremental reconstruction")
command = [
    'openMVG_main_SfM',
    "--sfm_engine", "INCREMENTAL", 
    "-i", matches_dir+"/sfm_data.json", 
    "-m", matches_dir, 
    "-o", reconstruction_dir
]
result = subprocess.run(command, text=True, check=True)

print ("\n7. Colorize Structure")
command = [
    'openMVG_main_ComputeSfM_DataColor',
    "-i", reconstruction_dir+"/sfm_data.bin", 
    "-o", reconstruction_dir+"/colorized.ply"
]
result = subprocess.run(command, text=True, check=True)

print ("\n8. Store the data as JSON file")
command = [
    'openMVG_main_ConvertSfM_DataFormat',
    "-i", reconstruction_dir+"/sfm_data.bin", 
    "-o", reconstruction_dir+"/sfm_data.json"
]
result = subprocess.run(command, text=True, check=True)
