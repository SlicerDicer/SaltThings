FreeBSD is incredible, some of the utilties are not. This was a large issue for my admin of FreeBSD. 

## Solved Problems

* Install jails simply.
* Manage all the packages in hosts/jail
* Manage host/jail release upgrades. 

## Todo
* Upgrade Packages with pkgaudit data
* Install bhyve vms easily. 
* Automated kernel builds based on release

## Goals

FreeBSD is difficult, so lets make it not difficult.\
The goal is to develop a complete FreeBSD lifecycle management. Rolling release to release without issues. 

## Installation:

DO put this on a test machine.\
DO not destroy prod. Ye hath duly been warned.\
Assumption is using ZFS in zroot\

Install SaltStack and git\
`pkg install py37-salt git`\
Clone SaltThings\
`git clone https://github.com/SlicerDicer/SaltThings.git`\
Patch Salt
```
cp SaltThings/modules/* /usr/local/lib/python3.7/site-packages/salt/modules/
cp SaltThings/states/* /usr/local/lib/python3.7/site-packages/salt/states/
```
Enable services
```
service enable salt_master
service enable salt_minion
```
Edit /usr/local/etc/salt/master put ip address here and minion
```
interface: ipaddress
id: salt_test
```
Edit /usr/local/etc/salt/minion
```
master: ipaddress
id: salt_test
```
Start SaltStack\
```
service salt_master start
service salt_minion start
```
Create jail zfs
```
salt salt_test zfs.create zroot/jails
mkdir /zroot/jails/12.2
cd /zroot/jails/12.2
```
Grab base.txz from FreeBSD.org\
`wget http://ftp.freebsd.org/pub/FreeBSD/releases/amd64/12.2-RELEASE/base.txz`\
Grab a cup of coffee if your internet connection is horrible :\
### Jail Time
Lets put on a 12.2-RELEASE jail!\
`salt salt_test jail.manage /zroot/jails 12.2 zroot/jails/test_jail test_jail`\
\
Edit /etc/jail.conf
```
test_jail {
    host.hostname = salt_test;                 # Hostname
    ip4.addr = ;                               # IP address of the jail
    path = "/zroot/jails/test_jail";           # Path to the jail
    devfs_ruleset = "4";                       # devfs ruleset
    mount.devfs;                               # Mount devfs inside the jail
    exec.start = "/bin/sh /etc/rc";            # Start command
    exec.stop = "/bin/sh /etc/rc.shutdown";    # Stop command
}
```
Start test_jail\
`service jail onestart test_jail`\
jexec into test_jail\
`jexec test_jail`\
\
Congrats you now have a working jail.

### More
As I have time, I will document the rest. 
