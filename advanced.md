
# SaltThings Advanced
   SaltStack Jail Management
   
   Using these below, templating jail.conf and fstab.
   Putting in pillar data and state file with below.
   You will be able to spin up two jails. 
   
   files will automatic download from FreeBSD Mirror.
   jail1 and jail2 on igb0, with nano installed.
   ip address will be 192.168.1.61 and 192.168.62

## Installing the states/module in files.


    {{ grains.saltpath }}/states/jail.py:
        file.managed:
            - source: salt://templates/patches/saltpatches/states/jail.py

    {{ grains.saltpath }}/states/poudriere.py:
        file.managed:
            - source: salt://templates/patches/saltpatches/states/poudriere.py

    {{ grains.saltpath }}/states/chflags.py:
        file.managed:
            - source: salt://templates/patches/saltpatches/states/chflags.py

    {{ grains.saltpath }}/states/freebsdservice_jail.py:
        file.managed:
            - source: salt://templates/patches/saltpatches/states/freebsdservice_jail.py

    {{ grains.saltpath }}/modules/chflags.py:
        file.managed:
            - source: salt://templates/patches/saltpatches/modules/chflags.py


## jail.conf Template

      {% if pillar['jail_vars'] is defined %}
      exec.start = "/bin/sh /etc/rc";
      exec.stop = "/bin/sh /etc/rc.shutdown";
      exec.clean;
      mount.devfs;
      path = "{{ salt['pillar.get']('jail_settings:location') }}/jails/$name";
      mount.fstab = /etc/fstab.$name;
      #################################################################################
      ################## All the Jails ################################################
      {% for jailname, jail in pillar.get('jail_vars', {}).items()  %}
      {{ jailname }} {
          host.hostname = "{{ jail.hostname }}";
          ip4.addr = "{{ jail.jail_if }}|{{ jail.jip }}";
          devfs_ruleset = {{ jail.devfs }};
          securelevel = {{ jail.securelevel }};
          {% if jail.rawsocket is defined %}
          {{ jail.rawsocket }};{% endif %}
      }
      {% endfor %}
      {% endif %}


## fstab file Template
      {% if jailname is defined  %}{% if fstab is defined  %}{% for fstab in fstab %}{{ fstab }}
      {% endfor %}{% endif %}{% endif %}



## Pillar Data

    jail_settings:
        zpool_root: storage
        location: /storage
        location_jail: /storage/jails
    
    jail_vars:
        jail1:
            name: jail1
            version: 12.1
            hostname: jail1
            jail_if: igb0
            jip: 192.168.1.61
            devfs: 4
            securelevel: 3
            mountpoints:
              - /storage/jails/jail1
            fstab:
              - /storage/jaildata/jail1 /storage/jails/jail1 nullfs  rw  0  0
            pkgs:
              - nano
        jail2:
            name: jail2
            version: 12.1
            hostname: jail2
            jail_if: igb0
            jip: 192.168.1.62
            devfs: 4
            securelevel: 3
            mountpoints:
              - /storage/jails/jail2
            fstab:
              - /storage/jaildata/jail2 /storage/jails/jail2 nullfs  rw  0  0
            pkgs: 
              - nano
              
## State File
  
     ################################################################################    
     ################## Download Jail Sources ########################################
    {% for files in pillar['jail_base'] %}
    update_{{ salt['pillar.get']('poudriere_build:freebsd_version') }}_{{ files.name }}_base:
        file.managed:
          - name: {{ salt['pillar.get']('jail_settings:location_jail') }}/{{ salt['pillar.get']('poudriere_build:freebsd_version') }}/{{ files.name }}
           - source: http://ftp.freebsd.org/pub/FreeBSD/releases/amd64/{{ salt['pillar.get']('poudriere_build:freebsd_release') }}/{{ files.name }}
           - skip_verify: true
           - replace: false
           - makedirs: True
    {% endfor %}

    ################################################################################
    ################## Upgrade Jails as Needed #####################################
    {% for jailname, jail in pillar.get('jail_vars', {}).items() %}
    jail_upgrade_{{jailname}}:
        jail.upgrade:
          - name: {{jailname}}
          - jailloc: {{ salt['pillar.get']('jail_settings:location_jail') }}/{{ jailname }}/
          - version: {{ jail.version }}
          - jail_files: {{ salt['pillar.get']('jail_settings:location_jail') }}/
    {% endfor %}

    ################################################################################
    ################## Set Jail Grain Version ######################################
    {% for jailname, jail in pillar.get('jail_vars', {}).items() %}
    jail_{{ jailname }}_installed:
        grains.present:
          - name: jail:jail_{{ jailname }}_installed
          - value: {{ jail.version }}
    {% endfor %}

    ################################################################################
    ################## Set Jail Mountpoints ########################################
    {% for jailname, jail in pillar.get('jail_vars', {}).items() %}
    {% if jail.mountpoints is defined %}
    {% for mountpoints in jail.mountpoints %}
    jail_mountpoint_create_{{ jailname }}_{{ mountpoints }}:
        file.directory:
          - name: {{ mountpoints }}
          - makedirs: True
    {% endfor %}
    {% endif %}
    {% endfor %}

    {% for jailname in pillar['jail_vars'] %}
    jail_start_{{ jailname }}:
        jail.start:
          - name: {{ jailname }}
    {% endfor %}

    ################################################################################
    ################## Install Jail Packages #######################################
    {% for jailname, jail in pillar.get('jail_vars', {}).items() %}
    {% if jail.pkgs is defined %}
    {{ jailname }}_jail_install_pkgs:
        pkg.installed:
          - jail: {{ jailname }}
          - pkgs:
          {% for packages in jail.pkgs %}
          - {{ packages }}
          {% endfor %}
    {% endif %}
    {% endfor %}

    ################################################################################
    ################## Upgrade Jails Packages Needed ###############################
    {% for jailname, jail in pillar.get('jail_vars', {}).items() %}
    {{ jailname }}_jail_upgrade_pkgs:
        pkg.uptodate:
          - jail: {{ jailname }}
          - refresh: True
    {% endfor %}

    ################################################################################
    ################## Restart Jails as Needed #####################################
    {% for jailname, jail in pillar.get('jail_vars', {}).items() %}
    jail_restart_{{ jailname }}:
        jail.restart:
          - name: {{ jailname }}
          - onchanges:
            {% if jail.fstab is defined %}
            - file: jail_{{ jailname }}_fstab
            {% endif %}
            - pkg: {{ jailname }}_jail_install_pkgs
            - pkg: {{ jailname }}_jail_upgrade_pkgs
     {% endfor %}
