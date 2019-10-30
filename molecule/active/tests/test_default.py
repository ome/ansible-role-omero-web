import os
import pytest
import re

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


OMERO = '/opt/omero/web/OMERO.web/bin/omero'
VERSION_PATTERN = re.compile('(\d+)\.(\d+)\.(\d+)-ice36-')


def test_omero_web_config(Command, Sudo):
    with Sudo('omero-web'):
        cfg = Command.check_output("%s config get" % OMERO)
    assert cfg == (
        'omero.web.server_list=[["localhost", 12345, "molecule-test"]]')


def test_omero_version(Command, Sudo):
    with Sudo('omero-web'):
        ver = Command.check_output("%s version" % OMERO)
    m = VERSION_PATTERN.match(ver)
    assert m is not None
    assert int(m.group(1)) >= 5
    assert int(m.group(2)) > 3


@pytest.mark.parametrize("name", ["omero-web", "nginx"])
def test_services_running_and_enabled(Service, name):
    service = Service(name)
    assert service.is_running
    assert service.is_enabled


def test_nginx_gateway(Command):
    out = Command.check_output('curl -L localhost')
    assert 'OMERO.web - Login' in out


def test_omero_web_config_applied(Command, Sudo):
    out = Command.check_output('curl -L localhost')
    assert 'molecule-test:12345' in out
