"""
Module providing the ability to test the following:
    1. Read target data from ckl file.
    2. Write target data to the ckl file
    3. Write vkey data to the ckl file
    4. Load vkey data that can then be used to verify you are writing to an 
       actual vkey in that stig
    5. Load target data that can then be used to verify you are writing to 
       an actual target in that stig
"""

import unittest
import xmltodict
from stig_edit import ckl_editor

TEST_FILE = "./tests/test.ckl"

class TestStigEdit(unittest.TestCase):

    '''Class to go through and test each function within the ckl_editor module.'''

    def test_read_target_data(self):

        '''Test the read_target_data function'''

        result = ckl_editor.read_target_data(TEST_FILE)
        self.assertIsNotNone(result)

    def test_load_target_data(self):

        '''Test the load_target_data function'''

        result = ckl_editor.load_target_data("./tests/test.ckl")
        self.assertIsNotNone(result)

    def test_load_vkey_data(self):

        '''Test the load_vkey_data function'''

        result = ckl_editor.load_vkey_data("./tests/test.ckl")
        self.assertIsNotNone(result)

    def test_write_target_data(self):

        '''Test the write_target_data function'''

        key = 'ROLE'
        value = 'Member Server'
        target_values = ckl_editor.load_target_data(TEST_FILE)
        #print(target_values)

        ckl_editor.write_target_data(   file_name="./tests/test.ckl",
                                        key=key,
                                        value=value,
                                        target_list=target_values
                                    )

        with open(TEST_FILE, 'r', encoding='utf-8') as ckl:
            ckl_dict = xmltodict.parse(ckl.read())
            self.assertEqual(ckl_dict['CHECKLIST']['ASSET'][key], value)

    def test_write_vkey_data(self):

        '''Test the write_vkey_data function'''

        key = 'V-230222'
        value = 'Not_Reviewed'
        vkeylist = ckl_editor.load_vkey_data(TEST_FILE)
        finding_details = "Server was patched.\nThis is not a finding"
        comment = "This is a test comment."

        ckl_editor.write_vkey_data( file_name="./tests/test.ckl",
                                    key=key,
                                    status=value,
                                    finding_details=finding_details,
                                    comments=comment,
                                    vkeylist=vkeylist
                                )

        with open(TEST_FILE, 'r', encoding='utf-8') as ckl:
            ckl_dict = xmltodict.parse(ckl.read())

            for vuln in ckl_dict['CHECKLIST']['STIGS']['iSTIG']['VULN']:
                for attribute in vuln['STIG_DATA']:
                    if attribute['ATTRIBUTE_DATA'] == key:
                        self.assertEqual(vuln['STATUS'], value)
                        self.assertEqual(vuln['FINDING_DETAILS'], finding_details)
                        self.assertEqual(vuln['COMMENTS'], comment)
