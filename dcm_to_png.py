'''
Convert dcm image to png format
'''
import os
import png
import dicom
import shutil
def dcm_to_png(dcm_file, png_file):
    ''' Function to convert from a DCM image to png
        @param dcm_file: An opened file like object to read te dicom data
        @param png_file: An opened file like object to write the png data
    '''

    # Extracting data from the dcm file
    plan = dicom.read_file(dcm_file)
    shape = plan.pixel_array.shape

    image_2d = []
    max_val = 0
    for row in plan.pixel_array:
        pixels = []
        for col in row:
            pixels.append(col)
            if col > max_val: max_val = col
        image_2d.append(pixels)

    # Rescaling grey scale between 0-255
    image_2d_scaled = []
    for row in image_2d:
        row_scaled = []
        for col in row:
            col_scaled = int((float(col) / float(max_val)) * 255.0)
            row_scaled.append(col_scaled)
        image_2d_scaled.append(row_scaled)

    # Writing the PNG file
    w = png.Writer(shape[1], shape[0], greyscale=True)
    w.write(png_file, image_2d_scaled)


def convert_file(dcm_file_path, png_file_path):
    ''' Function to convert an dcm binary file to a PNG image file.
        @param dcm_file_path: Full path to the dcm file
        @param png_file_path: Full path where the png files will be saved
    '''

    # Making sure that the dcm file exists
    if not os.path.exists(dcm_file_path):
        raise Exception('File "%s" does not exists' % dcm_file_path)

    # Making sure the png file does not exist
    if os.path.exists(png_file_path):
        raise Exception('File "%s" already exists' % png_file_path)

    dcm_file = open(dcm_file_path, 'rb')
    png_file = open(png_file_path, 'wb')

    dcm_to_png(dcm_file, png_file)

    png_file.close()


def convert_folder(dcm_folder, png_folder):
    '''
    Convert all dcm files in a folder to png files in a destination folder
    '''
    # Create the folder for the pnd directory structure
    if  os.path.exists(png_folder):
        shutil.rmtree(png_folder)
        os.makedirs(png_folder)
    else:
        os.makedirs(png_folder)

    # Recursively traverse all sub-folders in the path
    for dcm_sub_folder, subdirs, files in os.walk(dcm_folder):
    
        for dcm_file in os.listdir(dcm_sub_folder):
            dcm_file_path = os.path.join(dcm_sub_folder, dcm_file)

            # Make sure path is an actual file
            if os.path.isfile(dcm_file_path) and '.dcm' in dcm_file_path:

                #get patient ID and check their PD status
                rel_path = os.path.relpath(dcm_sub_folder, dcm_folder)
                png_folder_path = os.path.join(png_folder, rel_path)

                if not os.path.exists(png_folder_path):
                    os.makedirs(png_folder_path)
                png_file_path = os.path.join(png_folder_path, '%s.png' % dcm_file)

                try:
                    # Convert the actual file
                    convert_file(dcm_file_path, png_file_path)

                    print ('SUCCESS>', dcm_file_path, '-->', png_file_path)

                except Exception as e:
                    print ('FAIL>', dcm_file_path, '-->', png_file_path, ':', e)



convert_folder('dcm_folder', 'png_folder') 
