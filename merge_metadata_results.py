
## This script performs an inner join between the DICOM metadata file and the Automatica results file 
## the result is a csv file which contains additional information from the DICOM headers (such as patient name)

## The two files are joined on the SOP Instance UID which is unique for the slice. This is read directly by the metadata script 
##   and is available in the results Excel file as it is incorporated into the file name

import pandas as pd     # Pandas for dataframe manipulation
import os               # Used to construct path names
import datetime         # Used for date_time stamp in output file

import tkinter as tk    # Provides graphical user interface with dialog box
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo

def perform_inner_join(csv_file, excel_file, csv_column1, excel_column1, save_path):
    # Read the CSV file (which contains metadata extracted from the DICOM headers)
    df_csv = pd.read_csv(csv_file)

    # Read the Excel file (which contains results from the AutoMATiCA ML algorithm)
    df_results = pd.read_excel(excel_file)
    df_results['results_uid'] = df_results['Scan folder'].apply(extract_uid)

    # Perform the inner join on the common columns (SOP UID) which uniquely identify each scan
    df_merged_metada_results = pd.merge(df_csv, df_results, left_on=[csv_column1], right_on=[excel_column1], how='inner')

    # Save the result as a new CSV file
    save_file_name = generate_filename()
    output_file = os.path.join(save_path,save_file_name)
    df_merged_metada_results.to_csv(output_file, index=False)
    print(f"Inner join result saved to {output_file}")


def extract_uid(dicom_path):
    
     # Split the location string by '\' and return the last element (after the last '\')
    dicom_path_strip = dicom_path[:-4]
    return dicom_path_strip.rsplit('\\', 1)[-1]


def generate_filename():
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d")
    filename = f"merged_metadata_results_{formatted_datetime}.csv"
    return filename


if __name__ == "__main__":
    # Provide file paths and common column names
    metadata_file_path  = fd.askopenfilename(initialdir="E:", title="Select DICOM Metadata file",filetypes=(("CSV", "*.csv"),("all files", "*.*")))
    results_file_path = fd.askopenfilename(initialdir="E:", title="Select Results file from AutoAMTiCA", filetypes=(("EXCEL", "*.xlsx"),("all files", "*.*")))
    metadata_common_column1 = "SOP Instance UID"  # Unique slice identifier extracted by metadata script
    results_common_column1 = "results_uid" # Unique slice identifier which had been incorporated into file name (and was captured by AutoMATiCA)
    
    output_csv_path = fd.askdirectory(initialdir="E:", title="Location to Save Merged Metadata + Results File")

    # Call the function to perform the inner join and save the result
    perform_inner_join(metadata_file_path, results_file_path, metadata_common_column1, results_common_column1, output_csv_path)
