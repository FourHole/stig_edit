# STIG EDIT

## Description

The purpose of this package is to allow you to quickly and easily edit STIG files (in ckl format). With this you can read and make changes to the target data within the check list. You can also make changes to individual checks.

## Editable Fields 

The following fields are able to be modified with this package:

### Target Data
| Available Targets | Available Fields                                          | Examples         |
|:------------------|:----------------------------------------------------------|:-----------------|
| ROLE              | None, Workstation, Member Server, Domain Controller       | Member Server    
| ASSET_TYPE        | Computing, Non-Computing                                  | Computing
| MARKING           | Any                                                       | CUI
| HOST_NAME         | Any                                                       | test_hostname1
| HOST_IP           | Any                                                       | 192.168.1.5
| HOST_MAC          | Any                                                       | 00:00:5e:00:53:af
| HOST_FQDN         | Any                                                       | test_hostname1.example.com
| TARGET_COMMENT    | Any                                                       | This is a test server.           
| TECH_AREA         | See footnote for options. [^1]                            | UNIX OS
| WEB_OR_DATABASE   | true, false                                               | false         
| WEB_DB_SITE       | Any (Only if WEB_OR_DATABASE is set to true)              | Chicago
| WEB_DB_INSTANCE   | Any (Only if WEB_OR_DATABASE is set to true)              | test01

[^1]: TECH_AREA Options: Application Review, Boundary Security, CDS Admin Review, CDS Technical Review, Database Review, Domain Name System (DNS), Exchange Server, Host Based System Security (HBSS), Internal Network, Mobility, Releasable Networks (REL), Traditional Security, UNIX OS, VVOIP Review, Web Review, Windows OS, Other Review


### vKey Data
| Available to Edit | Available Fields                                          | Examples         |
|:------------------|:----------------------------------------------------------|:-----------------|
| STATUS            | Not_Reviewed, Not_Applicable, NotAFinding, Open           | NotAFinding      
| FINDING_DETAILS   | Any                                                       | The check returned no results
| COMMENTS          | Any                                                       | Fixed on July 4, 1776

## Modules Available

---

### **read_target_data**(*filename*)

This module returns all target data for the ckl file that is parsed.

| Parameters        | Description                                               | Examples         | Required |
|:------------------|:----------------------------------------------------------|:-----------------|:---------|
| filename          | Filename of CKL file to parse.                            | testfile.txt     | yes

#### Example
```python
import ckl_editor
print(ckl_editor.read_target_data("test.ckl"))
```
    

---

### **load_vkey_data**(*filename*)

This module loads all available vkeys that can be passed to the *write_vkey_data()* module to ensure that you do not try to edit a vkey that does not exists in the stig file you are parsing. 

You should run this before running the *write_vkey_data()* module or use it as an input into it.

| Parameters        | Description                                               | Examples         | Required |
|:------------------|:----------------------------------------------------------|:-----------------|:---------|
| filename          | Filename of CKL file to parse.                            | testfile.txt     | yes

#### Example
```python
import ckl_editor

vkeylist = ckl_editor.load_vkey_data("test.ckl")
```

---

### **load_target_data**(*file_name*)

This is used to load all of the available target data for the STIG.

You should run this before running the *write_target_data()* or use it as an input into it

| Parameters        | Description                                               | Examples         | Required |
|:------------------|:----------------------------------------------------------|:-----------------|:---------|
| filename          | Filename of CKL file to parse.                            | testfile.txt     | yes

#### Example
```python
import ckl_editor

target_values=ckl_editor.load_target_data("test.ckl")
```
---

### **write_target_data**(*file_name*, *key*, *value*, *target_list*)

This module can write to any of the Target Data fields shown in the *Editable Fields/Target Data* section. Note the values because some fields must match a list of predefined values or the STIG Viewer will not be able to open the file.

Before running this module, you need to run the *load_target_data()* module and use that as the input for target_list. 

| Parameters        | Description                                               | Examples         | Required |
|:------------------|:----------------------------------------------------------|:-----------------|:---------|
| filename          | Filename of CKL file to parse.                            | testfile.txt     | yes      
| key               | Target field name that you want to edit                   | ROLE             | yes      
| value             | The value that you want to set the target field to        | Workstation      | yes      
| target_list       | The list of editable targets from *load_target_data()*    | load_target_data("test.txt")| yes

#### Example
```python
import ckl_editor

target_values=ckl_editor.load_target_data("test.ckl")

ckl_editor.write_target_data(file_name="test.ckl", key="ROLE", value="Member Server",target_list=target_values)
```

---

### **write_vkey_data**(*file_name*, *key*, *status*, *finding_details*, *comments*, *vkeylist*)

This module can write status, finding_details, and comments to any vkey that exists in your CKL file. It will error out if the vkey does not exists. Some of the fileds such as status have a list of predefined values you must use or the STIG Viewer will not be able to open the file.

Before running this module, you need to run the *load_vkey_data()* module and use that as the input for vkeylist.

| Parameters        | Description                                            | Examples         | Required |
|:------------------|:-------------------------------------------------------|:-----------------|:---------|
| filename          | Filename of CKL file to parse.                         | testfile.txt     | yes      
| key               | The vkey that you want to edit in the checklist        | V-230222         | yes      
| status            | The value that you want to set the status to.          | NotAFinding      | yes     
| finding_details   | Any information you want to put in the finding details | The check returned no results.| yes   
| comments          | Any information you want to put in the comments        | Fixed on July 4, 1776 | yes    
| vkeylist          | The list of editable vkeys from *load_vkey_data()*     | load_vkey_data("test.txt")| yes

```python
import ckl_editor

vkeylist = ckl_editor.load_vkey_data("test.ckl")

ckl_editor.write_vkey_data(file_name="test.ckl", key="V-230222", status="Not_Reviewed", finding_details="Server was patched.\nThis is not a finding", comments="No Comment.", vkeylist=vkeylist)
```

---