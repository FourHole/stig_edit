import xmltodict

def check_file_and_keys(file_name, key, write_location, available_inputs):
    
    #Error out if the file is not found, is a directory, or incorrect permissions on the file
    try:
        file = open(file_name, encoding='utf-8')
    except FileNotFoundError as e:
        print(f'ERROR: File not found: {file_name}')
    except IsADirectoryError as e:
        print(f'ERROR: {file_name} is a directory and not a file.')
    except PermissionError as e:
        print(f'Permission denied for file: {file_name}')
    else:
        with open(file_name, 'r', encoding='utf-8') as ckl:
            #ckl_dict = xmltodict.parse(ckl.read())
            if write_location == 'target_data':
                available_keys = available_inputs
            elif write_location == 'vkey_data':
                available_keys == available_inputs

            if key not in available_keys:
               raise Exception(f'{key} is not a valid key.') 