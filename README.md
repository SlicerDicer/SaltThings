# SaltThings
SaltStack Modifications


## For jails capabilities, apply the following to state.

    {{ grains.saltpath }}/states/jail.py:
        file.managed:
          - source: salt://templates/patches/saltpatches/states/jail.py



## Pillar Data

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

## State Data pkg

    {% for jailname, jail in pillar.get('jail_vars', {}).items() %}
    {% if jail.pkgs is defined %}
    {{ jailname }}_jail_install_pkgs:
        pkg.installed:
          - jail: {{ jailname }}
          - pkgs:
            # install salt on all jails
            - py36-salt
            {% for packages in jail.pkgs %}
            - {{ packages }}
            {% endfor %}
    {% endif %}
    {% endfor %}

## State Data Jails

    {% for jailname in pillar['jail_vars'] %}
    jail_status_{{ jailname }}:
        jail.status:
            - name: {{ jailname }}
    {% endfor %}

    {% for jailname in pillar['jail_vars'] %}
    jail_start_{{ jailname }}:
        jail.start:
          - name: {{ jailname }}
    {% endfor %}

