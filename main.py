import os
import time
import subprocess

ENCYRPTION = "otp"
PROCESS_NUM = "4"


def file_exists(file_path):
    return os.path.exists(file_path)


def in_dir_sign(dir: str, encryption: str):
    dir_list = os.listdir(dir)
    for file in dir_list:
        if not file.startswith("."):
            file_path = os.path.join(dir, file)
            print(f"Signing {file}")
            subprocess.run(["mpirun", "-np", PROCESS_NUM, "pmac0.out","sign", file_path, encryption])

def in_dir_remove_tags(dir: str):
    for file in os.listdir(dir):
        if file.endswith(".tag"):
            file_path = os.path.join(dir, file)
            print(f"Removing {file}")
            os.remove(file_path)


def in_dir_verify(dir: str, encryption: str) -> bool:
    for file in os.listdir(dir):
        if not file.endswith(".tag"):
            file_path = os.path.join(dir, file)
            print(f"Verifing {file}")
            process = subprocess.run(["mpirun", "-np", PROCESS_NUM, "pmac0.out","verify", file_path, encryption, file_path + ".tag"], capture_output=True, text=True)

            if process.returncode == 0:
                stdout = process.stdout.strip()
                if stdout == "Tag is NOT valid":
                    print("Intruder Detected in file: ", file_path)
                    return False
            else:
                print("Something went wrong! Error code: ", process.returncode)
                return True
    return True
# compile pmac0.c if it does not exist
if not file_exists("pmac0.out"):
    subprocess.run(["mpicc", "pmac0/pmac0.c", "-o", "pmac0.out"])

in_dir_remove_tags("files")
# Make the signature
in_dir_sign("files", ENCYRPTION)

# Verify the signatures for each file in loop
check_num = 0
while True:
    print(f"Check number: {check_num}")
    if not in_dir_verify("files", ENCYRPTION):
        break
    time.sleep(0.5)
    check_num += 1
