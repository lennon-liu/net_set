from flask import Flask, request
from flask.json import jsonify
import traceback
from tool import logcfg
from tool import netconfig
from tool import  networks_from_settings
import json
from tool.mode_control import *

app = Flask(__name__)


@app.route('/get_addr_info',methods=["POST"])
def get_adder_info():
    try:
        try:
            data = json.loads(request.json)
            nic1_name= data.get('nic1_name',"")
        except:
            nic1_name=""
        if not nic1_name:
            status,nic1_name = networks_from_settings.get_nic_name("/td01/network_settings.json")
            if not status:
                return json.dumps({"status":False,"msg":"no nic info"})
        net_info = netconfig.td01_netconfig_query(nic1_name)
        net_info["net_mode"] = net_mode_class.net_mode
        return jsonify(net_info)
    except:
        msg = traceback.format_exc()
        logcfg.logger.debug(msg)
        content = {
            "status":False,
            "msg":msg
        }
        content["net_mode"] = net_mode_class.net_mode
        return jsonify(content)

@app.route('/manual_setting',methods=["POST"])
def manual_setting():
    try:
        try:
            data = json.loads(request.data)
            nic1_name = data.get('nic1_name',"")
            ipaddr = data.get("ipaddr", "")
            netmask = data.get("netmask", "")
            gateway = data.get("gateway", "")
            dns1 = data.get("dns1", "")
            dns2 = data.get("dns2", "")
        except:
            nic1_name=None
            msg = traceback.format_exc()
            logcfg.logger.debug(msg)
        if not nic1_name:
            status,nic1_name = networks_from_settings.get_nic_name("/td01/network_settings.json")
            if not status:
                return json.dumps({"status":False,"msg":"no nic info"})
        net_info={"interface":nic1_name,"ipaddr": ipaddr, "netmask": netmask, "gateway": gateway,"dns1": dns1, "dns2": dns2}
        setting_status = netconfig.manual_net_set(net_info)

        return jsonify(setting_status)
    except:
        msg = traceback.format_exc()
        logcfg.logger.debug(msg)
        content = {
            "status":False,
            "msg":msg
        }
        return jsonify(content)


@app.route('/auto_setting',methods=["POST"])
def auto_setting():
    try:

        try:
            data = json.loads(request.data)
            nic1_name= data.get('nic1_name',"")
        except:
            nic1_name=""
        if not nic1_name:
            status,nic1_name = networks_from_settings.get_nic_name("/td01/network_settings.json")
            if not status:
                return json.dumps({"status":False,"msg":"no nic info"})
        reset_status = netconfig.auto_net_set({"interface":nic1_name})

        return jsonify(reset_status)
    except:
        msg = traceback.format_exc()
        logcfg.logger.debug(msg)
        content = {
            "status":False,
            "msg":msg
        }
        return jsonify(content)



def create_app():
    app.run(host="0.0.0.0", port=8500, debug=False)

if __name__ == '__main__':
    create_app()
