# APK Compare Tool

A tool to compare differences between two APK files by decompiling them to smali code and showing textual differences. Ideal for analyzing code changes between app versions while excluding common library noise.

## Features
- Decompiles APKs using `apktool`
- Excludes specified libraries/paths from comparison (default: `com/google`, `androidx`)
- Outputs unified diff format for easy inspection
- Automatic cleanup of temporary files

## Prerequisites
- Java Runtime Environment (JRE)
- Python 3.x
- [apktool.jar](https://ibotpeaches.github.io/Apktool/) in project root

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/Maxdha/ApkCompare.git
   cd ApkCompare
   ```
2. Download `apktool.jar` from [official site](https://ibotpeaches.github.io/Apktool/) and place it in the project directory

## Usage

### Basic Comparison
```bash
python3 apk_compare.py old_app.apk new_app.apk
```

### Advanced Usage
```bash
python3 apk_compare.py path/to/old.apk path/to/new.apk \
  --exclude lib_to_skip1 path/to/lib2
```

**Arguments**:
- `old_apk`: Path to older APK version
- `new_apk`: Path to newer APK version
- `-e/--exclude`: [Optional] Space-separated list of directories to exclude from comparison

### Default Exclusions
The tool automatically excludes these common libraries:
- `com/google` (Google Play Services)
- `androidx` (AndroidX libraries)
