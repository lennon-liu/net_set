import unittest
import requests
import json
class UserCase(unittest.TestCase):

    def testAddUser(self):
        ret = requests.post(url="http://192.168.214.131:8500/get_addr_info")
        print ret.json()
        self.assertTrue(ret.json().get("status"),True)

    def testDelUser(self):
        ret = requests.post(url="http://192.168.214.131:8500/auto_setting",timeout=10)
        self.assertTrue(ret.json().get("status"),True)

    def testauto_setting(self):
        content = {"ipaddr": "192.168.214.189", "netmask": "255.255.255.0", "gateway": "192.168.214.2","dns1": "", "dns2": ""}
        ret = requests.post(url="http://192.168.214.131:8500/manual_setting",json=content,timeout=10)
        print ret.json()
        self.assertTrue(ret.json().get("status"),True)

if __name__ == '__main__':
    suite = unittest.TestSuite(map(UserCase,['testAddUser','testDelUser',"testauto_setting"]))
    suite2 = unittest.TestSuite()
    suite2.addTests(map(UserCase,['testAddUser','testDelUser',"testauto_setting"]))
    suite3 = unittest.TestSuite()
    suite3.addTest(UserCase('testAddUser'))
    suite3.addTest(UserCase('testDelUser'))
    suite3.addTest(UserCase('testauto_setting'))
