# text-capture
Captures text files in a directory structure, and creates a single python script which can be executed to reproduce the file structure.

## Purpose
The purpose of this project is to capture text files in a directory structure and generate a Python script that can be used to recreate the same file structure.

## Usage
To use this project, follow these steps:
1. Clone the repository: `git clone https://github.com/your-username/text-capture.git`
2. Navigate to the project directory: `cd text-capture`
4. Run the script: `python text_capture.py --help`
5. The script will scan the directory structure and capture all the text files.
6. It will then generate a Python script named `uncapture.py` (by default) in the same directory.
7. Execute the `uncapture.py` script to recreate the file structure.

## Appendix: How to Use the rules.txt File
The `rules.txt` file is used to specify the rules for capturing the text files. Each line in the file represents a rule. Here are some examples of rules that can be used:

- To ignore files which match a specific regex, prefix with `ignore:`, for example `ignore:.*\.tgz`
- To capture files with a specific pattern in the name use the `keep:` prefix, for example `keep:.*Dockerfile`
- Files that are neither ignored nor kept, are kept by default
- Files without an extension, however, are ignored by default

Make sure to modify the `rules.txt` file according to your requirements before running the script.