import os
import time
import subprocess

ENCYRPTION = "otp"
PROCESS_NUM = "4"


def file_exists(file_path):
    return os.path.exists(file_path)


def sign_in_dir(dir: str, encryption: str):
    dir_list = os.listdir(dir)
    for file in dir_list:
        if not file.startswith("."):
            file_path = os.path.join(dir, file)
            print(f"Signing {file}")
            subprocess.run(["mpirun", "-np", PROCESS_NUM, "pmac0.out","sign", file_path, encryption])

def remove_tags_in_dir(dir: str):
    for file in os.listdir(dir):
        if file.endswith(".tag"):
            file_path = os.path.join(dir, file)
            print(f"Removing {file}")
            os.remove(file_path)


def verify_in_dir(dir: str, encryption: str):
    for file in os.listdir(dir):
        if not file.endswith(".tag"):
            file_path = os.path.join(dir, file)
            print(f"Verifing {file}")
            subprocess.run(["mpirun", "-np", PROCESS_NUM, "pmac0.out","verify", file_path, encryption, file_path + ".tag"])

# compile pmac0.c if it does not exist
if not file_exists("pmac0.out"):
    subprocess.run(["mpicc", "pmac0/pmac0.c", "-o", "pmac0.out"])

remove_tags_in_dir("files")
# Make the signature
sign_in_dir("files", ENCYRPTION)

# Verify the signatures for each file in loop
check_num = 0
while True:
    print(f"{check_num}:", end=" ")
    verify_in_dir("files", ENCYRPTION)
    time.sleep(1)
    check_num += 1
