# ImageJ Scripts

## Adjust Segmentation

Reads a single folder which contains L3 DICOM files (containing a single image)

## DICOM_Read_MIM_Folders

1 - Reads an enclosing collection folder which contains: 

- workday folders (eg MIM_0804), which are represent files pulled on a given day, which in turn contain:
- monthly folders created by MIM Vista (eg 2016_January)
- Patient folders (Jones^^Albert^^Franklin...)

2 - Opens each DICOM file to confirm that it can be read

3 - Confirms that each DICOM file is 512x512

4 - Creates a copy of the DICOM which moves Accession Number into the Patient ID position.  
This is done because AutoMATiCA stores mask images according to Patient ID.  
If there are duplicates of Patient ID, the algorithm will append characters to the end of the file name.  
The accession number is more likely to be unique.

5 - Saves copies of single-slice DICOM files into a folder "L3" which is inside the enclosing collection folder 

6 - Creates a *metadata* folder inside the *L3* folder
- Saves a metadata file with date stamp  *dicom_l3_metadata_2023-08-16.csv*
- Saves an error file with date stamp  *dicom_l3_metadata_2023-08-16.csv*




## DICOM_Read_Stacks.py

This script processes a folder of  DICOM stacks stored in nested folders  
    DICOM files are read and metadata extracted  
    DICOM stacks are converted to NifTI files and stored in temp folder  
    NifTI files are uploaded to a docker server running sarcopenia-ai, which will identify the L3 slide  
    L3 slice number from sarcopenia-ai is used to select the L3 slice from the original DICOM stack  
    L3 slices are collected in the L3 folder for subsequent reading with AutoMATiCA  

Calls localhost:5000/predict 
- Requires a running Docker instance of sarcopenia-ai
- Uses the saropenia-ai Imperial College London script to identify L3

Input is a DICOM stack,
... which is contained within a folder with the patients name
... which is contained wtihin a folder with the Year and Month
... which is contained within a "workday" folder eg "DICOM 0720"
... which is contained within an enclosing folder eg "DICOM Stacks"
Final L3 DICOM images (single-slice) are stored in L3 folder
temp folder is used for Nifti files



# Directory Structure

## Single-slice (*MIM_*) Directory Structure
```
Enclosing Folder eg *Cancer_NutritionMIM*
├── L3
│   |── overlay
│   │   ├── AutoMATiCA overlay images eg *08-449870.png*
│   |── raw CT scan
│   │   ├── AutoMATiCA raw CT images eg *08-449870.png*
│   |── segmentation map
│   │   ├── AutoMATiCA raw CT images eg *08-449870.png*
│   |── metadata
│   │   ├── DICOM header errors *dicom_l3_errors_2023-08-16.csv*
│   │   ├── DICOM header metadata *dicom_l3_metadata_2023-08-16.csv*
│   │   ├── DICOM outliers ("rejects") flagged for re-reading *rejects_2023-08-18.csv*
│   │   ├── AutoMATiCA Results *Results - Wed Aug 16 23-46-55 2023.xlsx*
│   │   ├── ImageJ re-reading Results *reread_results.csv*
│   │   ├── Merged Data from AutoMATiCA + DICOM Results *merged_metadata_results_2023-08-18.csv*
│   |── single-slice collected DICOM files...  *08-37784953.dcm*
│   |── single-slice collected DICOM files...  *100CT38749403458.dcm*
├── Workday folder eg *MIM_0214*
│   |── Monthly folder eg *2007-04_Studies*
│   │   ├── Patient folder eg *Jones^^Albert^^Franklin...*
│   │   │   ├── DICOM file (single slice) *2.16.840.224363.2.354664.dcm*
├── Workday folder eg *MIM_0301*
│   |── Monthly folder eg *2016-07_Studies*
│   │   ├── Patient folder eeg *Fraser^^Milton^^Franklin...*
│   │   │   ├── DICOM file (single slice) *1.20.240.66753.7.000239.dcm*
└── Workday folders...
```

## Image Stack (*DICOM_*) Directory Structure
