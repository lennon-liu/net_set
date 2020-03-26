
import json
import os
import traceback
from logcfg import *
def get_nic_name(setting_path):
    try:
        if os.path.exists(setting_path):
            file_content = open(setting_path,"r").read()
            file_dict = json.loads(file_content)
            nic_name = file_dict.get("NIC1","")
            #print nic_name,"------->"
            if nic_name:
                return True,nic_name
            else:
                return False,""
        return False, ""
    except:
        msg=traceback.format_exc()
        logger.error(msg)
        return False,""
