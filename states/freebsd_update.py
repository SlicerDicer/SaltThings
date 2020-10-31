import salt.exceptions


def manage(name, version, host_files, lib32=False, src=False):
    """
    upgrade host

    to upgrade release of host

    name:
        Name of system
    version:
        Version represented in 12.1
    host_files:
        system files used.
    """

    ret = {
        "name": name,
        "changes": {},
        "result": False,
        "comment": "",
    }

    pass_opt = __opts__["test"]
    host_version = __salt__["grains.get"]("release_version")
    if host_version != version and pass_opt is False:
        freebsd_manage = __salt__["freebsd_update.manage"](host_files, version, lib32, src, pass_opt)
        ret["result"] = True
        ret["comment"] = 'System "{0}" is upgraded please reboot'.format(name)
        ret["changes"] = {
            "new": "{0}".format(version),
            "old": host_version,
        }
        return ret
    if host_version == version and pass_opt is False:
        ret["result"] = True
        ret["comment"] = 'Host "{0}" is current version "{1}"'.format(name, version)
        return ret

    if host_version != version and pass_opt is True:
        ret["result"] = True
        ret["comment"] = 'Host "{0}" needs update to version "{1}"'.format(name, version)
        ret["changes"] = {
            "new": "{0}".format(version),
            "old": str(host_version),
        }
        return ret

    if host_version == version and pass_opt is True:
        ret["result"] = True
        ret["comment"] = 'Host "{0}" is at version {1}.'.format(name, host_version)
        return ret

    return ret
