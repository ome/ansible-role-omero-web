import os
import pytest
import re

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


OMERO = '/opt/omero/web/OMERO.web/bin/omero'
VERSION_PATTERN = re.compile('(\d+)\.(\d+)\.(\d+)-ice36-')


def test_omero_web_config(host):
    with host.sudo('omero-web'):
        cfg = host.check_output("%s config get" % OMERO)
    assert cfg == (
        'omero.web.server_list=[["localhost", 12345, "molecule-test"]]')


def test_omero_version(host):
    with host.sudo('omero-web'):
        ver = host.check_output("%s version" % OMERO)
    m = VERSION_PATTERN.match(ver)
    assert m is not None
    # This is an old Python 2 test so it'll never be more recent than 5.5.1
    assert m.groups() == ('5', '5', '1')


@pytest.mark.parametrize("name", ["omero-web", "nginx"])
def test_services_running_and_enabled(host, name):
    service = host.service(name)
    assert service.is_running
    assert service.is_enabled


def test_nginx_gateway(host):
    out = host.check_output('curl -L localhost')
    assert 'OMERO.web - Login' in out


def test_omero_web_config_applied(host):
    out = host.check_output('curl -L localhost')
    assert 'molecule-test:12345' in out
