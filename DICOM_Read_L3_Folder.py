import SimpleITK as sitk
import os
import datetime         # Used for date_time stamp in output file
import tkinter as tk    # Library for user input dialog
from tkinter import filedialog
import csv              # Library used to write DICOM header informationto CSV file
import json             # Library for cURL
import requests         # Library for cURL
import pydicom          # Library for reading DICOM files
from natsort import natsorted


## This script processes a folder of  DICOM files stored in a single folder
##    DICOM files are read and metadata extracted
##    Metadata is written to a file

## Folder names "Monthly" and "Workday" are irrelevant.

def choose_dicom_directory():   # User Dialog to choose location of DICOM folder
    root = tk.Tk()
    root.withdraw()
    dicom_path = filedialog.askdirectory(title='Choose Location of DICOM folder to read. Note that this folder should contain DICOM files without subfolders')
    return dicom_path

def choose_output_directory():  # User dialog to choose location of L3 (results) folder
    root = tk.Tk()
    root.withdraw()
    output_directory = filedialog.askdirectory(title='Choose Location metadata folder')
    return output_directory

def is_dicom_file(file_path):   # Tests whether a file path correspoinds to a valid DICOM file
    try:
        pydicom.dcmread(file_path)
        return True
    except pydicom.errors.InvalidDicomError:
        return False


comments='comments here'

## User input chooses dicom_folder and output_folder
dicom_folder = choose_dicom_directory()
output_folder = choose_output_directory()

#dicom_folder = 'E:/DICOM_Stacks_E'
#output_folder = "E:/DICOM_Stacks_E"



def generate_filename():
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d")
    filename = f"dicom_folder_metadata_{formatted_datetime}.csv"
    return filename

def generate_errorfile():
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d")
    efilename = f"dicom_folder_errors_{formatted_datetime}.csv"
    return efilename

## Create dicom_metadata .CSV file and write headers
dicom_metadata_filename = generate_filename()
dicom_metadata_path = os.path.join(output_folder,dicom_metadata_filename)
csv_file = open(dicom_metadata_path, "w", newline="")
writer = csv.writer(csv_file)

writer.writerow(["Patient Name","Patient ID","Birth Date","Sex","Age" ,"Height","Weight","BMI","Study Date", "Series","Manufacturer", "Modality","SOP Instance UID",
                 "Accession","Institution","Description","Model","Ethnic","Thickenss","Series Instance UID",
                 "Study Instance UID","rows","columns","pixel_spacing","Slice Z","Area","Attenuation","Slice_Prob","Workday","Monthly",dicom_folder,comments])
## Create dicom_errors .CSV file and write headers
dicom_error_filename = generate_errorfile()
dicom_error_path = os.path.join(output_folder,'L3',dicom_error_filename)
ecsv_file = open(dicom_error_path, "w", newline="")
ewriter = csv.writer(ecsv_file)
ewriter.writerow(["Path"]) 


def read_monthly_folder1(day_path):
    for month_folder  in os.listdir(day_path): # Iterate through monthly folders in DICOM_XXX folder
        month_folder_path=os.path.join(day_path,month_folder)
        if month_folder=='L3':  # Do not read files inside L3 folder
            continue
        if month_folder=='temp': # Do not read files inside temp folder
            continue
        if os.path.isdir(month_folder_path): # Read the contents of month_folder it it is a valid directory
            for patient_folder in os.listdir(month_folder_path): # Read contents of patient_folder inside month_folder
                patient_path = os.path.join(day_path,month_folder,patient_folder)
                print(f"Patient Folder: {patient_path}")



def read_monthly_folder(day_path):
    for month_folder  in os.listdir(day_path): # Iterate through monthly folders in DICOM_XXX folder
        month_folder_path=os.path.join(day_path,month_folder)
        if month_folder=='L3':  # Do not read files inside L3 folder
            continue
        if month_folder=='temp': # Do not read files inside temp folder
            continue
        if os.path.isdir(month_folder_path): # Read the contents of month_folder it it is a valid directory
            for patient_folder in os.listdir(month_folder_path): # Read contents of patient_folder inside month_folder
                patient_path = os.path.join(day_path,month_folder,patient_folder)
                print(f"Patient Folder: {patient_path}")
                dicom_list = natsorted(os.listdir(patient_path))
                dicom_file_path = os.path.join(patient_path, dicom_list[0])

                if not is_dicom_file(dicom_file_path): # Tests file using the is_dicom_file function to verity it is valid DICOM
                    print(f"Skipping non-DICOM file: {dicom_file_path}")
                    continue            
                dicom_file = pydicom.dcmread(dicom_file_path)
                patient_name = dicom_file.PatientName
                patient_id = dicom_file.PatientID
                birth_date=dicom_file.PatientBirthDate
                sex=dicom_file.PatientSex
                try:
                    age=dicom_file.PatientAge
                except AttributeError:
                    age=''
                study_date = dicom_file.StudyDate
                series=dicom_file.SeriesNumber
                manufacturer = dicom_file.Manufacturer
                modality = dicom_file.Modality
                series_instance_uid=dicom_file.SeriesInstanceUID # One digit less than first slice. Uniquely identifies the series
                study_instance_uid=dicom_file.StudyInstanceUID #  Uniquely identifies the study (which includes multiple series)
                sop_instance_uid=dicom_file.SOPInstanceUID # Uniquely identifies the L3 image
                accession=dicom_file.AccessionNumber
                institution=dicom_file.InstitutionName
                study_desc=dicom_file.StudyDescription
                try:
                    model=dicom_file.ManufacturerModelName
                except AttributeError:
                    model=''
                try:
                    weight=dicom_file.PatientWeight
                except AttributeError: 
                    weight=''
                try:
                    height=dicom_file.PatientSize
                except AttributeError: 
                    height=''
                try:
                    bmi=dicom_file.PatientBodyMassIndex
                except AttributeError: 
                    bmi=''
                try:
                    ethnic=dicom_file.EthnicGroup
                except AttributeError: 
                    ethnic=''
                thickness=dicom_file.SliceThickness
                rows=dicom_file.Rows
                columns=dicom_file.Columns
                pixel_spacing=dicom_file.PixelSpacing
                if rows != 512 | columns !=512:
                    print(f"Rejecting non-standard size DICOM file: {patient_path}")
                    continue

                nifti_file_name = dicom_list[0] +'.nii.gz'

                output_path_nii = os.path.join(output_folder,'temp',nifti_file_name)

                ##print(f"Processed DICOM file: {dicom_file_path}")


                #print("DICOM Headers:")
               #for element in dicom_file:
                #    print(element)
    

                reader = sitk.ImageSeriesReader()
                dicom_names = reader.GetGDCMSeriesFileNames(patient_path)
                reader.SetFileNames(dicom_names)
                image = reader.Execute()

                ## XXXXXX # Added a call to PermuteAxes to change the axes of the data
                ## XXXXXZ image = sitk.PermuteAxes(image, [2, 1, 0])

                ## Flip image vertically
                image=sitk.Flip(image,[False,False,True])

                sitk.WriteImage(image, output_path_nii)
                files = {
                    'image': open(output_path_nii, 'rb'),
                }
                response = requests.post('http://localhost:5000/predict', files=files)

                try:
                    results_dict=json.loads(response.content)
                except json.errors.JSONDecodeError:
                    print(f"line 172 JSONDecodeError: {patient_path}")
                    continue
                except ValueError:
                    print(f"line 175 ValueError: {patient_path}")
                    continue
                except JSONDecodeError:
                    print(f"line 178 JSONDecodeError: {patient_path}")
                    continue

                #results_dict=json.loads(response.content)
                print("results_dict:",results_dict)
                if results_dict['success']:  
                    slice_predict= results_dict['prediction']['slice_z']
                    muscle_atten = results_dict['prediction']['muscle_attenuation']
                    muscle_area = results_dict['prediction']['muscle_area']
                    slice_z = results_dict['prediction']['slice_z']
                    slice_prob = results_dict['prediction']['slice_prob']
                    ## Numeric (integer) variable corresponds to L3 slice number
                    slice_number = int(slice_predict)
                    print("dicom_list[0]:", dicom_list[0])

                    print("dicom_list[slice_predict]:", dicom_list[slice_number])
                    l3_dicom_input_path = os.path.join(patient_path, dicom_list[slice_number])
                    l3_dicom_file = pydicom.dcmread(l3_dicom_input_path )
                    sop_instance_uid=l3_dicom_file.SOPInstanceUID # Uniquely identifies the L3 image
                    l3_dicom_file_name = sop_instance_uid+ '.dcm'
                    #print("l3_dicom_file_name:", l3_dicom_file_name)
                    l3_dicom_output_path = os.path.join(l3_folder_path,l3_dicom_file_name)

                    print("l3_dicom_input_path:", l3_dicom_input_path)
                    ######################################################
                    ##  Edit here to put a uniqiue identifier in the Patient ID field 
                    ##  Maybe accession number?
                    ##  This could make it possible to easily positively identify Automatica segmentation images
                    ##  Which currently use Patient ID in the name, but this is a challenge where more than one
                    ##  film is read per patient

                    
                    dsl3 = pydicom.read_file(l3_dicom_input_path)
                    dsl3.PatientID = accession
                    dsl3.save_as(l3_dicom_output_path)
                    ##  Old script: used copy function
                    ## os.system(f'copy "{l3_dicom_input_path}" "{l3_dicom_output_path}"')

                    ######################################################


                    csv_file = open(dicom_metadata_path, "a", newline="")
                    writer = csv.writer(csv_file)
                    writer.writerow([patient_name, patient_id,birth_date,sex,age,height,weight,bmi,study_date, series,manufacturer, modality,
                                 sop_instance_uid,accession, institution, study_desc,model,ethnic,thickness,series_instance_uid,
                                 study_instance_uid, rows,columns,pixel_spacing,slice_z,muscle_area,muscle_atten,slice_prob])
                    csv_file.close()
                    continue
                else:
                    print(f"SKIPPED DICOM file: {dicom_file_path}")
                    ecsv_file = open(dicom_error_path, "a", newline="")
                    ewriter = csv.writer(ecsv_file)
                    ewriter.writerow([dicom_file_path])
                    ecsv_file.close()
                    continue

csv_file.close()
ecsv_file.close()


for day_folder in os.listdir(dicom_folder):
        # Construct the full path of the item
        day_path = os.path.join(dicom_folder, day_folder)
        # Check if the item is a file or a folder
        if os.path.isdir(day_path):
            # If it's a folder, recursively call the copy_files function with the new source and destination folders
            read_monthly_folder(day_path)