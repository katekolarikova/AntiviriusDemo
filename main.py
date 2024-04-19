import os
import hashlib
import stat
import pwd
import grp
import time
import json
import hashlib
from virus_total_apis import PublicApi as VirusTotalPublicApi

def get_md5_hash(file_path):
    """Calculate the MD5 checksum of a file."""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def get_file_type(file_path):
    """Determine the type of the file."""
    if os.path.isdir(file_path):
        return "Directory"
    elif os.path.isfile(file_path):
        return "File"
    elif os.path.islink(file_path):
        return "Symlink"
    else:
        return "Unknown"

def print_file_info(root_directory):
    """Print detailed information about all files in the directory, including hidden files."""
    for root, dirs, files in os.walk(root_directory):
        for name in files:
            file_path = os.path.join(root, name)
            try:
                # File information
                file_stat = os.stat(file_path)
                size = file_stat.st_size
                mod_time = time.ctime(file_stat.st_mtime)
                acc_time = time.ctime(file_stat.st_atime)
                cre_time = time.ctime(file_stat.st_ctime)
                owner = pwd.getpwuid(file_stat.st_uid).pw_name
                group = grp.getgrgid(file_stat.st_gid).gr_name
                permissions = stat.filemode(file_stat.st_mode)
                checksum = get_md5_hash(file_path)
                file_type = get_file_type(file_path)

                # Output information
                print(f"File: {file_path}")
                print(f"Type: {file_type}")
                print(f"Size: {size} bytes")
                print(f"Location: {root}")
                print(f"Last Modified: {mod_time}")
                print(f"Last Accessed: {acc_time}")
                print(f"Created: {cre_time}")
                print(f"Owner: {owner}")
                print(f"Group: {group}")
                print(f"Permissions: {permissions}")
                print(f"MD5 Checksum: {checksum}")
                print("-" * 40)
            except Exception as e:
                print(f"Error processing file {file_path}: {e}")


def check_with_virus_total(file_path):
    API_KEY = '6154f0630f8b307005a0a6d0ab11b8c2240f1f26d97df97477fdfd1ac7b861e7'

    EICAR_MD5 = get_md5_hash(file_path)

    vt = VirusTotalPublicApi(API_KEY)

    response = vt.get_file_report(EICAR_MD5)
    print(json.dumps(response, sort_keys=False, indent=4))
# Replace 'your_directory_path_here' with the path to the directory you want to scan
print_file_info('./data')
check_with_virus_total('./data/ab6799b9abcfccd9d1813d07d83b325737221cf242126ad0918c2b84cc16c815.txt')
check_with_virus_total('./data/index.html')
