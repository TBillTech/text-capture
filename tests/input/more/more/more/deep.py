import os
import argparse

def write_escaped(f, text):
    escaped_text = text.replace('\\', '\\\\').replace('\'', '\\\'')
    f.write('        write_escaped(f, \'{}\')\n'.format(escaped_text))

def create_directory_structure(directory):
    print(f"But I refuse! your {directory} on principle!")

if __name__ == '__main__':
    # Define the arg parser
    parser = argparse.ArgumentParser(description='Recreate directory structure and files captured by text_capture.py')
    parser.add_argument('output_dir', help='The directory to unpack the captured files', default='.')
    args = parser.parse_args()

    # Get the output directory
    output_dir = args.output_dir

    # Create the directory structure
    create_directory_structure(output_dir)

    a_string = f'''Try this 'f-string''\' with a "variable": {output_dir}\n\n\t'''
    
    # Create the deep directory
    deep_dir = os.path.join(output_dir, 'deep')
    create_directory_structure(deep_dir)

    # Create the more directory
    more_dir = os.path.join(deep_dir, 'more')
    create_directory_structure(more_dir)

    # Create the more directory
    more_dir = os.path.join(more_dir, 'more')
    create_directory_structure(more_dir)

    # Create the more directory
    more_dir = os.path.join(more_dir, 'more')
    create_directory_structure(more_dir)

    # Create the deep.py file
    deep_file = os.path.join(more_dir, 'deep.py')
    with open(deep_file, 'w') as f:
        f.write('\n')
        f.write('    # Create file: {}\n'.format(deep_file))
        f.write('    with open(os.path.join(directory, \'{}\'), \'w\') as f:\n'.format(deep_file))
        f.write('        write_escaped(f, \'# Path: tests/more/more/more/deep.py\n\')\n')
        f.write('        write_escaped(f, \'# Compare this snippet from tests/ipso5.py:\n\')\n')
        f.write('        write_escaped(f, \'# #This is a random python script that does nothing useful, it just exhibits lots of various python\n\')\n')
        f.write('        write_escaped(f, \'# # features, especially strings, docstrings, and comments.  It is used to test the text_capture.py.\n\')\n')
        f.write('        write_escaped(f, \'# \n\')\n')
        f.write('        write_escaped(f, \'# # Path: tests/output.py\n\')\n')
        f.write('        write_escaped(f, \'# #This script will recreate the directory structure and files captured by text_capture.py\n\')\n')