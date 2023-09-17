# importing the tkinter module and PIL
# that is pillow module
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
from tkinter.filedialog import askdirectory
import os
from natsort import natsorted
from tkinter import ttk
import datetime         # Used for date_time stamp in output file
import csv              # Library used to write list of accession numbers of rejected scans to CSV file
from pathlib import Path


# This script allows viewing of the segmentation map folder output from AutoMATiCA

# Overall goal is to view the segmentation maps to determine which may need to be re-read

# The images in the folder are displayed serially.  Clicking the "Reject" button adds the accession number
# to a list which would then be used to direct ImageJ to re-read DICOMS corresponding to these patients.


## Output is a metadata files



comments='Read PNG images from segmentation map'





def forward(img_no):

	# GLobal variable so that we can have
	# access and change the variable
	# whenever needed
	global label
	global button_forward
	global button_back
	global button_exit
	#global button_reject
	global png_list
	global png_path
	global png_image_path
	global png_images
	global png_length
	global accession
	#label.grid(row=1, column=0, columnspan=5)
	label.grid_forget()
	#label.grid_remove()

	# This is for clearing the screen so that
	# our next image can pop up
	#label = Label(image=List_images[img_no-1]) # Original
	#label = Label(image='') # new - put start image here
	png_n_path = os.path.join(png_path, png_list[img_no]) ## seeing if global variables work
	print(f"png_n_path 54: {png_n_path}")
	accession = Path(png_n_path).stem
	print(f"accession line 56: {accession}")
	


	######################## NEWEST #######################


	image_next = ImageTk.PhotoImage(Image.open(png_n_path)) #??? not used??
	imag=Image.open(png_n_path) #### new
	im = imag.resize((768,768)) #### New
	ph=ImageTk.PhotoImage(im)
	label = Label(image=ph)
	label.image=ph
	#########################################################
	
	#label.grid(row=1, column=0, columnspan=5)
	#label.grid_remove()
	label.grid(row=1, column=0, columnspan=4)
	button_for = Button(root, text="forward",command=lambda: forward(img_no+1)) # img_no+1 as we want the next image to pop up
	no_diff =png_length-img_no
	if no_diff==1:
		button_for = Button(root, text="Forward", state=DISABLED)
	button_back = Button(root, text="Back",	command=lambda: back(img_no-1)) # img_no-1 as we want previous image when we click back
	button_reject = Button(root, text="Reject",	command=lambda: reject(accession))

	button_back.grid(row=5, column=0)
	button_exit.grid(row=5, column=1)
	button_reject.grid(row=5,column=2)
	button_for.grid(row=5, column=3)


	label.grid(row=1, column=0, columnspan=3)
	label1 = Label(text="")
	label1.grid(row=6, column=1)
	label1.grid_forget()
	label1.grid_remove()
	label1 = Label(text=accession)
	label1.grid(row=6, column=1)
	label2 = Label(text=img_no)
	label2.grid(row=6, column=0)
	label3 = Label(text=png_length)
	label3.grid(row=6, column=2)


def back(img_no):

	# We will have global variable to access these
	# variable and change whenever needed
	global label
	global button_forward
	global button_back
	global button_exit
	global png_list
	global png_path
	global png_image_path
	global png_images
	global png_length
	#label.grid_forget()

	# for clearing the image for new image to pop up
	#label = Label(image=List_images[img_no - 1])
	png_n_path = os.path.join(png_path, png_list[img_no]) ## seeing if global variables work
	######################## NEWEST #######################
	image_next = ImageTk.PhotoImage(Image.open(png_n_path))
	imag=Image.open(png_n_path)
	im=imag.resize((800,800))
	ph=ImageTk.PhotoImage(im)
	label = Label(image=ph)
	label.image=ph
	#########################################################



	accession = Path(png_n_path).stem
	print(f"accession line 122: {accession}")
	label.grid(row=1, column=0, columnspan=3)
	button_forward = Button(root, text="forward", command=lambda: forward(img_no + 1))
	button_back = Button(root, text="Back",	command=lambda: back(img_no - 1))
	#print(img_no)
	if img_no == 0: # whenever the first image will be there we will have the back button disabled
		button_back = Button(root, text="Back", state=DISABLED)
	button_reject = Button(root, text="Reject",	command=lambda: reject(accession))
	label.grid(row=1, column=0, columnspan=4)
	button_back.grid(row=5, column=0)
	button_exit.grid(row=5, column=1)
	button_reject.grid(row=5, column=2)
	button_forward.grid(row=5, column=3)
	

	# Bottom Row (Information)
	label.grid(row=1, column=0, columnspan=3)

	label1 = Label(text="")
	label1.grid(row=6, column=1)
	label1.grid_forget()
	label1.grid_remove()
	label1 = Label(text=accession)
	label1.grid(row=6, column=1)
	label2 = Label(text=img_no)
	label2.grid(row=6, column=0)
	label3 = Label(text=png_length)
	label3.grid(row=6, column=2)



def reject(accession):
	#global accession
	global reject_csv_path
	print(f"Reject: {accession}")
	with open (reject_csv_path, 'a',newline='') as csv_file:
	#csv_file = open(reject_csv_path, "a", newline="")  
		writer = csv.writer(csv_file) 
		writer.writerow([accession,'DICOM Comment',png_path,comments]) 
	csv_file.close()
	

def exit():
	print(f"Exiting: {accession}")
	csv_file.close()
	root.destroy

########################## OBSELETE##################################################
def choose_png_directory():   # User Dialog to choose location of DICOM_XXX folder
	root2 = Tk()
	root2.withdraw()
	png_path = filedialog.askdirectory(title='Choose Location of folder with PNG images')
	return png_path
#####################################################################################



def generate_reject_filename():
	current_datetime = datetime.datetime.now()
	formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H_%M_%S")
	filename = f"rejects_{formatted_datetime}.csv"
	return filename



## Dialog box to choose segmentation maps folder

def openFile():
	global png_path
	png_path = askdirectory()

root=Tk() ## TEMP
Button(root, text='Click here, choose segmentation map Folder, then close this dialog box', command=openFile).pack(fill=X) # TEMP
mainloop() # TEMP
print(f"PNG Folder: {png_path}")
l3_folder_path = os.path.dirname(png_path)
print(f"L3 Folder: {l3_folder_path}")

## Determine whether there is a folder "metadata" inside of the LICOM
metadata_folder_path = os.path.join(l3_folder_path, "metadata")
if not os.path.exists(metadata_folder_path):
    os.makedirs(metadata_folder_path)

## Create reject .CSV file and write headers
reject_filename = generate_reject_filename()
reject_csv_path = os.path.join(l3_folder_path,'metadata',reject_filename)
csv_file = open(reject_csv_path, "w", newline="")
writer = csv.writer(csv_file)
writer.writerow(["Accession Number","DICOM Comments",png_path,comments])
csv_file.close()

##########################################################
##########################################################
###################### TK ########################
# Calling the Tk (The initial constructor of tkinter)
root = Tk()
# We will make the title of our app as Image Viewer
root.title("Segmentation Map Viewer")
# The geometry of the box which will be displayed on the screen
root.geometry("900x900")

#png_list = natsorted(os.listdir(png_path))  # OLD

png_list = [ f for f in natsorted(os.listdir(png_path)) if  f[(len(f) - len('.png')):len(f)].find('png')>=0   ]
png_length = len(png_list)
#png_list = os.listdir(png_path)
png_start_path = os.path.join(png_path, png_list[0])
accession = Path(png_start_path).stem
#print(f"png_start_image: {png_start_path}")
#print(f"accession (start): {accession}")
#png_start_image = ImageTk.PhotoImage(Image.open(png_start_path)) # Recent

image=Image.open(png_start_path)
img = image.resize((768,768))
png_start_image = ImageTk.PhotoImage(img)

label = Label(image=png_start_image)  # Recent OLD
#larger_image = png_start_image.zoom(2, 2)  # new fail
#larger_image = resizeImage(png_start_image, 1024,2024)  # New Fail

#label = Label(image=larger_image) # new fail


############### Buttons ###################################
label.grid(row=1, column=0, columnspan=4)

# We will have four button back , exit, reject, forward
button_back = Button(root, text="Back", command=back,state=DISABLED)
button_exit = Button(root, text="Exit",	command=lambda: exit() ) # closes csv file and runs root.quit for closing the app
button_forward = Button(root, text="Forward",command=lambda: forward(1))
button_reject = Button(root, text="Reject",	command=lambda: reject(accession))

# grid function is for placing the buttons in the frame
button_back.grid(row=5, column=0)
button_exit.grid(row=5, column=1)
button_reject.grid(row=5, column=2)
button_forward.grid(row=5, column=3)



################ Information #########################
label.grid(row=1, column=0, columnspan=3)
label1 = Label(text=accession)
label1.grid(row=6, column=1)
label2 = Label(text='0')
label2.grid(row=6, column=0)
label3 = Label(text=png_length)
label3.grid(row=6, column=2)



root.mainloop()
