import os
import subprocess
import difflib
from shutil import rmtree
import argparse

def decode_apk(apk_path, output_dir):
    """Use apktool to decode APK files to smali code."""
    subprocess.run(["java", "-jar", "apktool.jar", "d", apk_path, "-o", output_dir], check=True)

def get_smali_files(directory, excluded_libraries):
    """Recursively get all smali files, skipping excluded libraries."""
    smali_files = []
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in excluded_libraries]  # Skip excluded directories
        for file in files:
            if file.endswith(".smali"):
                smali_files.append(os.path.join(root, file))
    return smali_files

def compare_files(file1, file2):
    """Compare two smali files and return the diff."""
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        file1_lines = f1.readlines()
        file2_lines = f2.readlines()

    diff = difflib.unified_diff(file1_lines, file2_lines, fromfile=file1, tofile=file2, lineterm='')
    return '\n'.join(diff)

def main(old_apk, new_apk, excluded_libraries):
    old_dir = "old_apk"
    new_dir = "new_apk"

    # Decode both APKs
    decode_apk(old_apk, old_dir)
    decode_apk(new_apk, new_dir)

    # Get smali files, skipping specified libraries
    old_files = get_smali_files(old_dir, excluded_libraries)
    new_files = get_smali_files(new_dir, excluded_libraries)

    # Map file paths from old APK to new APK
    old_files_map = {os.path.relpath(path, old_dir): path for path in old_files}
    new_files_map = {os.path.relpath(path, new_dir): path for path in new_files}

    # Compare corresponding smali files
    for file_path in old_files_map:
        if file_path in new_files_map:
            diff = compare_files(old_files_map[file_path], new_files_map[file_path])
            if diff:
                print(f"Changes in {file_path}:\n{diff}")

    # Clean up decoded directories
    rmtree(old_dir)
    rmtree(new_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Compare two APK files by decompiling them to smali and diffing the results."
    )
    parser.add_argument("old_apk", help="Path to the old APK file")
    parser.add_argument("new_apk", help="Path to the new APK file")
    parser.add_argument(
        "-e", "--exclude", nargs="*", default=['com/google', 'androidx'],
        help="List of libraries/directories to exclude (default: 'com/google', 'androidx')"
    )
    args = parser.parse_args()
    
    main(args.old_apk, args.new_apk, args.exclude)
