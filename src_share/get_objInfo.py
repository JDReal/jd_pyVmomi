#!/usr/bin/env python3

"""
Written by jdreal.
Github: 


"""

from src_share import vc_login, vcenter_instance_check


def get_obj(cloudid, vimtype, name):
    """
    cloudid: 确定是在哪个vc下寻找对象
    Return an object by name, if name is None the
    first found object is returned
    """
    content = vcenter_instance_check.vc_instance_check(cloudid)

    obj = None

    container = content.viewManager.CreateContainerView(
        content.rootFolder, vimtype, True)
    for c in container.view:
        if name:
            if c.name == name:
                obj = c
                break
        else:
            obj = c
            break

    return obj


if __name__ == "__main__":
    si = vc_login.vclogin()
    content = si.RetrieveContent()
