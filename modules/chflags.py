# -*- coding: utf-8 -*-
# (c) Gregg Furstenwerth 2020

'''
Manage chflags on FreeBSD systems
'''

from __future__ import absolute_import, print_function, unicode_literals

# Import python libs
import logging
import os

# pylint: disable=import-error,no-name-in-module,redefined-builtin
from salt.ext import six
from salt.ext.six.moves import range, zip
from salt.ext.six.moves.urllib.parse import urlparse as _urlparse
# pylint: enable=import-error,no-name-in-module,redefined-builtin

# Import salt libs
import salt.utils.args
import salt.utils.atomicfile
import salt.utils.data
import salt.utils.dictupdate
import salt.utils.filebuffer
import salt.utils.files
import salt.utils.find
import salt.utils.functools
import salt.utils.hashutils
import salt.utils.itertools
import salt.utils.path
import salt.utils.platform
import salt.utils.stringutils
import salt.utils.templates
import salt.utils.url
import salt.utils.user
import salt.utils.versions
from salt.exceptions import CommandExecutionError, MinionError, SaltInvocationError, get_error_message as _get_error_message
from salt.utils.files import HASHES, HASHES_REVMAP

log = logging.getLogger(__name__)

# Define the module's virtual name
__virtualname__ = 'chflags'

def __virtual__():
    '''
    Only runs on FreeBSD systems
    '''
    if __grains__.get('os') == 'FreeBSD':
        return __virtualname__
    return (False, 'The freebsd chflags execution module cannot be loaded: '
            'only available on FreeBSD systems.')


def change(switch, flag, file):
    '''

    set system system flags

    switch
        desired switch for chflags

    flag
        desired flag for chflags

    file
        desired file to change chflags

    CLI Example:

    .. code-block:: bash

        salt '*' chflags.noschg '' noschg /path/to/foo
        salt '*' chflags.noschg '-v' noschg /path/to/foo

    '''
    flags = ''
    switch = ''
    if os.path.exists(file):
        try:
            # Broken file will return false
            __salt__['cmd.run']('chflags {0} {1} {2}'.format(switch, flag, file))
            chflag = __salt__['chflags.report'](file)
            if flag in str(chflag):
                flags = True
                return flags
            else:
                flags = None
                return flags
        except OSError:
            pass
    else:
        flags = False
    return flags


def report(file):
    '''

    Search for system flags

    file
        desired file to scan

    CLI Example:

    .. code-block:: bash

        salt '*' chflags.report /path/to/foo
    '''

    statval = ''

    if os.path.exists(file):
        try:
            # Broken file will return false
            statdat = os.stat(file)
            statval = statdat.st_flags

            if statval == 133120:
                statval = "schg", "uarch"
                return statval
            if statval == 133121:
                statval = "schg", "uarch", "nodump"
                return statval
            if statval == 2049:
                statval = "uarch", "nodump"
                return statval
            if statval == 2048:
                statval = "uarch"
                return statval
            else:
                return statval
            return statval
        except OSError:
            pass
    else:
        statval = False
    return statval
