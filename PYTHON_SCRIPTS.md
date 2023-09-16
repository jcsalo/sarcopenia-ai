# Python Scripts

## DICOM_Read_L3_Folder

Reads a single folder which contains L3 DICOM files (containing a single image)

## DICOM_Read_MIM_Folders

Reads a collection folder which contains: 

- workday folders (eg MIM_0804), which in turn contain:
- monthly folders created by MIM Vista (eg 2016_January)
- Patient folders (Jones^^Albert^^Franklin...)

Opens each DICOM file to confirm that it can be read

Confirms that each DICOM file is 512x512

Creates a copy of the DICOM which moves Accession Number into the Patient ID position. This is done because AutoMATiCA stores mask images according to Patient ID.  If there are duplicates of Patient ID, the algorithm will append characters to the end of the file name. The accession number is more likely to be unique.

Collects copies of DICOM files into a folder "L3".  

Saves a metadata file with date stamp

Saves a error file with date stamp

