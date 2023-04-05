import os
import zipfile
from ftplib import FTP
# Set up the FTP connection
ftp = FTP('storage1700.is.cc')
ftp.login(user='trainer@st31327.ispot.cc', passwd='ga42918828')

def ftpsavemodel(lcdir, filename):
# Set up the local directory and the name of the zip file
    local_dir = lcdir
    zip_filename = filename
    # Create the zip file
    zip_file = zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(local_dir):
        for file in files:
            zip_file.write(os.path.join(root, file))
    zip_file.close()

    # Open the zip file and send it over FTP
    with open(zip_filename, 'rb') as f:
        ftp.storbinary('STOR ' + zip_filename, f)
    # Close the FTP connection
    ftp.quit()
    # Delete the local zip file
    os.remove(zip_filename)
    return 'saved'