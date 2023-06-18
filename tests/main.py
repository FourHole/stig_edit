import stig_edit.src.stig_edit.ckl_editor as ckl_editor

#Load Target Data
target_values = ckl_editor.load_target_data("test.ckl")

#Load vKey List
vkeylist = ckl_editor.load_vkey_data("test.ckl")

#Test Target Data Pull
print(ckl_editor.read_target_data("test.ckl"))

#Test Write to Target Data then print the new output
ckl_editor.write_target_data(file_name="test.ckl", key="ROLE", value="Member Server",target_list=target_values)
#print(ckl_editor.read_target_data("test.ckl"))

#Test Write to vKey
ckl_editor.write_vkey_data(file_name="test.ckl", key="V-230222", status="Not_Reviewed", finding_details="Server was patched.\nThis is not a finding", comments="No Comment.", vkeylist=vkeylist)