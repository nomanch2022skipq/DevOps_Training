import os

file_path = './data_2/Free_Test_Data_10.5MB_PDF.pdf'

if os.path.exists(file_path):
    print("yes")
else:
    print("no")# file doesn't exist, handle the error
