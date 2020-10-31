# -*- coding: utf-8 -*-
"""
The release upgrade module for FreeBSD
"""

# Import python libs
from __future__ import absolute_import, print_function, unicode_literals

import os
import re
import subprocess

# Import salt libs
import salt.utils.args
import salt.utils.files
import salt.utils.stringutils

# Define the module's virtual name
__virtualname__ = "freebsd_update"


def __virtual__():
    """
    Only runs on FreeBSD systems
    """
    if __grains__["os"] == "FreeBSD":
        return __virtualname__
    return (
        False,
        "The freebsd_update execution module cannot be loaded: "
        "only available on FreeBSD systems.",
    )


def chflags(host_files):
    """
    Set chflags on host

    CLI Example:

    .. code-block:: bash

        salt '*' freebsd_update.chflags <host_files>
    """
    switch = ""
    loclist = [
        "var/empty",
        "lib",
        "bin",
        "sbin",
        "usr/bin",
        "usr/lib",
        "usr/lib32",
        "usr/libexec",
        "usr/sbin",
        "libexec",
    ]

    for data in loclist:
        data = "{0}{1}".format("/", data)
        filelist = __salt__["file.readdir"](data)
        for files in filelist:
            truepath = '{0}/{1}'.format(data, host_files)
            __salt__["chflags.change"](switch, "noschg", truepath)


def etc_resolve():
    """
    resolve etc

    CLI Example:

    .. code-block:: bash

        salt '*' freebsd_update.etc_resolve
    """
    __salt__["cmd.run"]("etcupdate")
    __salt__["cmd.run"]("etcupdate resolve")


def base_upgrade(host_files, version):
    """
    host base upgrade

    CLI Example:

    .. code-block:: bash

        salt '*' freebsd_upgrade.base_upgrade <host_files> <version>
    """
    __salt__["archive.tar"]("xzf", '{0}/{1}/kernel.txz'.format(host_files, str(version)), dest="/")
    __salt__["archive.tar"]("xzf", '{0}/{1}/base.txz'.format(host_files, str(version)), dest="/", exclude="etc")


def lib32_upgrade(host_files, version):
    """
    host lib32 upgrade

    CLI Example:

    .. code-block:: bash

        salt '*' freebsd_upgrade.lib32_upgrade <host_files> <version>
    """
    if __salt__["archive.tar"]("xzf", "{0}/{1}/lib32.txz".format(host_files, str(version)), dest="/") is True:
        return True
    else:
        return False


def manage(host_files, version, lib32=False, src=False, pass_opt=False):
    """
    manage FreeBSD release

    snapshot, lib32, src are true/false

    host_files is location of txz files

    CLI Example:

    .. code-block:: bash

        salt '*' freebsd_upgrade.manage <host_files> <version> <lib32> <src>
    """
    host_version = __salt__["grains.get"]("release_version")

    if host_version != version and pass_opt is False:

        __salt__["freebsd_update.chflags"]("/")

        if __salt__["freebsd_update.base_upgrade"](host_files, version) is True:

            if lib32 is True:
                __salt__["freebsd_update.lib32_upgrade"](host_files, version)

    __salt__["grains.set"]("release_version", val=version)
    __salt__["saltutil.refresh_grains"]
    return True
