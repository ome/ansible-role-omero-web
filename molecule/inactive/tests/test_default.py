import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


OMERO = '/opt/omero/web/OMERO.web/bin/omero'


def test_omero_web_config(host):
    with host.sudo('omero-web'):
        cfg = host.check_output("%s config get" % OMERO)
    assert cfg == (
        'omero.web.server_list=[["localhost", 12345, "molecule-test"]]')


def test_omero_version(host):
    with host.sudo('omero-web'):
        ver = host.check_output("%s version" % OMERO)
    assert ver.startswith('5.3.')


def test_nginx_not_configured(host):
    assert not host.file('/etc/nginx/conf.d/omero-web.conf').exists


def test_nginx_not_installed(host):
    assert not host.package('nginx').is_installed


def test_omeroweb_systemd_configured(host):
    assert host.file('/etc/systemd/system/omero-web.service').exists
