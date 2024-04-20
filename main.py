import os
import stat
import pwd
import grp
import time
import json
import hashlib
from virus_total_apis import PublicApi as VirusTotalPublicApi


# return hash a of specific file
def get_md5_hash(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def print_file_info(root_directory):
    for root, dirs, files in os.walk(root_directory):  # walk through directory
        for name in files:
            file_path = os.path.join(root, name)  # get file path for each file
            try:
                # use file path and different libraries to get information about file
                file_stat = os.stat(file_path)
                size = file_stat.st_size
                mod_time = time.ctime(file_stat.st_mtime)
                acc_time = time.ctime(file_stat.st_atime)
                cre_time = time.ctime(file_stat.st_ctime)
                owner = pwd.getpwuid(file_stat.st_uid).pw_name
                group = grp.getgrgid(file_stat.st_gid).gr_name
                permissions = stat.filemode(file_stat.st_mode)
                checksum = get_md5_hash(file_path)

                # print information about file
                print(f"""
                File: {file_path}
                Size: {size} bytes
                Location: {root}
                Last Modified: {mod_time}
                Last Accessed: {acc_time}
                Created: {cre_time}
                Owner: {owner}
                Group: {group}
                Permissions: {permissions}
                MD5 Checksum: {checksum}
                """)
                print("-" * 40)
            except Exception as e:
                print(f"Error processing file {file_path}: {e}")


def check_with_virus_total(file_path):
    API_KEY = 'YOUR_API_KEY'  # API from virus total

    MD5_hash = get_md5_hash(file_path)
    vt = VirusTotalPublicApi(API_KEY)

    response = vt.get_file_report(MD5_hash)  # get report from virus total
    print(json.dumps(response, sort_keys=False, indent=4))


print_file_info('./data')
check_with_virus_total('./data/ab6799b9abcfccd9d1813d07d83b325737221cf242126ad0918c2b84cc16c815.txt')
check_with_virus_total('./data/index.html')
