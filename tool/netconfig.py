#ecoding:utf-8
import json
import os
import netifaces
import traceback
from logcfg import *
from systemcontrol import SystemControl
from tool.mode_control import *

def td01_netconfig_query(interface):
    if not interface:
        return {"status": False, "info": {}, "msg": "no nic info"}
    try:
        try:
            gatewaylist=netifaces.gateways()[2]
            for gateway in gatewaylist:
                gatewaycp,interfacecp,status =gateway
                if interface==interfacecp:
                    routingGateway=gatewaycp
                    break
            else:
                routingGateway = '0.0.0.0'
        except:
            routingGateway = '0.0.0.0'
        # routingNicName = netifaces.gateways()['default'][netifaces.AF_INET][1]
        # print "routingNicName:", routingNicName
        # routingGateway = netifaces.gateways()['default'][netifaces.AF_INET][0]
        # print "routingGateway:", routingGateway
        # if interface != routingNicName:
        #     routingGateway = '0.0.0.0'
        #print  netifaces.ifaddresses(interface)[netifaces.AF_LINK][0]
        routingNicMacAddr = netifaces.ifaddresses(interface)[netifaces.AF_LINK][0]['addr']
        try:
            routingIPAddr = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr']
            # TODO(Guodong Ding) Note: On Windows, netmask maybe give a wrong result in 'netifaces' module.
            routingIPNetmask = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['netmask']
            #print netifaces.ifaddresses(interface)
            # routingdns1 = netifaces.ifaddresses(interface)[netifaces.AF_INET][0].get("dns1","")
            # #print "dns1:",routingdns1
            #
            # routingdns2 = netifaces.ifaddresses(interface)[netifaces.AF_INET][0].get("dns2", "")
            #print "dns2:", routingdns2
        except KeyError:
            msg = traceback.format_exc()
            logger.error(msg)
            return {"status": False, "info": {}, "msg": str(msg)}
        if not routingIPAddr:
            return {"status": False, "info": {}}
        try:
            info = read_network_info()
            dns1 = info["dns1"]
            dns2 = info["dns2"]
            nic2_info = info.get("NIC2",{})
        except:
            dns1=""
            dns2=""
            nic2_info={}
        if not dns1 and not dns2:
            if not dns1 :
                dns1= "218.2.135.1"
            if not dns2:
                dns2="114.114.114.114"
        return  {"status": True,"info":{"NIC1":{"ip": routingIPAddr, "netmask": routingIPNetmask, "gateway": routingGateway, "mac": routingNicMacAddr,"dns1":dns1,"dns2":dns2},"NIC2":nic2_info}}
    except Exception,e:
        msg= traceback.format_exc()
        logger.error(msg)
        return {"status": False, "info": {},"msg":str(msg)}


def manual_net_set(args):
    try:
        interface= args.get("interface","")
        ipaddr= args.get("ipaddr","")
        netmask= args.get("netmask","")
        gateway= args.get("gateway","")
        dns1= args.get("dns1","")
        dns2 = args.get("dns2","")
        #print interface,ipaddr,netmask,gateway
        if not interface  or not ipaddr or not  netmask or not gateway:
            #return({"td01_netconfig_set": "usage: td01_netconfig_set -i eth0 -a 192.168.1.5 -m 255.255.255.0 -g 192.168.1.2"})
            return {"status": False,"msg":"配置不全，请验证"}
        # if not dns1:
        #     dns1 = "218.2.135.1"
        # if not dns2:
        #     dns2 = "114.114.114.114"
        doSomething = SystemControl(ipaddr, gateway, netmask, interface, dns1, dns2)
        reset_status = doSomething.reset_devide_cfg("manul")
        info = read_network_info()
        info["dns1"] = dns1
        info["dns2"] = dns2
        write_network_info(info)
        if reset_status:
            if doSomething.restart_device():
                net_mode_class.set_mode("manual")
                return ({"status":True})
            else:
                return ({"status": False,"msg":"配置错误,请验证"})
        else:
            logger.error("重写设备网络配置失败!")


    except:
        msg = traceback.format_exc()
        return({"status": False,"msg":str(msg)})

def auto_net_set(args):
    try:
        interface = args.get("interface", None)
        doSomething = SystemControl(ip="", gateway="", netmask="", device=interface, dns1="", dns2="")
        reset_status = doSomething.reset_devide_cfg("auto")
        info = read_network_info()
        info["dns1"] = ""
        info["dns2"] = ""
        write_network_info(info)
        if reset_status:
            if doSomething.restart_device():
                net_mode_class.set_mode("auto")
                return ({"status": True})
            else:
                return ({"status": False, "msg": "配置错误,请验证"})
        else:
            logger.error("重写设备网络配置失败!")
            return ({"status": False, "msg": "重写设备网络配置失败"})

    except:
        msg = traceback.format_exc()
        return({"status": False,"msg":str(msg)})



def read_network_info():
    fp=open("/td01/network_settings.json","rb")
    info= json.load(fp)
    fp.close()
    return info

def write_network_info(info):  
    fp=open("/td01/network_settings.json","wb")
    json.dump(info,fp)
    fp.close()
