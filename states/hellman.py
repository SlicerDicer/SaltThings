import salt.exceptions


def create(name, bits):
    """
    Create dhparams


    """

    ret = {
        "name": name,
        "changes": {},
        "result": False,
        "comment": "",
    }

    # Check the current state of dhprams.
    current_state = __salt__["dhparam.check"](name)
    if current_state is True:
        ret["result"] = True
        ret["comment"] = 'file "{0}" is already created'.format(name)
        return ret
    if current_state is False:
        __salt__["dhparam.create"](name, bits)
        ret["result"] = False
        ret["comment"] = 'file "{0}" is created'.format(name)
        return ret

    if __opts__["test"] is True:
        ret["result"] = None
        ret["comment"] = 'file "{0}" is not created.'.format(name)
        ret["changes"] = {
            "old": current_state,
            "new": 'File "{0}" is to be creaed.'.format(name),
        }
        return ret

    return ret
