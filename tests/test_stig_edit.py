import unittest
import xmltodict
from src.stig_edit import ckl_editor

test_file = "./tests/test.ckl"

class TestStigEdit(unittest.TestCase):

    def test_read_target_data(self):
        result = ckl_editor.read_target_data(test_file)
        self.assertIsNotNone(result)

    def test_load_target_data(self):
        result = ckl_editor.load_target_data("./tests/test.ckl")
        self.assertIsNotNone(result)
    
    def test_load_vkey_data(self):
        result = ckl_editor.load_vkey_data("./tests/test.ckl")
        self.assertIsNotNone(result)

    def test_write_target_data(self):
        key = 'ROLE'
        value = 'Member Server'
        target_values = ckl_editor.load_target_data(test_file)
        #print(target_values)

        ckl_editor.write_target_data(file_name="./tests/test.ckl", key=key, value=value, target_list=target_values)
#
        with open(test_file, 'r', encoding='utf-8') as ckl:
            ckl_dict = xmltodict.parse(ckl.read())
            print(', Input Value: ' + value + ', Value in Dictionary: ' + ckl_dict['CHECKLIST']['ASSET'][key])
            self.assertEqual(ckl_dict['CHECKLIST']['ASSET'][key], value)
    
    def test_write_vkey_data(self):
        key = 'V-230222'
        value = 'Not_Reviewed'
        vkeylist = ckl_editor.load_vkey_data(test_file)
        finding_details = "Server was patched.\nThis is not a finding"
        comment = "This is a test comment."
        
        ckl_editor.write_vkey_data( file_name="./tests/test.ckl",
                                    key=key,
                                    status=value,
                                    finding_details=finding_details,
                                    comments=comment,
                                    vkeylist=vkeylist
                                )

        with open(test_file, 'r', encoding='utf-8') as ckl:
            ckl_dict = xmltodict.parse(ckl.read())

            for vuln in ckl_dict['CHECKLIST']['STIGS']['iSTIG']['VULN']:
                for attribute in vuln['STIG_DATA']:
                    if attribute['ATTRIBUTE_DATA'] == key:
                        self.assertEqual(vuln['STATUS'], value)
                        self.assertEqual(vuln['FINDING_DETAILS'], finding_details)
                        self.assertEqual(vuln['COMMENTS'], comment)
