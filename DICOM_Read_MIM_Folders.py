import SimpleITK as sitk
import os
import datetime         # Used for date_time stamp in output file
import tkinter as tk    # Library for user input dialog
from tkinter import filedialog
from tkinter import messagebox
import csv              # Library used to write DICOM header informationto CSV file
import json             # Library for cURL
import requests         # Library for cURL
import pydicom          # Library for reading DICOM files
import shutil
from natsort import natsorted

## This script processes a folder of L3 single-slice DICOM files stored in nested folders
##    DICOM files are read and metadata extracted. Files are then collected into an L3 folder
##    Which is then read for reading with AutoMATiCA

## Input is a folder of L3 DICOMS
## ... which is contained within a folder with the patients name
## ... which is contained wtihin a folder with the Year and Month = "Monthly"
## ...... "Monthly" folder is generated by MIM_Vista
## ... which is contained within a "day" folder eg "DICOM 0720" = "Workday"
## ...... "Workday" folders are used to collect a day's work of identifying L3"
## ... which is contained within a folder eg "DICOM_Folder"  = "Collection"
## Output is a metadata files

def choose_dicom_directory():   # User Dialog to choose location of DICOM_XXX folder
    root = tk.Tk()
    root.withdraw()
    dicom_path = filedialog.askdirectory(title='Choose Location of superset folder containg nested folders from MIM Vista')
    return dicom_path

def choose_output_directory():  # User dialog to choose location of L3 (results) folder
    root = tk.Tk()
    root.withdraw()
    output_directory = filedialog.askdirectory(title='Choose folder containing the L3 folder, which will house the collected DICOMs')
    return output_directory

def is_dicom_file(file_path):   # Tests whether a file path correspoinds to a valid DICOM file
    try:
        pydicom.dcmread(file_path)
        return True
    except pydicom.errors.InvalidDicomError:
        return False





## User input chooses dicom_folder and output_folder
dicom_folder = choose_dicom_directory()
output_folder = choose_output_directory()

#dicom_folder = 'E:/CancerNutrition_MIMs_E'
#output_folder = 'E:/CancerNutrition_MIMs_E'

comments='Wednesday evening 8/16 swapping Patient ID and Accession'


messagebox.showinfo(title="Read_MIM_Folders", message="This script reads a directory of which contains daily work folders containing monthly MIM folders containing patient foolders containing single DICOM slices")



## Determine whether there is a folder "L3" inside of the dicom_folder
l3_folder_path = os.path.join(dicom_folder, "L3")
if not os.path.exists(l3_folder_path):
    os.makedirs(l3_folder_path)

## Determine whether there is a folder "metadata" inside of the LICOM
metadata_folder_path = os.path.join(l3_folder_path, "metadata")
if not os.path.exists(metadata_folder_path):
    os.makedirs(metadata_folder_path)

def generate_filename():
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d")
    filename = f"dicom_l3_metadata_{formatted_datetime}.csv"
    return filename

def generate_errorfile():
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d")
    efilename = f"dicom_l3_errors_{formatted_datetime}.csv"
    return efilename

## Create dicom_metadata .CSV file and write headers
dicom_metadata_filename = generate_filename()
dicom_metadata_path = os.path.join(output_folder,'L3','metadata',dicom_metadata_filename)
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


def read_monthly_folder_test(day_path):
    for month_folder  in os.listdir(day_path): # Iterate through monthly folders in DICOM_XXX folder
        month_folder_path=os.path.join(day_path,month_folder)
        if month_folder=='L3':  # Do not read files inside L3 folder
            continue
        if month_folder=='temp': # Do not read files inside temp folder
            continue
        if os.path.isdir(month_folder_path): # Read the contents of month_folder it it is a valid directory
            for patient_folder in os.listdir(month_folder_path): # Read contents of patient_folder inside month_folder
                patient_path = os.path.join(day_path,month_folder,patient_folder)
                #print(f"Patient Folder: {patient_path}")



def read_monthly_folder(day_path,day_folder):
    for month_folder  in os.listdir(day_path): # Iterate through monthly folders in DICOM_XXX folder
        month_folder_path=os.path.join(day_path,month_folder)
        skip_array = ['L3','temp','TIFF','inner','mask','outer','subq','temp','train','visceral','wall','quarantine','overlay','raw CT scan','segmentation map']
        if month_folder in skip_array:  # skip folders which appear on the skip list
            continue
        if os.path.isdir(month_folder_path): # Read the contents of month_folder it it is a valid directory
            for patient_folder in os.listdir(month_folder_path): # Read contents of patient_folder inside month_folder
                if patient_folder in skip_array:  # skip folders which appear on the skip list
                    continue
                patient_path = os.path.join(day_path,month_folder,patient_folder)
                print(f"Patient Folder: {patient_path}")
                dicom_list = os.listdir(patient_path)
                dicom_file_path = os.path.join(patient_path, dicom_list[0])
                print(f"DICOM file path: {dicom_file_path}")
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
                try:
                    thickness=dicom_file.SliceThickness
                except AttributeError:
                    thickness=0
                rows=dicom_file.Rows
                columns=dicom_file.Columns
                pixel_spacing=dicom_file.PixelSpacing
                if rows != 512 | columns !=512:
                    print(f"Rejecting non-standard size DICOM file: {patient_path}")
                    continue

                csv_file = open(dicom_metadata_path, "a", newline="")
                writer = csv.writer(csv_file)
                writer.writerow([patient_name, patient_id,birth_date,sex,age,height,weight,bmi,study_date, series,manufacturer, modality,
                                 sop_instance_uid,accession, institution, study_desc,model,ethnic,thickness,series_instance_uid,
                                 study_instance_uid, rows,columns,pixel_spacing,"","","","",day_folder,month_folder,""])
                csv_file.close()
                ### Need to change
                print(f"dicom_file_path: {dicom_file_path}")
                dsl3 = pydicom.read_file(dicom_file_path)
                dsl3.PatientID = accession
                dsl3.AccessionNumber = patient_id  
                new_l3_path = os.path.join(l3_folder_path, dicom_list[0])
                #print(f"new_l3_path: {new_l3_path}")
                dsl3.save_as(new_l3_path)
                ##  Old script: used copy function
                #l3_file_path = os.path.join(l3_folder_path,dicom_list[0])
                #print(f"le_file_path: {l3_file_path}")
                #shutil.copy2(dicom_file_path, l3_file_path)
                continue


csv_file.close()
ecsv_file.close()


for day_folder in os.listdir(dicom_folder):
        # Construct the full path of the item
        day_path = os.path.join(dicom_folder, day_folder)
        # Check if the item is a file or a folder
        if os.path.isdir(day_path):
            # If it's a folder, recursively call the copy_files function with the new source and destination folders
            read_monthly_folder(day_path,day_folder)