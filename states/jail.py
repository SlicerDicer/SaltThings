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
        ret['changes'] = {
            'old': current_state,
            'new': 'Jail "{0}" is to be started.'.format(name),
        }
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
    if current_state is True:
        ret['result'] = True
        ret['comment'] = 'Jail "{0}" is already running'.format(name)
        return ret
    if current_state is False:
        new_state = __salt__['jail.start'](name)
        ret['result'] = True
        ret['comment'] = 'Jail "{0}" was started'.format(name)
        ret['changes'] = {
            'old': current_state,
            'new': new_state,
        }
        return ret

    if __opts__['test'] is True:
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
    if current_state is True:
        new_state = __salt__['jail.stop'](name)
        ret['result'] = True
        ret['comment'] = 'Jail "{0}" is running'.format(name)
        ret['changes'] = {
            'old': current_state,
            'new': new_state,
        }
        return ret
    if current_state is False:
        ret['result'] = True
        ret['comment'] = 'Jail "{0}" is already stopped'.format(name)
        return ret

    if __opts__['test'] is True:
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

    if __opts__['test'] is True:
        ret['result'] = None
        ret['comment'] = 'Jail "{0}" is not running.'.format(name)
        ret['changes'] = {
            'old': current_state,
            'new': 'Restarting Jail "{0}"'.format(name),
        }
        return ret

    return ret


def manage(name, jailloc, version, jail_files, jail_txz, freebsd_mirror,
           snapshot=False, rollback=False, lib32=True, src=True):
    '''
    Manage jail

    Manage release of jail
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

    if jailversion != version:

        if __salt__['file.file_exists']('{0}/{1}/base.txz'.format(jail_txz, str(version))) is False:
            __salt__['cp.get_url']('{0}amd64/{1}-RELEASE/base.txz'.format(freebsd_mirror, str(version)), '{0}/{1}/base.txz'.format(jail_txz, str(version)))

        if lib32 is True:
            if __salt__['file.file_exists']('{0}/{1}/lib32.txz'.format(jail_txz, str(version))) is False:
                __salt__['cp.get_url']('{0}amd64/{1}-RELEASE/lib32.txz'.format(freebsd_mirror, str(version)), '{0}/{1}/lib32.txz'.format(jail_txz, str(version)))

        if src is True:
            if __salt__['file.file_exists']('{0}/{1}/src.txz'.format(jail_txz, str(version))) is False:
                __salt__['cp.get_url']('{0}amd64/{1}-RELEASE/src.txz'.format(freebsd_mirror, str(version)), '{0}/{1}/src.txz'.format(jail_txz, str(version)))

        if __salt__['zfs.exists'](jailloc[1:-1]) is False:
            __salt__['zfs.create'](jailloc[1:-1])

        if __salt__['jail.status'](name) is True:
            __salt__['jail.stop'](name)

        # if snapshot is True:
            # __salt__['zfs.snapshot']('{0}@{1}'.format(jailloc[1:-1], str(jailversion)))

        for data in loclist:
            data = '{0}{1}'.format(jailloc, data)
            if __salt__['file.directory_exists'](data) is True:
                filelist = __salt__['file.readdir'](data)
                for files in filelist:
                    truepath = data + '/' + files
                    __salt__['chflags.change'](switch, 'noschg', truepath)
        if __salt__['file.file_exists']('{0}/bin/freebsd-version'.format(jailloc)) is False:
            __salt__['archive.tar']('xzf', '{0}{1}/base.txz'.format(jail_files, str(version)), dest=jailloc)
        else:
            __salt__['archive.tar']('xzf', '{0}{1}/base.txz'.format(jail_files, str(version)), dest=jailloc, exclude='/etc')

        __salt__['archive.tar']('xzf', '{0}{1}/lib32.txz'.format(jail_files, str(version)), dest=jailloc)
        if __salt__['file.directory_exists']('{0}/{1}/src'.format(jail_txz, str(version))) is False:
            __salt__['archive.tar']('xzf', '{0}/{1}/src.txz'.format(jail_txz, str(version)), dest='{0}/{1}/src'.format(jail_txz, str(version)))

        __salt__['jail.start'](name)

        __salt__['cmd.run']('mount -t nullfs {0}/{1}/src/usr/src {2}/usr/src'.format(jail_txz, str(version), jailloc))
        __salt__['cmd.run']('jexec {0} etcupdate'.format(name))
        __salt__['cmd.run']('jexec {0} etcupdate resolve'.format(name))
        # __salt__['cmd.run']('yes | jexec {0} make -c /usr/src delete-old'.format(name))
        # __salt__['cmd.run']('yes | jexec {0} make -c /usr/src delete-old-libs'.format(name))
        __salt__['mount.umount']('{0}/usr/src'.format(jailloc))

        if __salt__['jail.status'](name) is True:
            ret['result'] = True
            ret['comment'] = 'Jail "{0}" is upgraded and restarted'.format(name)
            ret['changes'] = {
                'new': '{0}'.format(version),
                'old': str(jailversion),
                }
            return ret
        if __salt__['jail.status'](name) is False:
            # __salt__['zfs.clone'](jailloc[1:-1] + '@' + jailversion + ' ' + jailloc[1:-1])
            __salt__['jail.start'](name)

            ret['result'] = False
            ret['comment'] = 'Jail "{0}" is rolled back and restarted'.format(name)
            ret['changes'] = {
                'new': 'Snapshot Rollback, fix and remove rollback: True',
                'old': 'broken jail {0}'.format(jailversion),
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
