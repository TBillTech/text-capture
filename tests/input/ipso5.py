#This is a random python script that does nothing useful, it just exhibits lots of various python
# features, especially strings, docstrings, and comments.  It is used to test the text_capture.py.

# Path: tests/output.py
#This script will recreate the directory structure and files captured by text_capture.py

import os
import argparse
import re

# Do some nothing grinding with string literals
def nothing_grinder(more_text):
    # Define the arg parser
    parser = argparse.ArgumentParser(description='Grind up some text about a random topic')
    parser.add_argument('topic', help='A topic to grind', default='pandas')
    args = parser.parse_args()

    # Get the topic
    topic = args.topic

    # Define some text about animals, complete with escape characters, parenthesis, latin names, and other special characters.
    text = '''Animals are multicellular, "eukaryotic" organisms in the \n\tbiological kingdom Animalia. With 'few' exceptions, '''\
        '''animals consume organic material, breathe oxygen, are able to move, reproduce sexually, and grow from a hollow sphere of cells, '''\
        '''the blastula, during embryonic development. Over 1.5 million living animal species have been described—of which'''\
        ''' around 1 million are insects—but it has been estimated there are over 7 million animal species in total. Animals'''\
        ''' range in length from 8.5 millionths of a meter to 33.6 meters (110 ft) and have complex interactions with each'''\
        ''' other and their environments, forming intricate food webs. The category includes humans, but in colloquial use'''\
        ''' the term animal often refers only to non-human animals. The study of non-human animals is known as zoology.'''
    text = text + more_text

    # do a regexp replacement of the word 'animal' with the topic
    text = re.sub('animal', topic, text)

    # create an escaped text copy:
    escaped_text = text.replace('\\', '\\\\').replace('\'', '\\\'')
    return escaped_text

# Do some nothing grinding with string literals
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
    