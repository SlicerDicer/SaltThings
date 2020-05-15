import salt.exceptions


def report(name):
    '''
    Report chflags

    This reports the status of chflags
    '''

    ret = {
        'name': name,
        'changes': {},
        'result': False,
        'comment': '',
        }

    # Check the current state of jails.
    current_state = __salt__['chflags.report'](name)
    if current_state is not False:
        ret['result'] = True
        ret['comment'] = 'File "{0}" exists'.format(name), current_state
        return ret
    if current_state == False:
        ret['result'] = False
        ret['comment'] = 'File "{0}" does not exist'.format(name), current_state
        return ret
    # The state of the system does need to be changed. Check if we're running
    # in ``test=true`` mode.
    if __opts__['test'] == True:
        ret['result'] = None
        ret['comment'] = 'File "{0}" exists.'.format(name), current_state
        ret['changes'] = result

        return ret

    return ret



def change(name, switch, flag):
    '''
    Change chflag

    This will allow changing chflags as a state.

    '''

    ret = {
        'name': name,
        'switch': switch,
        'flag': flag,
        'changes': {},
        'result': False,
        'comment': '',
        }
    current_state = __salt__['chflags.report'](name)

    for data in current_state:
        if data == flag:
            ret['result'] = True
            ret['comment'] = 'chflag "{0}" is already set'.format(flag)
            return ret
            break

    if __opts__['test'] == True:
        ret['result'] = None
        ret['comment'] = 'chflag "{0}" is not set.'.format(flag)
        ret['changes'] = {
            'old': current_state,
            'new': 'setting chflag "{0}"'.format(flag),
        }
        return ret

    if current_state is not False:
        new_state = __salt__['chflags.change'](switch, flag, name)
        ret['result'] = True
        ret['comment'] = 'chflags "{0}" is set'.format(flag)
        ret['changes'] = {
            'old': current_state,
            'new': flag + current_state,
        }
        return ret

    return ret
