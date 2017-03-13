OMERO Web
=========

Installs and configures OMERO.web and Nginx.


Role Variables
--------------

All variables are optional, see `defaults/main.yml` for the full list

- `omero_web_release`: The version of OMERO.web to install, default `latest`
- `omero_web_upgrade`: Upgrade OMERO.web if the current version does not match `omero_web_release`
- `omero_web_default_server_list`: A list of OMEOR.servers that should be configured in OMERO.web.
  This may be ignored if `omero_web_prestart_file` is changed.
- `omero_web_prestart_file`: The Jinja2 template used to generate the OMERO.web configuration file, default `templates/omero-web-config.j2`.
  If you require any non-default configuration settings define your own template, and either copy or include the default template.
- `omero_web_ice_version`: The ice version.

Warning
-------

This role regenerates the OMERO.web configuration file.
Manual configuration changes (`omero config ...`) will be lost following an upgrade.

Configuration changes are executed using two handlers:
1. Loading the Jinja2 genwerated template into OMERO.web using `omero load`
2. Restarting the OMERO.web service

If a playbook fails part way it is possible that configuration changes will not be deployed at one or more of these stages.
See https://github.com/openmicroscopy/design/issues/70 for a proposal to remove the first handler.


Example Playbooks
-----------------

Configure OMERO.web with a single backend server, `omero.example.org:4064`:

    - hosts: localhost
      roles:
        - role: ansible-role-omero-web
          omero_web_default_server_list:
          - [omero.example.org, 4064, omero-example]

Configure OMERO.web with a custom configuration template `custom-web-config.j2`:

    # {{ ansible_managed }}

    config drop default
    config set omero.web.server_list {{ omero_web_default_server_list | to_json | quote }}
    config set config set omero.web.public.enabled True
    config set omero.web.public.server_id 1
    config set omero.web.public.user public
    config set omero.web.public.password {{ omero_web_public_password }}

Playbook:

    - hosts: localhost
      roles:
        - role: ansible-role-omero-web
          omero_web_prestart_file: custom-web-config.j2


Author Information
------------------

ome-devel@lists.openmicroscopy.org.uk
