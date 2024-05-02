import os
import time
import subprocess

ENCYRPTION = "otp"
PROCESS_NUM = "4"


def file_exists(file_path):
    return os.path.exists(file_path)


def make_tags(dir: str, encryption: str):
    dir_list = os.listdir(dir)
    for file in dir_list:
        if not file.startswith("."):
            file_path = os.path.join(dir, file)
            subprocess.run(["mpirun", "-np", PROCESS_NUM, "pmac0.out","sign", file_path, encryption])
            print(f"{file}.tag created")

def remove_tags(dir: str):
    for file in os.listdir(dir):
        if file.endswith(".tag"):
            file_path = os.path.join(dir, file)
            os.remove(file_path)
            print(f"{file} removed")


def is_intruder_in_dir(dir: str, encryption: str) -> bool:
    for file in os.listdir(dir):
        if not file.endswith(".tag"):
            file_path = os.path.join(dir, file)
            print(f"Verifing {file} and {file}.tag")
            process = subprocess.run(["mpirun", "-np", PROCESS_NUM, "pmac0.out","verify", file_path, encryption, file_path + ".tag"], capture_output=True, text=True)

            if process.returncode == 0:
                stdout = process.stdout.strip()
                if stdout == "Tag is NOT valid":
                    print("Intruder Detected in file: ", file_path)
                    return True
            else:
                print("Something went wrong! Error code: ", process.returncode)
                return False
    return False 


# ---- MAIN ----

# compile pmac0.c if it does not exist
if not file_exists("pmac0.out"):
    subprocess.run(["mpicc", "pmac0/pmac0.c", "-o", "pmac0.out"])

remove_tags("files")
print("------------------------------")
# Make the signature
make_tags("files", ENCYRPTION)
print("------------------------------")

# Verify the signatures for each file in loop
check_num = 1
while True:
    print(f"Check number: {check_num}")
    if is_intruder_in_dir("files", ENCYRPTION):
        break
    time.sleep(0.5)
    check_num += 1
    print("------------------------------")
