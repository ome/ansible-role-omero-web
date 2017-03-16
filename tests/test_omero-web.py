import testinfra.utils.ansible_runner
import pytest

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    '.molecule/ansible_inventory').get_hosts('omero-web')


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
