import salt.exceptions


def is_jail(name):
    '''
    Check Poudriere jail status
    '''

    ret = {
        'name': name,
        'changes': {},
        'result': False,
        'comment': '',
        }

    # Check the current state of jails.
    current_state = __salt__['poudriere.is_jail'](name)
    if current_state == True:
        ret['result'] = True
        ret['comment'] = 'Poudriere "{0}" exists'.format(name)
        return ret
    if current_state == False:
        ret['result'] = False
        ret['comment'] = 'Poudriere "{0}" does not exist'.format(name)
        return ret
    # The state of the system does need to be changed. Check if we're running
    # in ``test=true`` mode.
    if __opts__['test'] == True:
        ret['result'] = None
        ret['comment'] = 'Poudriere "{0}" does not exist.'.format(name)
        ret['changes'] = result

        return ret

    return ret


def create_jail(name, arch, version):
    '''
    Create Poudriere Jail
    '''

    ret = {
        'name': name,
        'changes': {},
        'result': False,
        'comment': '',
        }
    current_state = __salt__['poudriere.is_jail'](name)
    if current_state == True:
        ret['result'] = True
        ret['comment'] = 'Poudriere Jail "{0}" is already created'.format(name)
        return ret
    if __opts__['test'] == True:
        ret['result'] = None
        ret['comment'] = 'Poudriere Jail "{0}" is not created.'.format(name)
        ret['changes'] = {
            'old': current_state,
            'new': 'Creating Poudriere Jail "{0}"'.format(name),
        }

        return ret

    new_state = __salt__['poudriere.create_jail'](name, arch, version)

    ret['comment'] = 'Poudriere Jail "{0}" was created'.format(name)

    ret['changes'] = {
        'old': current_state,
        'new': new_state,
    }

    ret['result'] = True

    return ret

def delete_jail(name):
    '''
    Delete Poudriere Jail
    '''

    ret = {
        'name': name,
        'changes': {},
        'result': False,
        'comment': '',
        }
    current_state = __salt__['poudriere.is_jail'](name)
    if current_state == False:
        ret['result'] = True
        ret['comment'] = 'Poudriere Jail "{0}" is deleted'.format(name)
        return ret
    if __opts__['test'] == True:
        ret['result'] = None
        ret['comment'] = 'Poudriere Jail "{0}" is deleted.'.format(name)
        ret['changes'] = {
            'old': current_state,
            'new': 'Deleting Poudriere Jail "{0}"'.format(name),
        }
        return ret

    new_state = __salt__['poudriere.delete_jail'](name)
    ret['comment'] = 'Poudriere Jail "{0}" was created'.format(name)
    ret['changes'] = {
        'old': current_state,
        'new': new_state,
        }
    ret['result'] = True
    return ret
