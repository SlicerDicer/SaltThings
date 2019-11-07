import salt.exceptions


def status(name):
    '''
    Check jail status

    This checks the status of jails, are they running or dead?

    name
        jailname
    '''

    ret = {
        'name': name,
        'changes': {},
        'result': False,
        'comment': '',
        }

    # Check the current state of jails.
    current_state = __salt__['jail.status'](name)
    if current_state == True:
        ret['result'] = True
        ret['comment'] = 'Jail "{0}" is already running'.format(name)
        return ret
    if current_state == False:
        ret['result'] = False
        ret['comment'] = 'Jail "{0}" is not running'.format(name)
        return ret
    # The state of the system does need to be changed. Check if we're running
    # in ``test=true`` mode.
    if __opts__['test'] == True:
        ret['result'] = None
        ret['comment'] = 'Jail "{0}" is not running.'.format(name)
        ret['changes'] = result

        return ret

    return ret


def start(name):
    '''
    Start Jail

    This will allow the starting of jails as a state.

    '''

    ret = {
        'name': name,
        'changes': {},
        'result': False,
        'comment': '',
        }
    current_state = __salt__['jail.status'](name)
    if current_state == True:
        ret['result'] = True
        ret['comment'] = 'Jail "{0}" is already running'.format(name)
        return ret
    if __opts__['test'] == True:
        ret['result'] = None
        ret['comment'] = 'Jail "{0}" is not running.'.format(name)
        ret['changes'] = {
            'old': current_state,
            'new': 'Starting Jail "{0}"'.format(name),
        }

        return ret

    new_state = __salt__['jail.start'](name)

    ret['comment'] = 'Jail "{0}" was started'.format(name)

    ret['changes'] = {
        'old': current_state,
        'new': new_state,
    }

    ret['result'] = True

    return ret


def restart(name):
    '''
    Restart Jail

    This will allow the restarting of jails as a state.

    '''

    ret = {
        'name': name,
        'changes': {},
        'result': False,
        'comment': '',
        }

    current_state = __salt__['jail.status'](name)

    if __opts__['test'] == True:
        ret['result'] = None
        ret['comment'] = 'Jail "{0}" is not running.'.format(name)
        ret['changes'] = {
            'old': current_state,
            'new': 'Restarting Jail "{0}"'.format(name),
        }

        return ret

    new_state = __salt__['jail.restart'](name)

    ret['comment'] = 'Jail "{0}" was restarted'.format(name)

    ret['changes'] = {
        'old': current_state,
        'new': new_state,
    }

    ret['result'] = True

    return ret
