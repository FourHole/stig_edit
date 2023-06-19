"""
Module providing error handling to prevent ckl file corruption and thaty it exists with 
the correct permissions
"""
import os

def check_file_and_keys(file_name, key, available_inputs):

    """Error out if the file is not found, is a directory, or incorrect permissions on the file"""
    try:
        with open(file_name, 'r', encoding='utf-8'):
            if os.path.getsize(file_name) == 0:
                raise ValueError('The CKL file is empty.')
        #file = open(file_name, encoding='utf-8')
    except FileNotFoundError:
        print(f'ERROR: File not found: {file_name}')
    except IsADirectoryError:
        print(f'ERROR: {file_name} is a directory and not a file.')
    except PermissionError:
        print(f'Permission denied for file: {file_name}')
    else:
        if key not in available_inputs:
            raise ValueError(f'{key} is not a valid key.')
