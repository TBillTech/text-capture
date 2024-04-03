#This script merely runs the text_capture.py test using the tests/input directory and the tests/output directory.  
#It cleans up the tests/output directory afterwards.  It is not a test itself, but rather a script to run the test.


import os
import shutil

def test_text_capture():
    # Define the input and output directories
    directory = 'tests/input'
    test_output_dir = 'tests/output'
    
    # Run the text_capture.py script, using the --test flag and the input and output directories
    os.system('python text_capture.py {} {} --rules tests/input/test_rules.rgx --test --test_output_dir {}'.format(directory, 'tests/test_output.py', test_output_dir))
        
    # Clean up the output directory
    #shutil.rmtree(test_output_dir)

if __name__ == '__main__':
    test_text_capture()
