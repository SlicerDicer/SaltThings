def enable(name, jail=None):
    '''
    Enable Jail Services

    This will allow the enable of jails service as a state.

    '''

    ret = {
        'name': name,
        'changes': {},
        'result': False,
        'comment': '',
        }
    enhanced_state = ''
    current_state = __salt__['service.get_enabled'](jail=jail)
    for data in current_state:
        if data == name:
            enhanced_state = data
    if enhanced_state != name:
        new_state = __salt__['service.enable'](name, jail=jail)
        ret['result'] = True
        ret['comment'] = 'Service "{0}" is Enabled'.format(name, jail=jail)
        ret['changes'] = {
            'old': current_state,
            'new': new_state,
        }
        return ret
    if enhanced_state == name:
        ret['result'] = True
        ret['comment'] = 'Service "{0}" is already enabled'.format(name, jail=jail)
        return ret

    if __opts__['test'] == True:
        ret['result'] = None
        ret['comment'] = 'Service "{0}" is disabled.'.format(name, jail=jail)
        ret['changes'] = {
            'old': current_state,
            'new': 'enabling service "{0}"'.format(name, jail=jail),
        }

        return ret

    return ret

def disable(name, jail=None):
    '''
    Disable Jail Service

    This will allow the disabling of jails service as a state.

    '''

    ret = {
        'name': name,
        'changes': {},
        'result': False,
        'comment': '',
        }
    enhanced_state = ''
    current_state = __salt__['service.get_disabled'](jail=jail)
    for data in current_state:
        if data == name:
            enhanced_state = data
    if enhanced_state != name:
        new_state = __salt__['service.disable'](name, jail=jail)
        ret['result'] = True
        ret['comment'] = 'Service "{0}" is disabled'.format(name, jail=jail)
        ret['changes'] = {
            'old': '"{0}" was enabled'.format(name),
            'new': '"{0}" is disabled'.format(name),
        }
        return ret
    if enhanced_state == name:
        ret['result'] = True
        ret['comment'] = 'Service "{0}" is already disabled'.format(name, jail=jail)
        return ret

    if __opts__['test'] == True:
        ret['result'] = None
        ret['comment'] = 'Service "{0}" is enabled.'.format(name, jail=jail)
        ret['changes'] = {
            'old': current_state,
            'new': 'disabling service "{0}"'.format(name, jail=jail),
        }

        return ret

    return ret


def status(name, jail=None):
    '''
    Check jail service status

    This checks the status of service on jails, are they running or dead?
    '''

    ret = {
        'name': name,
        'changes': {},
        'result': False,
        'comment': '',
        }
    # Check the current state of jails.
    current_state = __salt__['service.available'](name, jail=jail)
    if current_state is True:
        ret['result'] = True
        ret['comment'] = 'Service "{0}" is already running'.format(name, jail=jail)
        return ret
    if current_state is False:
        ret['result'] = False
        ret['comment'] = 'Service "{0}" is not running'.format(name, jail=jail)
        return ret

    if __opts__['test'] is True:
        ret['result'] = None
        ret['comment'] = 'Service "{0}" is not running.'.format(name, jail=jail)
        ret['changes'] = result
        return ret

    return ret


def running(name, jail=None, enable=None):
    '''
    Start Jail Service

    This will allow the starting of jails service as a state.

    '''

    ret = {
        'name': name,
        'changes': {},
        'result': False,
        'comment': '',
        'enable': True,
        }
    if enable is True:
        enhanced_state = ''
        current_state = __salt__['service.get_enabled'](jail=jail)
        for data in current_state:
            if data == name:
                enhanced_state = data
        if enhanced_state != name:
            new_state = __salt__['service.enable'](name, jail=jail)
            ret['enable'] = True
            ret['changes'] = {
                'old': 'Jail {0} service {1} disabled'.format(jail, name),
                'new': 'Jail {0} service {1} enabled'.format(jail, name),
                }
        if enhanced_state is name:
            ret['enable'] = True
    if enable is False:
        disable(name, jail=jail)

    current_state = __salt__['service.available'](name, jail=jail)
    if current_state == True:
        ret['result'] = True
        ret['comment'] = 'Service "{0}" is already running'.format(name, jail=jail)
        return ret
    if current_state == False:
        new_state = __salt__['service.start'](name, jail=jail)
        ret['result'] = True
        ret['comment'] = 'Service "{0}" was started'.format(name, jail=jail)
        ret['changes'] = {
            'old': current_state,
            'new': new_state,
        }
        return ret

    if __opts__['test'] == True:
        ret['result'] = None
        ret['comment'] = 'Service "{0}" is not running.'.format(name, jail=jail)
        ret['changes'] = {
            'old': current_state,
            'new': 'Starting service "{0}"'.format(name, jail=jail),
        }

        return ret

    return ret


def stop(name, jail=None):
    '''
    Stop Jail Service

    This will allow the Stopping of jails service as a state.

    '''

    ret = {
        'name': name,
        'changes': {},
        'result': False,
        'comment': '',
        }
    current_state = __salt__['service.available'](name, jail=jail)
    if current_state == True:
        new_state = __salt__['service.stop'](name, jail=jail)
        ret['result'] = True
        ret['comment'] = 'Service "{0}" is running'.format(name, jail=jail)
        ret['changes'] = {
            'old': current_state,
            'new': new_state,
        }
        return ret
    if current_state == False:
        ret['result'] = True
        ret['comment'] = 'Service "{0}" is already stopped'.format(name, jail=jail)
        return ret

    if __opts__['test'] == True:
        ret['result'] = None
        ret['comment'] = 'Service "{0}" is running.'.format(name, jail=jail)
        ret['changes'] = {
            'old': current_state,
            'new': 'stopping service "{0}"'.format(name, jail=jail),
        }

        return ret

    return ret


def restart(name, jail=None):
    '''
    Restart Jail Service

    This will allow the restarting of jails service as a state.

    '''

    ret = {
        'name': name,
        'changes': {},
        'result': False,
        'comment': '',
        }

    current_state = __salt__['service.available'](name, jail=jail)

    if current_state is True:
        new_state = __salt__['service.restart'](name, jail=jail)
        ret['result'] = True
        ret['comment'] = 'Service "{0}" was restarted'.format(name, jail=jail)
        ret['changes'] = {
            'old': 'Service "{0}" was running'.format(name, jail=jail),
            'new': 'Restarting Service "{0}"'.format(name, jail=jail),
        }
        return ret
    if current_state is False:
        new_state = __salt__['service.restart'](name, jail=jail)
        ret['result'] = True
        ret['comment'] = 'Jail "{0}" was restarted'.format(name, jail=jail)
        ret['changes'] = {
            'old': 'Service "{0}" was not running'.format(name, jail=jail),
            'new': 'Starting Service "{0}"'.format(name, jail=jail),
        }
        return ret

    if __opts__['test'] == True:
        ret['result'] = None
        ret['comment'] = 'Service "{0}" is not running.'.format(name, jail=jail)
        ret['changes'] = {
            'old': current_state,
            'new': 'Restarting Service "{0}"'.format(name, jail=jail),
        }
        return ret

    return ret
