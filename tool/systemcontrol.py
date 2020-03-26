#ecoding:utf-8
import commands
import platform
import logcfg
class SystemControl(object):

    def __init__(self, ip, gateway, netmask, device, dns1, dns2):
        """
        @desc: init
        """
        self.platform = self.getPlatform()
        self.ip = ip
        self.gateway = gateway
        self.netmask = netmask
        self.device = device
        self.dns1 = dns1
        self.dns2 = dns2

    def changeNetwork(self):
        """
        @attention: change the network of the system
        """
        if self.platform == "centos":
            path = "/etc/sysconfig/network-scripts/ifcfg-" + str(self.device)
            file_handler = open(path, "r")
            network_content = file_handler.read()
            file_handler.close()
            conte = "IPADDR=%s\nNETMASK=%s\nGATEWAY=%s\nDNS1=%s\nDNS2=%s\n" % (
            self.ip, self.netmask, self.gateway, self.dns1, self.dns2)  # "218.2.135.1","114.114.114.114")
            # conte = "IPADDR=%s\nNETMASK=%s\nGATEWAY=%s\n" % (self.ip, self.netmask, self.gateway)

            num = network_content.find("IPADDR")
            if num != -1:
                network_content = network_content[:num] + conte
                # print(network_content)
                file_handler = open(path, "w")
                file_handler.write(network_content)
                file_handler.close()
        elif self.platform == "ubuntu":
            path = "/etc/network/interfaces"
            file_handler = open(path, "r")
            network_interfaces = file_handler.read()
            file_handler.close()
            network_content = network_interfaces.split("auto")
            for i in network_content:

                if self.device in i:
                    content = "auto %s\niface %s inet static\n\taddress %s\n\tnetmask %s\n\tgateway %s\n\t" % (
                        self.device, self.device, self.ip, self.netmask, self.gateway)
                    network_interfaces = network_interfaces.replace(i, content)
                    break
            file_handler = open(path, "w")
            file_handler.write(network_interfaces)
            file_handler.close()
        else:
            raise Exception("unknown os")
        commands.getoutput("sudo ifdown %s && sudo ifup %s" % (self.device, self.device))



    def delWith(self):
         self.changeNetwork()

    def getPlatform(self):
        """
        @attention: get the platform of the system
        """
        try:
            platForm = platform.platform().lower()
            if "ubuntu" in platForm:
                return "ubuntu"
            elif "centos" in platForm:
                return "centos"
        except:
            return None



    def restart_device(self):
        msg =  commands.getoutput("sudo ifdown %s && sudo ifup %s" % (self.device, self.device))
        if "错误" in msg or "失败" in msg:
            return False
        else:
            return True
        logcfg.logger.info(msg)


    def reset_devide_cfg(self,opt):
        if self.platform == "centos":
            path = "/etc/sysconfig/network-scripts/ifcfg-" + str(self.device)
            file_handler = open(path, "r")
            network_content = file_handler.readlines()
            network_setting_dict={}
            file_handler.close()
            for content in network_content:
                try:
                    content_split=content.strip().split("=")
                    content_key = content_split[0]
                    content_value = content_split[1]
                    if content_key and content_value:
                        network_setting_dict[content_key] =content_value
                except Exception,e:
                    pass
            for keys in ["IPADDR", "NETMASK", "GATEWAY", "DNS1", "DNS2", "BOOTPROTO", "ONBOOT"]:
                if network_setting_dict.has_key(keys):
                    network_setting_dict.pop(keys)
            stetting_content = ""
            if opt == "auto":
                network_setting_dict["BOOTPROTO"]="dhcp"
                network_setting_dict["ONBOOT"] = "yes"
                for item in network_setting_dict.items():
                    key,value = item
                    stetting_content+="%s=%s\n"%(key,value)
            elif opt=="manul":
                network_setting_dict["BOOTPROTO"] = "static"
                network_setting_dict["ONBOOT"] = "no"
                network_setting_dict["IPADDR"] = self.ip
                network_setting_dict["NETMASK"] = self.netmask
                network_setting_dict["GATEWAY"] =  self.gateway
                if self.dns1:
                    network_setting_dict["DNS1"] = self.dns1
                if self.dns2:
                    network_setting_dict["DNS2"] = self.dns2
                for item in network_setting_dict.items():
                    key, value = item
                    stetting_content += "%s=%s\n" % (key, value)
            else:
                return False
            file_handler = open(path, "w")
            file_handler.write(stetting_content)
            file_handler.close()
            return True
        else:
            return False
