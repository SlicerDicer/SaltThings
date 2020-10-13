# -*- coding: utf-8 -*-

"""
Manage dhparam on FreeBSD systems
"""

from __future__ import absolute_import, print_function, unicode_literals

# Import python libs
import logging
import os
import re

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
from salt.exceptions import (
    CommandExecutionError,
    MinionError,
    SaltInvocationError,
    get_error_message as _get_error_message,
)
from salt.utils.files import HASHES, HASHES_REVMAP

log = logging.getLogger(__name__)

# Define the module's virtual name
__virtualname__ = "dhparam"


def __virtual__():
    """
    Only runs on FreeBSD systems
    """
    if __grains__.get("os") == "FreeBSD":
        return __virtualname__
    return (
        False,
        "The freebsd dhparams execution module cannot be loaded: "
        "only available on FreeBSD systems.",
    )


def check(file):
    """

    check dhparams

    file
        desired file to check dhparams

    CLI Example:

    .. code-block:: bash

        salt '*' dhparam.check /path/to/dh.pem

    """
    cmd = "openssl dhparam -check -in {0}".format(file)
    services = __salt__["cmd.run"](cmd, python_shell=False)
    for service in services.split("\\n"):
        if re.search("ok", service):
            return True
    return False


def create(file, bits):
    """

    create dhparams

    file
        desired file to create dhparams

    CLI Example:

    .. code-block:: bash

        salt '*' dhparam.create /path/to/dh.pem 2048

    """
    if __salt__["dhparam.check"](file) is True:
        return True
    else:
        cmd = "openssl dhparam -out {0} {1}".format(file, bits)
        services = __salt__["cmd.run"](cmd, python_shell=False)
        if __salt__["dhparam.check"](file) is True:
            return True
        else:
            return False
