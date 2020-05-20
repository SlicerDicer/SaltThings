import salt.exceptions


def status(name):
    '''
    Check jail status

    This checks the status of jails, are they running or dead?
    '''

    ret = {
        'name': name,
        'changes': {},
        'result': False,
        'comment': '',
        }

    # Check the current state of jails.
    current_state = __salt__['jail.status'](name)
    if current_state is True:
        ret['result'] = True
        ret['comment'] = 'Jail "{0}" is already running'.format(name)
        return ret
    if current_state is False:
        ret['result'] = False
        ret['comment'] = 'Jail "{0}" is not running'.format(name)
        return ret

    if __opts__['test'] is True:
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
    if current_state == False:
        new_state = __salt__['jail.start'](name)
        ret['result'] = True
        ret['comment'] = 'Jail "{0}" was started'.format(name)
        ret['changes'] = {
            'old': current_state,
            'new': new_state,
        }
        return ret

    if __opts__['test'] == True:
        ret['result'] = None
        ret['comment'] = 'Jail "{0}" is not running.'.format(name)
        ret['changes'] = {
            'old': current_state,
            'new': 'Starting Jail "{0}"'.format(name),
        }

        return ret

    return ret


def stop(name):
    '''
    Stop Jail

    This will allow the Stopping of jails as a state.

    '''

    ret = {
        'name': name,
        'changes': {},
        'result': False,
        'comment': '',
        }
    current_state = __salt__['jail.status'](name)
    if current_state == True:
        new_state = __salt__['jail.stop'](name)
        ret['result'] = True
        ret['comment'] = 'Jail "{0}" is running'.format(name)
        ret['changes'] = {
            'old': current_state,
            'new': new_state,
        }
        return ret
    if current_state == False:
        ret['result'] = True
        ret['comment'] = 'Jail "{0}" is already stopped'.format(name)
        return ret

    if __opts__['test'] == True:
        ret['result'] = None
        ret['comment'] = 'Jail "{0}" is running.'.format(name)
        ret['changes'] = {
            'old': current_state,
            'new': 'stopping Jail "{0}"'.format(name),
        }

        return ret

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

    if current_state is True:
        new_state = __salt__['jail.restart'](name)
        ret['result'] = True
        ret['comment'] = 'Jail "{0}" was restarted'.format(name)
        ret['changes'] = {
            'old': 'Jail "{0}" was running'.format(name),
            'new': 'Restarting Jail "{0}"'.format(name),
        }
        return ret
    if current_state is False:
        new_state = __salt__['jail.restart'](name)
        ret['result'] = True
        ret['comment'] = 'Jail "{0}" was restarted'.format(name)
        ret['changes'] = {
            'old': 'Jail "{0}" was not running'.format(name),
            'new': 'Starting Jail "{0}"'.format(name),
        }
        return ret

    if __opts__['test'] == True:
        ret['result'] = None
        ret['comment'] = 'Jail "{0}" is not running.'.format(name)
        ret['changes'] = {
            'old': current_state,
            'new': 'Restarting Jail "{0}"'.format(name),
        }
        return ret

    return ret


def upgrade(name, jailloc, version, jail_files, snapshot=False):
    '''
    upgrade jail

    to upgrade release of jail
    '''

    ret = {
        'name': name,
        'changes': {},
        'result': False,
        'comment': '',
        }
    switch = ''
    loclist = ['var/empty', 'lib', 'bin', 'sbin',
               'usr/bin', 'usr/lib', 'usr/lib32',
               'usr/libexec', 'usr/sbin', 'libexec']
    jailversion = __salt__['grains.get']('jail:jail_' + name + '_installed')

    if jailversion != version and rollback is False:

        if __salt__['zfs.exists'](jailloc[1:-1]) == False:
            __salt__['zfs.create'](jailloc[1:-1])

        if __salt__['jail.status'](name) is True:
            __salt__['jail.stop'](name)

        if snapshot is True:
            __salt__['zfs.snapshot'](jailloc[1:-1] + '@' + jailversion)

        for data in loclist:
            data = '{0}{1}'.format(jailloc, data)
            if __salt__['file.directory_exists'](data) is True:
                filelist = __salt__['file.readdir'](data)
                for files in filelist:
                    truepath = data + '/' + files
                    schgdata = __salt__['chflags.change'](switch, 'noschg', truepath)

        __salt__['archive.tar']('xzf', jail_files + str(version) + '/base.txz', dest=jailloc)
        __salt__['archive.tar']('xzf', jail_files + str(version) + '/lib32.txz', dest=jailloc)

        __salt__['jail.start'](name)

        if __salt__['jail.status'](name) is True:
            ret['result'] = True
            ret['comment'] = 'Jail "{0}" is upgraded and restarted'.format(name)
            ret['changes'] = {
                'new': '{0}'.format(version),
                'old': str(jailversion),
                }
            return ret
        if __salt__['jail.status'](name) is False:
            ret['result'] = False
            ret['comment'] = 'Jail "{0}" is upgraded and failed to restart'.format(name)
            ret['changes'] = {
                'new': '{0}'.format(version),
                'old': str(jailversion),
                }
            return ret
        return ret
    if jailversion == version:
        ret['result'] = True
        ret['comment'] = 'Jail "{0}" is current version "{1}"'.format(name, version)
        return ret

    if __opts__['test'] is True:
        ret['result'] = None
        ret['comment'] = 'Jail "{0}" needs updating.'.format(name)
        ret['changes'] = {
            'new': '{0}'.format(version),
            'old': str(jailversion),
        }

        return ret

    return ret
