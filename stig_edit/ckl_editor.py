"""
Module providing the ability to do the following:
    1. Read target data from ckl file.
    2. Write target data to the ckl file
    3. Write vkey data to the ckl file
    4. Load vkey data that can then be used to verify you are writing to an 
       actual vkey in that stig
    5. Load target data that can then be used to verify you are writing to 
       an actual target in that stig
"""

import json
import xmltodict
from stig_edit import handler

def read_target_data(file_name):

    '''Read CKL Target Data'''

    with open(file_name, 'r', encoding='utf-8') as ckl:
        ckl_dict = xmltodict.parse(ckl.read())

    target_data = json.dumps(ckl_dict['CHECKLIST']['ASSET'], indent=2)

    return target_data


def write_target_data(file_name, key, value):

    '''Write to CKL Target Data'''

    with open(file_name, 'r', encoding='utf-8') as ckl:
        ckl_dict = xmltodict.parse(ckl.read())

        target_values = ckl_dict['CHECKLIST']['ASSET'].keys()

    #Error out if the file is not found, is a directory, or incorrect permissions on the file
    handler.check_file_and_keys(file_name=file_name, key=key, available_inputs=target_values)

    #Set the new value
    with open(file_name, 'r+', encoding='utf-8') as ckl:
        ckl_dict = xmltodict.parse(ckl.read())
        ckl_dict['CHECKLIST']['ASSET'][key] = value
        print(f'Setting {key} to {value} in dictionary.')

    #Add to XML file
    with open(file_name, 'r+', encoding='utf-8') as ckl:

        xml_out = xmltodict.unparse(ckl_dict, pretty=True)
        ckl_file_data = [   '<?xml version="1.0" encoding="UTF-8"?>\n',
                            '<!--DISA STIG Viewer :: 2.17-->\n', 
                            xml_out
                        ]
        ckl.writelines(ckl_file_data)
        print(f"Adding {key}'s value from dictionary to ckl file.")

    #Create a list from all the lines to remove duplicate xml declarations
    with open(file_name, 'r', encoding='utf-8') as ckl:
        lines = ckl.readlines()

    #Rewrite the file without duplicate xml declaration
    with open(file_name, 'w', encoding='utf-8') as ckl:
        for number,line in enumerate(lines):
            if number not in [2]:
                ckl.writelines(line)

    print(f"Finished rebuilding CKL file with new {key} added.")

def write_vkey_data(file_name, key, status, finding_details, comments):

    '''Write to CKL vKey'''

    vkeylist = []

    with open(file_name, 'r', encoding='utf-8') as ckl:
        ckl_dict = xmltodict.parse(ckl.read())

        for vuln in ckl_dict['CHECKLIST']['STIGS']['iSTIG']['VULN']:
            for attribute in vuln['STIG_DATA']:
                if str(attribute['ATTRIBUTE_DATA']).startswith('V-'):
                    vkeylist.append(attribute['ATTRIBUTE_DATA'])

    handler.check_file_and_keys(file_name=file_name, key=key, available_inputs=vkeylist)

    with open(file_name, 'r', encoding='utf-8') as ckl:
        ckl_dict = xmltodict.parse(ckl.read())

        for vuln in ckl_dict['CHECKLIST']['STIGS']['iSTIG']['VULN']:
            for attribute in vuln['STIG_DATA']:
                if attribute['ATTRIBUTE_DATA'] == key:
                    vuln['STATUS'] = status
                    vuln['FINDING_DETAILS'] = finding_details
                    vuln['COMMENTS'] = comments

    #Add to XML file
    with open(file_name, 'r+', encoding='utf-8') as ckl:

        xml_out = xmltodict.unparse(ckl_dict, pretty=True)
        ckl_file_data = [   '<?xml version="1.0" encoding="UTF-8"?>\n',
                            '<!--DISA STIG Viewer :: 2.17-->\n',
                            xml_out
                        ]
        ckl.writelines(ckl_file_data)

    #Create a list from all the lines to remove duplicate xml declarations
    with open(file_name, 'r', encoding='utf-8') as ckl:
        lines = ckl.readlines()

    #Rewrite the file without duplicate xml declaration
    with open(file_name, 'w', encoding='utf-8') as ckl:
        for number,line in enumerate(lines):
            if number not in [2]:
                ckl.writelines(line)
