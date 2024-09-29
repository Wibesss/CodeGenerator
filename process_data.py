import os
import subprocess
from colorama import Fore, init

init(autoreset=True)

MAX_CHAR_LENGTH = 512
MIN_CHAR_LENGTH = 256

NEWLINECHAR = "<N>"

full_paths = []
for dirpath, dirnames, filenames in os.walk("repos"):
    for f in filenames:
        full_path = os.path.join(dirpath, f)
        full_paths.append(full_path)

print(f"Total files found: {len(full_paths)}")

counter = 5

def format_file_with_black(file_path):
    try:
        subprocess.run(['black', file_path], check=True)
        print(Fore.GREEN + f"Formatted file: {file_path} using Black")
    except subprocess.CalledProcessError as e:
        print(Fore.RED + f"Black formatting failed for {file_path}: {e}")

with open("python_code_text.txt", "a", encoding="utf-8") as output_file:
    for fpath in full_paths:
        try:
            format_file_with_black(fpath)

            with open(fpath, "r", encoding="utf-8") as intput_file:
                content = intput_file.read()

            print(Fore.BLUE + f"Processing file: {fpath}, Length: {len(content)}")

            formatted_content = content.replace("\n", NEWLINECHAR)

            if 50 < len(formatted_content) <= MAX_CHAR_LENGTH:
                output_file.write(formatted_content + "\n")
                print(formatted_content + "\n")

            else:
                split_content = formatted_content.split(f"{NEWLINECHAR}{NEWLINECHAR}")
                substring = ""
                
                for split in split_content:
                    substring += split + f"{NEWLINECHAR}{NEWLINECHAR}"

                    if MIN_CHAR_LENGTH <= len(substring) <= MAX_CHAR_LENGTH:
                        output_file.write(substring + "\n")
                        print(substring + "\n")
                        substring = ""
                    
                    elif len(substring) > MAX_CHAR_LENGTH:
                        while len(substring) > MAX_CHAR_LENGTH:
                            output_file.write(substring[:MAX_CHAR_LENGTH] + "\n")
                            print(substring[:MAX_CHAR_LENGTH] + "\n")
                            substring = substring[MAX_CHAR_LENGTH:]
                
                if MIN_CHAR_LENGTH <= len(substring) <= MAX_CHAR_LENGTH:
                    output_file.write(substring + "\n")
                    print(substring + "\n")

            print(Fore.GREEN + f"Processed file: {fpath}")
            counter -= 1
            if counter == 0:
                break

        except UnicodeDecodeError as e:
            print(Fore.RED + f"Error reading {fpath}: {e}")
        except Exception as e:
            print(Fore.RED + f"An error occurred with {fpath}: {e}")
