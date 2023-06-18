import xmltodict
import json
import stig_edit.checks as checks
#from src.stig_edit import checks

#Read CKL Target Data
def read_target_data(file_name):
    
    with open(file_name, 'r', encoding='utf-8') as ckl:
        ckl_dict = xmltodict.parse(ckl.read())
    
    target_data = json.dumps(ckl_dict['CHECKLIST']['ASSET'], indent=2)
    
    return target_data

#Write to CKL Target Data
def write_target_data(file_name, key, value, target_list):
    
    #Error out if the file is not found, is a directory, or incorrect permissions on the file
    checks.check_file_and_keys(file_name=file_name, key=key, write_location='target_data', available_inputs=target_list)

    #Set the new value   
    with open(file_name, 'r+', encoding='utf-8') as ckl:
        ckl_dict = xmltodict.parse(ckl.read())
        ckl_dict['CHECKLIST']['ASSET'][key] = value
    
    #Add to XML file
    with open(file_name, 'r+', encoding='utf-8') as ckl:

        xml_out = xmltodict.unparse(ckl_dict, pretty=True)
        ckl_file_data = ['<?xml version="1.0" encoding="UTF-8"?>\n', '<!--DISA STIG Viewer :: 2.17-->\n', xml_out]
        ckl.writelines(ckl_file_data)
    
    #Create a list from all the lines to remove duplicate xml declarations
    with open(file_name, 'r', encoding='utf-8') as ckl:
        lines = ckl.readlines()

    #Rewrite the file without duplicate xml declaration
    with open(file_name, 'w', encoding='utf-8') as ckl:
       for number,line in enumerate(lines):
           if number not in [2]:
               ckl.writelines(line)

#Write to CKL vKey
def write_vkey_data(file_name, key, status, finding_details, comments, vkeylist):

    checks.check_file_and_keys(file_name=file_name, key=key, write_location='target_data', available_inputs=vkeylist)

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
        ckl_file_data = ['<?xml version="1.0" encoding="UTF-8"?>\n', '<!--DISA STIG Viewer :: 2.17-->\n', xml_out]
        ckl.writelines(ckl_file_data)
    
    #Create a list from all the lines to remove duplicate xml declarations
    with open(file_name, 'r', encoding='utf-8') as ckl:
        lines = ckl.readlines()

    #Rewrite the file without duplicate xml declaration
    with open(file_name, 'w', encoding='utf-8') as ckl:
       for number,line in enumerate(lines):
           if number not in [2]:
               ckl.writelines(line)
    

#Load STIG vKeys
def load_vkey_data(file_name):
    vkeylist = []

    with open(file_name, 'r', encoding='utf-8') as ckl:
        ckl_dict = xmltodict.parse(ckl.read())

        for vuln in ckl_dict['CHECKLIST']['STIGS']['iSTIG']['VULN']:
            for attribute in vuln['STIG_DATA']:
                if str(attribute['ATTRIBUTE_DATA']).startswith('V-'):
                    vkeylist.append(attribute['ATTRIBUTE_DATA'])

    return vkeylist

#Load Target Values
def load_target_data(file_name):
    with open(file_name, 'r', encoding='utf-8') as ckl:
        ckl_dict = xmltodict.parse(ckl.read())
        
        target_values = ckl_dict['CHECKLIST']['ASSET'].keys()
    return target_values