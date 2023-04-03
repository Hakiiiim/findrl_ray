import ftplib
import os

# Define FTP server credentials and directory
host = 'ftp.example.com'
username = 'your-username'
password = 'your-password'

# Create FTP session
#session = ftplib.FTP(host, username, password)
#session.cwd(remote_directory)
# Define function to upload files recursively
def upload_files(local_dir,remote_dir):
    session = ftplib.FTP(host, username, password)
    session.cwd(remote_dir)
    for filename in os.listdir(local_dir):
        local_path = os.path.join(local_dir, filename)
        remote_path = os.path.join(remote_dir, filename)
        if os.path.isdir(local_path):
            session.mkd(remote_path)
            upload_files(local_path)
        else:
            with open(local_path, 'rb') as f:
                session.storbinary(f'STOR {remote_path}', f)
    print(f'{local_dir}is uploaded to:{remote_path}')
    session.quit()
