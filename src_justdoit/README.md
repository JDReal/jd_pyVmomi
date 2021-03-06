# folder_operations.py

包含了对文件夹的新建、删除、重命名等操作。

# vm_operations.py

`vm_operations.py` 内定义了虚拟机类`VirtualMachine`

```python
def __init__(self, name, pfolder, cloudid):
    self.__name = name          # 虚拟机名字
    self.__pfolder = pfolder    # 虚拟机的父文件夹
    self.__cloudid = cloudid    # 虚拟机所属虚拟化环境的 ID
```

- 我们有多套虚拟化环境由不同的 vCenter 管理，定义`cloudid`来区分不通的虚拟化环境



该类具有若干方法，挑选几个重要的介绍如下

### vm_clone()

该方法用来克隆虚拟机，会用到虚拟机的 [CloneVM_Task](https://vdc-download.vmware.com/vmwb-repository/dcr-public/790263bc-bd30-48f1-af12-ed36055d718b/e5f17bfc-ecba-40bf-a04f-376bbb11e811/vim.VirtualMachine.html#clone) 

需要指定新虚机所在的文件夹、虚机名字以及**虚拟机配置文件 [VirtualMachineCloneSpec](https://vdc-download.vmware.com/vmwb-repository/dcr-public/790263bc-bd30-48f1-af12-ed36055d718b/e5f17bfc-ecba-40bf-a04f-376bbb11e811/vim.vm.CloneSpec.html)**。根据文档，在配置文件内自定义好自己需要的参数即可。



### vm_clone_with_ip()

在 vm_clone() 方法的基础上增加了为新克隆的虚机配置 IP 的操作，详细见下面对方法 `vm_configure_ipaddress()` 的说明

:bulb::bulb::bulb:**要注意的是，要注意的是，要注意的是，**虚拟机的名字 `newvm` 不要包含下划线 “_“，圆点符 "."

```python
ident = vim.vm.customization.LinuxPrep()
ident.hostName = vim.vm.customization.FixedName()
ident.hostName.name = newvm
```

如果 `newvm` 包含了下划线，圆点符，空格或者纯粹由数字组成，则会报错（虚拟机能正常克隆完毕，但是 IP 无法配置上）：

```python
[ERROR]: (vmodl.fault.InvalidArgument) {
   dynamicType = <unset>,
   dynamicProperty = (vmodl.DynamicProperty) [],
   msg = 'A specified parameter was not correct: spec.identity.hostName',
   faultCause = <unset>,
   faultMessage = (vmodl.LocalizableMessage) [],
   invalidProperty = 'spec.identity.hostName'
}
```
另外，我们的虚机名字可能为中文，所以`ident.hostName.name`统一设置成了 `vmcentos`

参考：

- https://www.ibm.com/docs/en/cmwo/4.3.0.0?topic=customizations-customizing-network-settings-vmware-linux-guests
- https://github.com/ansible/ansible/issues/27096



### vm_configure_ipaddress()

该方法用来给虚拟机配置 IP 地址。

该方法用到了虚拟机的 [CustomizeVM_Task](https://vdc-download.vmware.com/vmwb-repository/dcr-public/790263bc-bd30-48f1-af12-ed36055d718b/e5f17bfc-ecba-40bf-a04f-376bbb11e811/vim.VirtualMachine.html#customize) 方法，通过指定虚机配置文件 [CustomizationSpec](https://vdc-download.vmware.com/vmwb-repository/dcr-public/790263bc-bd30-48f1-af12-ed36055d718b/e5f17bfc-ecba-40bf-a04f-376bbb11e811/vim.vm.customization.Specification.html) 中的 **nicSettingMap** 来给虚拟机配置 IP。**nicSettingMap** 用来给网络适配器配置指定的 IP，正是我们需要的。

nicSettingMap 是一个列表，每个元素是一个网络适配器对象，该对象包含了虚机的IP地址，掩码，网关等信息。

该列表的长度（即 IP 的个数）应该等于虚拟机网络适配器的个数，否则会报错。

参数 newip 是一个列表，元素是 IP 地址。通过遍历该列表，为 nicSettingMap  赋值。

:bulb::bulb::bulb:**要注意的是，要注意的是，要注意的是，**虚拟机的名字不要包含下划线“_“。

:bulb:要注意的是，CustomizeVM_TASK 要求虚机处于关机状态。



# 附录

`vm_operations.py` 所有实现的虚机的方法列表

| 方法                                                         | 说明                                            |
| ------------------------------------------------------------ | ----------------------------------------------- |
| vm_exist_check(self)                                         | 检查在 pfolder（父文件夹）下是否存在虚机 vmname |
| get_vm_obj(self)                                             | 获取 pfolder 和 vmname 对象，不存在则返回 None  |
| vm_clone(self, newvm, newvmpfolder, newvmhost, newvmdatastore) | **克隆虚机**                                    |
| vm_delete(self)                                              | 删除虚机                                        |
| vm_rename(self, newname)                                     | 重命名虚机                                      |
| vm_poweroff(self)                                            | 关闭虚机电源                                    |
| vm_poweron(self)                                             | 开启虚机电源                                    |
| vm_reboot(self)                                              | 重启虚机                                        |
| vm_snapshot_create(self)                                     | 给虚机打快照                                    |
| vm_snapshot_delete(self, snapshot_name)                      | 删除指定快照                                    |
| vm_snapshot_revert(self, snapshot_name)                      | 恢复到指定快照                                  |
| vm_snapshot_delete_all(self)                                 | 删除所有快照                                    |
| vm_reconfigure_mem(self, newmemsize)                         | 重新配置虚机内存大小                            |
| vm_reconfigure_cpu(self, newcpunum)                          | 重新配置虚机 CPU 个数                           |
| vm_reconfigure_nic_add(self, newnicname)                     | 给虚机添加一张网卡                              |
| vm_reconfigure_nic_remove(self, nicnumber)                   | 删除指定的网卡                                  |
| vm_reconfigure_disk_add(self, disksize)                      | 给虚机添加一块磁盘                              |
| vm_reconfigure_disk_remove(self, disknumber)                 | 删除指定的一块磁盘                              |
| vm_configure_ipaddress(self, newip)                          | 给虚机配置 IP                                   |
| vm_relocate(self, host, datastore)                           | **迁移虚拟机**                                  |

