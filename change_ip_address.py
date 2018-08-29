from python_terraform import *
import atexit
from pyVim import connect
from pyVmomi import vmodl
from pyVmomi import vim


def power_off_on():



def change_port_group():
   # https: // github.com / vmware / pyvmomi - community - samples / blob / master / samples / change_vm_vif.py

def guest_os():




def get_obj(content, vimtype, name):
    obj = None
    container = content.viewManager.CreateContainerView(content.rootFolder, vimtype, True)
    for c in container.view:
        if c.name == name:
            obj = c
            break
    return obj





def linux_change_ip(vm_name, new_ip):
    si = connect.SmartConnectNoSSL(host=vc_host, user=vc_user, pwd=vc_pass, port=443)
    content = si.RetrieveContent()
    vm = get_obj(content, [vim.VirtualMachine], vm_name)
    adaptermap = vim.vm.customization.AdapterMapping()
    globalip = vim.vm.customization.GlobalIPSettings()
    adaptermap.adapter = vim.vm.customization.IPSettings()
    adaptermap.adapter.ip = vim.vm.customization.FixedIp()
    adaptermap.adapter.ip.ipAddress = new_ip
    adaptermap.adapter.subnetMask = new_mask
    adaptermap.adapter.gateway = new_gw_ip
    globalip.dnsServerList = dns_server
    adaptermap.adapter.dnsDomain = dns_prefix
    globalip = vim.vm.customization.GlobalIPSettings()
    ident = vim.vm.customization.LinuxPrep(domain='srv.local', hostName=vim.vm.customization.FixedName(name=vm_name))
    customspec = vim.vm.customization.Specification()
    customspec.identity = ident
    customspec.nicSettingMap = [adaptermap]
    customspec.globalIPSettings = globalip
    task = vm.Customize(spec=customspec)


def windows_change_ip(vm_name, new_ip):
    #https://github.com/vmware/pyvmomi/issues/261
    si = connect.SmartConnectNoSSL(host=vc_host, user=vc_user, pwd=vc_pass, port=443)
    content = si.RetrieveContent()
    vm = get_obj(content, [vim.VirtualMachine], vm_name)
    adaptermap = vim.vm.customization.AdapterMapping()
    globalip = vim.vm.customization.GlobalIPSettings()
    adaptermap.adapter = vim.vm.customization.IPSettings()
    adaptermap.adapter.ip = vim.vm.customization.FixedIp()
    adaptermap.adapter.ip.ipAddress = new_ip
    adaptermap.adapter.subnetMask = new_mask
    adaptermap.adapter.gateway = new_gw_ip
    globalip.dnsServerList = dns_server
    adaptermap.adapter.dnsDomain = dns_prefix
    globalip = vim.vm.customization.GlobalIPSettings()
    ident = vim.vm.customization.Sysprep()
    ident.guiUnattended = vim.vm.customization.GuiUnattended()
    ident.userData = vim.vm.customization.UserData()
    ident.userData.computerName = vim.vm.customization.FixedName()
    ident.userData.computerName.name = vm_name
    ident.identification = vim.vm.customization.Identification()







#
# inputs = {'vcenter_ip': 'vc-linx',
#           'vcenter_password': 'Password123',
#           'vcenter_user': 'Administrator',
#           'vm_name': 'hosturl',
#           'isDHCP': False,
#           'vm_ip': '192.168.222.203',
#           'subnet': '255.255.255.0',
#           'gateway': '192.168.222.1',
#           'dns': ['172.10.10.10', '192.168.245.50'],
#           'domain': 'srv.local'
#           }
#
#
# def get_obj(content, vimtype, name):
#     """
#      Get the vsphere object associated with a given text name
#     """
#     obj = None
#     container = content.viewManager.CreateContainerView(content.rootFolder, vimtype, True)
#     for c in container.view:
#         if c.name == name:
#             obj = c
#             break
#     return obj
#
#
# def wait_for_task(task, actionName='job', hideResult=False):
#     """
#     Waits and provides updates on a vSphere task
#     """
#
#     while task.info.state == vim.TaskInfo.State.running:
#         time.sleep(2)
#
#     if task.info.state == vim.TaskInfo.State.success:
#         if task.info.result is not None and not hideResult:
#             out = '%s completed successfully, result: %s' % (actionName, task.info.result)
#             print
#             out
#         else:
#             out = '%s completed successfully.' % actionName
#             print
#             out
#     else:
#         out = '%s did not complete successfully: %s' % (actionName, task.info.error)
#         raise task.info.error
#         print
#         out
#
#     return task.info.result
#
#
# def main():
#     # args = GetArgs()
#     try:
#         si = None
#         try:
#             print("Trying to connect to VCENTER SERVER . . .")
#             si = connect.SmartConnectNoSSL(host='vc-linx.srv.local', user='nokhrimenko@phoenixit.ru', pwd='NikolonsO345831', port=443)
#         except:
#             pass
#             #atexit.register(Disconnect, si)
#
#         print("Connected to VCENTER SERVER !")
#
#         content = si.RetrieveContent()
#
#         # vm_name = args.vm
#         vm_name = inputs['vm_name']
#         vm = get_obj(content, [vim.VirtualMachine], vm_name)
#
#         if vm.runtime.powerState != 'poweredOff':
#             print("WARNING:: Power off your VM before reconfigure")
#             sys.exit()
#
#         adaptermap = vim.vm.customization.AdapterMapping()
#         globalip = vim.vm.customization.GlobalIPSettings()
#         adaptermap.adapter = vim.vm.customization.IPSettings()
#
#         isDHDCP = inputs['isDHCP']
#         if not isDHDCP:
#             """Static IP Configuration"""
#             adaptermap.adapter.ip = vim.vm.customization.FixedIp()
#             adaptermap.adapter.ip.ipAddress = inputs['vm_ip']
#             adaptermap.adapter.subnetMask = inputs['subnet']
#             adaptermap.adapter.gateway = inputs['gateway']
#             globalip.dnsServerList = inputs['dns']
#
#         else:
#             """DHCP Configuration"""
#             adaptermap.adapter.ip = vim.vm.customization.DhcpIpGenerator()
#
#         adaptermap.adapter.dnsDomain = inputs['domain']
#
#         globalip = vim.vm.customization.GlobalIPSettings()
#
#         # For Linux . For windows follow sysprep
#         ident = vim.vm.customization.LinuxPrep(domain=inputs['domain'], hostName=vim.vm.customization.FixedName(name=vm_name))
#
#
#
#         customspec = vim.vm.customization.Specification()
#         # For only one adapter
#         customspec.identity = ident
#         customspec.nicSettingMap = [adaptermap]
#         customspec.globalIPSettings = globalip
#
#         # Configuring network for a single NIC
#         # For multipple NIC configuration contact me.
#
#         print("Reconfiguring VM Networks . . .")
#
#         task = vm.Customize(spec=customspec)
#
#         # Wait for Network Reconfigure to complete
#         wait_for_task(task, si)
#
#
#
#
#
# # Start program
# if __name__ == "__main__":
#     main()
#
# si = connect.SmartConnectNoSSL(host='vc-linx.srv.local', user='nokhrimenko@phoenixit.ru', pwd='NikolonsO345831', port=443)
#
# content = si.RetrieveContent()
# vm_name = 'host-test'
#
# def get_obj(content, vimtype, name):
#     """
#      Get the vsphere object associated with a given text name
#     """
#     obj = None
#     container = content.viewManager.CreateContainerView(content.rootFolder, vimtype, True)
#     for c in container.view:
#         if c.name == name:
#             obj = c
#             break
#     return obj
#
#
#
# vm = get_obj(content, [vim.VirtualMachine], vm_name)
#
#
# adaptermap = vim.vm.customization.AdapterMapping()
# globalip = vim.vm.customization.GlobalIPSettings()
# adaptermap.adapter = vim.vm.customization.IPSettings()
# adaptermap.adapter.ip = vim.vm.customization.FixedIp()
# adaptermap.adapter.ip.ipAddress = '192.168.222.203'
# adaptermap.adapter.subnetMask = '255.255.255.0'
# adaptermap.adapter.gateway = '192.168.222.1'
# globalip.dnsServerList = ['172.10.10.10', '192.168.245.50']
# adaptermap.adapter.dnsDomain = 'srv.ru'
# globalip = vim.vm.customization.GlobalIPSettings()
# #hostname_ = vim.vm.customization.FixedName(name=vm_name)
# ident = vim.vm.customization.LinuxPrep(domain='srv.local', hostName=vim.vm.customization.FixedName(name=vm_name))
#
#
#
# ident = vim.vm.customization.Sysprep(hostName = 'test', guiUnattended=vim.vm.customization.GuiUnattended(), userData = vim.vm.customization.UserData(computerName = vim.vm.customization.NameGenerator(), identification = vim.vm.customization.Identification()))
# customspec = vim.vm.customization.Specification()
# customspec.identity = ident
# customspec.nicSettingMap = [adaptermap]
# customspec.globalIPSettings = globalip
# task = vm.Customize(spec=customspec)
#
# task = vm.Customize(spec=customspec)

