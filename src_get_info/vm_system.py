#!/usr/bin/env python3

"""
Written by jdreal.
Github:

Get the information about vm 2nd-level folders.
"""

from src_share import get_obj_id, vcenter_instance_check

global allDict
allDict = {}


def vm_folders(vmfolder, cloudid):
    """
    递归获取所有项目的文件夹
    """
    # if hasattr(vmfolder, 'childEntity'):
    #     for vmf in vmfolder.childEntity:
    #         vm_folders(vmf)
    for vmf in vmfolder.childEntity:
        if hasattr(vmf, 'childEntity'):
            vm_folders(vmf, cloudid)

    folderName = vmfolder.name

    folderDict = {"SYSID": get_obj_id.id(vmfolder),
                  "SYSNAME": folderName,
                  "CHKTIME": '',
                  "DESCRIPTION": '',
                  "ID": '',
                  "CLOUD": cloudid}

    allDict[folderName] = folderDict

    return allDict


def get_vm_system(cloudid):
    """
    打印第二层次的虚拟机文件夹，对应到 系统 的概念
    """

    si_content = vcenter_instance_check.vc_instance_check(cloudid)
    # 新增判断，当传入了错误的 cloudid 时，vc_instance_check() 返回的是一个包含错误信息的字典
    # 此时第 53 行给 datacenter 赋值的语句会报错
    if isinstance(si_content, dict):
        return si_content

    # if isinstance(si_content, vim.ServiceInstanceContent)
    datacenter = si_content.rootFolder.childEntity[0]
    datacenterName = datacenter.name

    secondFolderDict = {}
    topVmFolder = datacenter.vmFolder.childEntity[0]

    folderDict = vm_folders(topVmFolder, cloudid)
    return folderDict


if __name__ == "__main__":
    cloudid = 7
    print(get_vm_system(cloudid))
