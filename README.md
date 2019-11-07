# SaltThings
SaltStack Modifications


## For jails capabilities, apply the following to state.

    {{ grains.saltpath }}/states/jail.py:
        file.managed:
          - source: salt://templates/patches/saltpatches/states/jail.py

## Pillar Data

    ##### PIllar Data #####

    jail_vars:
        jail1:
            name: jail1
            pkg:
              - pkg1
              - pkg2
        jail2:
            name: jail2
            pkg:
              - pkg3
              - pkg4

    ##### End Pillar Data #####

    ##### Status State Data #####

    {% for jailname in pillar['jail_vars'] %}
    jail_status_{{ jailname }}:
        jail.status:
            - name: {{ jailname }}
    {% endfor %}

    ##### End Status State Data #####

    ##### Start State Data #####

    {% for jailname in pillar['jail_vars'] %}
    jail_start_{{ jailname }}:
        jail.start:
          - name: {{ jailname }}
    {% endfor %}

    ##### End Start State Data #####
