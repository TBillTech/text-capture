#This script will capture all the text-like files in the directory structure and build another python
#script that will be able to recreate the directory structure and files. The new python script will take
#an argument for the location to unpack the captured tiles. This is useful for capturing
#the text of a website and being able to recreate it later, for example.

#The main inputs to this script are defined by the arg_parse object, which is defined in the main function.
#In this case, the arg_parse takes the following inputs:
#- The directory to be captured
#- The output file name
#- Optionally the rules file (which contains regexp patterns to ignore and/or keep)
#- Optionally the test flag which turns on running the resulting script, and comparing the output to the original
#- Optionally the test output directory for the test flag

import os
import re
import argparse

def main():
    # Define the arg parser
    parser = argparse.ArgumentParser(description='Capture text files in a directory structure')
    parser.add_argument('directory', help='The directory to be captured', default='.')
    parser.add_argument('output', help='The output file name', default='uncapture.py')
    parser.add_argument('--rules', help='The rules file (contains regexp patterns to ignore or keep)', default=None)
    parser.add_argument('--test', help='Run the resulting script and compare the output to the original', action='store_true')
    parser.add_argument('--test_output_dir', help='The output directory for the test flag', default='test_output')

    # Parse the arguments
    args = parser.parse_args()

    # Get the directory to be captured
    directory = args.directory

    # Get the output file name
    output = args.output

    # Get the ignore file
    rules = read_rules(args.rules)

    # Get the test flag
    test = args.test

    # Get the test output directory
    test_output_dir = args.test_output_dir
    # If the test_output_dir has anything other files or directories in it already, warn the user, and quit
    if os.path.exists(test_output_dir) and os.listdir(test_output_dir):
        print('The test_output_dir already exists and is not empty. Please clean the directory or choose a different one.')
        return

    # Capture the text files
    capture_text(directory, output, rules)

    if test:
        # Create the test output directory
        os.makedirs(test_output_dir, exist_ok=True)

        # Run the resulting script, passing the test_output_dir as the argument
        os.system('python {} {}'.format(output, test_output_dir))

        mismatch_summary = {}
        # Walk the output dir and the test_output_dir, comparing the files, _unless_ the file is in the ignore list
        for root, dirs, files in os.walk(directory):
            # Get the relative path
            rel_path = get_rel_path(directory, root)
            for file in files:
                # Get the file path
                file_path = os.path.join(root, file)
                rel_file_path = os.path.join(rel_path, file)

                # Check if the file should be ignored
                if ignore_file(file_path, rules):
                    continue

                # Compare the files
                with open(file_path, 'r') as f1, open(os.path.join(test_output_dir, rel_file_path), 'r') as f2:
                    if f1.read() != f2.read():
                        print('Files do not match: {} and {}'.format(file_path, os.path.join(test_output_dir, rel_file_path)))
                        mismatch_summary[file_path] = (file_path, os.path.join(test_output_dir, rel_file_path))
        
        # If there are no mismatches, print a success message
        if not mismatch_summary:
            print('All files match!')

def get_rel_path(directory, file):
    parts = []
    abs_root = file
    while abs_root != directory:
        abs_root, part = os.path.split(abs_root)
        parts.insert(0, part)
    return os.path.join(*parts) if parts else ''

def capture_text(directory, output, rules):
    # Open the output file
    with open(output, 'w') as f:
        # Write the header
        f.write('# Path: {}\n'.format(output))
        f.write('#This script will recreate the directory structure and files captured by text_capture.py\n')
        f.write('\n')

        # Write the import statements
        f.write('import os\n')
        f.write('import argparse\n')
        f.write('\n')

        # Write the main function (with arg parser)
        f.write('def main():\n')
        f.write('    # Define the arg parser\n')
        f.write('    parser = argparse.ArgumentParser(description=\'Recreate directory structure and files captured by text_capture.py\')\n')
        f.write('    parser.add_argument(\'output_dir\', help=\'The directory to unpack the captured files\', default=\'.\')\n')
        f.write('    args = parser.parse_args()\n')
        f.write('\n')
        f.write('    # Get the output directory\n')
        f.write('    output_dir = args.output_dir\n')
        f.write('\n')
        f.write('    # Create the directory structure\n')
        f.write('    create_directory_structure(output_dir)\n')
        f.write('\n')

        # Write the create_directory_structure function
        f.write('def create_directory_structure(directory):\n')

        # Walk the directory
        for root, dirs, files in os.walk(directory):
            rel_path = get_rel_path(directory, root)

            # Write the create files
            for file in files:
                # Get the file path
                file_path = os.path.join(root, file)
                rel_file_path = os.path.join(rel_path, file)

                # Check if the file should be ignored
                if ignore_file(file_path, rules):
                    continue

                # Write the create directory structure, prepending the root with the output directory
                f.write('    # Create directory: {}\n'.format(rel_path))
                f.write('    os.makedirs(os.path.join(directory, \'{}\'), exist_ok=True)\n'.format(rel_path))
                f.write('\n')
                # Write the create file, taking care to use the output directory
                f.write('    # Create file: {}\n'.format(rel_file_path))
                f.write('    with open(os.path.join(directory, \'{}\'), \'w\') as f:\n'.format(rel_file_path))

                # Write the file contents
                # Since each line can contain arbitrary text characters, we need to escape the line before capturing it
                # to the output script, but then un-escape it when the script is run
                with open(file_path, 'r') as file:
                    empty = True
                    for line in file:
                        # Remove the newline
                        text = line.rstrip('\n')
                        escaped_line = text.replace('\\', '\\\\').replace('\'', '\\\'')
                        # Now write out a call to the f.write_escaped:
                        if line.endswith('\n'):
                            f.write('        f.write(\'{}\\n\')\n'.format(escaped_line))
                        else:
                            f.write('        f.write(\'{}\')\n'.format(escaped_line))
                        empty = False
                    if empty:
                        f.write('        pass')

                f.write('\n')

        # Write the main function call
        f.write('if __name__ == \'__main__\':\n')
        f.write('    main()\n')

def read_rules(rule_file):
    # Check if the rules file is None
    if rule_file is None:
        return ([],[])

    (ignore_patterns, keep_patterns) = ([], [])
    # Read the rules file
    with open(rule_file, 'r') as f:
        for line in f:
            if line.startswith('ignore:'):
                ignore_patterns += [re.compile(line[7:].strip())]
            elif line.startswith('keep:'):
                keep_patterns += [re.compile(line[5:].strip())]
    return (ignore_patterns, keep_patterns) 

def ignore_file(file, rules):
    for pattern in rules[1]:
        if pattern.match(file):
            return False
    # First, if it doesn't have a file extension, and is not one of Dockerfile, Jenkinsfile ignore it 
    if not '.' in file:
        return True
    # Check if the file should be ignored
    for pattern in rules[0]:
        if pattern.match(file):
            return True

    return False

if __name__ == '__main__':
    main()


