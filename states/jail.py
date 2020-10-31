import salt.exceptions


def status(name):
    """
    Check jail status

    This checks the status of jails, are they running or dead?
    """

    ret = {
        "name": name,
        "changes": {},
        "result": False,
        "comment": "",
    }

    # Check the current state of jails.
    current_state = __salt__["jail.status"](name)
    if current_state is True:
        ret["result"] = True
        ret["comment"] = 'Jail "{0}" is already running'.format(name)
        return ret
    if current_state is False:
        ret["result"] = False
        ret["comment"] = 'Jail "{0}" is not running'.format(name)
        return ret

    if __opts__["test"] is True:
        ret["result"] = None
        ret["comment"] = 'Jail "{0}" is not running.'.format(name)
        ret["changes"] = {
            "old": current_state,
            "new": 'Jail "{0}" is to be started.'.format(name),
        }
        return ret

    return ret


def start(name):
    """
    Start Jail

    This will allow the starting of jails as a state.

    """

    ret = {
        "name": name,
        "changes": {},
        "result": False,
        "comment": "",
    }
    current_state = __salt__["jail.status"](name)
    if current_state is True:
        ret["result"] = True
        ret["comment"] = 'Jail "{0}" is already running'.format(name)
        return ret
    if current_state is False:
        new_state = __salt__["jail.start"](name)
        ret["result"] = True
        ret["comment"] = 'Jail "{0}" was started'.format(name)
        ret["changes"] = {
            "old": current_state,
            "new": new_state,
        }
        return ret

    if __opts__["test"] is True:
        ret["result"] = None
        ret["comment"] = 'Jail "{0}" is not running.'.format(name)
        ret["changes"] = {
            "old": current_state,
            "new": 'Starting Jail "{0}"'.format(name),
        }

        return ret

    return ret


def stop(name):
    """
    Stop Jail

    This will allow the Stopping of jails as a state.

    """

    ret = {
        "name": name,
        "changes": {},
        "result": False,
        "comment": "",
    }
    current_state = __salt__["jail.status"](name)
    if current_state is True:
        new_state = __salt__["jail.stop"](name)
        ret["result"] = True
        ret["comment"] = 'Jail "{0}" is running'.format(name)
        ret["changes"] = {
            "old": current_state,
            "new": new_state,
        }
        return ret
    if current_state is False:
        ret["result"] = True
        ret["comment"] = 'Jail "{0}" is already stopped'.format(name)
        return ret

    if __opts__["test"] is True:
        ret["result"] = None
        ret["comment"] = 'Jail "{0}" is running.'.format(name)
        ret["changes"] = {
            "old": current_state,
            "new": 'stopping Jail "{0}"'.format(name),
        }

        return ret

    return ret


def restart(name):
    """
    Restart Jail

    This will allow the restarting of jails as a state.

    """

    ret = {
        "name": name,
        "changes": {},
        "result": False,
        "comment": "",
    }

    current_state = __salt__["jail.status"](name)

    if current_state is True:
        new_state = __salt__["jail.restart"](name)
        ret["result"] = True
        ret["comment"] = 'Jail "{0}" was restarted'.format(name)
        ret["changes"] = {
            "old": 'Jail "{0}" was running'.format(name),
            "new": 'Restarting Jail "{0}"'.format(name),
        }
        return ret
    if current_state is False:
        new_state = __salt__["jail.restart"](name)
        ret["result"] = True
        ret["comment"] = 'Jail "{0}" was restarted'.format(name)
        ret["changes"] = {
            "old": 'Jail "{0}" was not running'.format(name),
            "new": 'Starting Jail "{0}"'.format(name),
        }
        return ret

    if __opts__["test"] is True:
        ret["result"] = None
        ret["comment"] = 'Jail "{0}" is not running.'.format(name)
        ret["changes"] = {
            "old": current_state,
            "new": 'Restarting Jail "{0}"'.format(name),
        }
        return ret

    return ret


def manage(name, jailloc, version, arch, jail_files, jail_txz, freebsd_mirror, snapshot=False, rollback=False, lib32=False, src=False):
    """
    Manage jail

    Manage release of jail
    """

    ret = {
        "name": name,
        "changes": {},
        "result": False,
        "comment": "",
    }
    pass_opt = __opts__["test"]
    jailversion = __salt__["grains.get"]('jail:jail_{0}_installed'.format(name))
    jail_manage = __salt__["jail.manage"](jail_files, version, jailloc, name, snapshot, lib32, src, pass_opt)

    if __salt__["jail.status"](name) is True and jailversion != version and pass_opt is False:
        if jail_manage is True:
            ret["result"] = True
            ret["comment"] = 'Jail "{0}" is upgraded and restarted'.format(name)
            ret["changes"] = {
                "new": "{0}".format(version),
                "old": str(jailversion),
                }
            return ret
        if jail_manage is False:
            ret["result"] = False
            ret["comment"] = 'Jail "{0}" failed to upgrade'.format(name)
            return ret

    if jailversion == version:
        ret["result"] = True
        ret["comment"] = 'Jail "{0}" is current version "{1}"'.format(name, version)
        return ret

    if __opts__["test"] is True and jailversion == version:
        ret["result"] = None
        ret["comment"] = 'Jail "{0}" is current version.'.format(name, version)
        return ret

    if __opts__["test"] is True and jailversion != version:
        ret["result"] = None
        ret["comment"] = 'Jail "{0}" needs updating.'.format(name)
        ret["changes"] = {
            "new": "{0}".format(version),
            "old": str(jailversion),
        }

        return ret

    return ret
