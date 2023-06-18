#import ckl_editor
from src.stig_edit import ckl_editor

#Load Target Data
target_values = ckl_editor.load_target_data("./tests/test.ckl")

#Load vKey List
vkeylist = ckl_editor.load_vkey_data("./tests/test.ckl")

#Test Target Data Pull
print(ckl_editor.read_target_data("./tests/test.ckl"))

#Test Write to Target Data then print the new output
ckl_editor.write_target_data(file_name="./tests/test.ckl", key="ROLE", value="Member Server",target_list=target_values)

#Test Write to vKey
ckl_editor.write_vkey_data(file_name="./tests/test.ckl", key="V-230222", status="Not_Reviewed", finding_details="Server was patched.\nThis is not a finding", comments="No Comment.", vkeylist=vkeylist)
