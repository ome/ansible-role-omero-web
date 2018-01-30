import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    '.molecule/ansible_inventory').get_hosts('omero-web-inactive')

OMERO = '/opt/omero/web/OMERO.web/bin/omero'


def test_omero_version(Command, Sudo):
    with Sudo('omero-web'):
        ver = Command.check_output("%s version" % OMERO)
    assert ver.startswith('5.3.')


def test_nginx_not_configured(File):
    assert not File('/etc/nginx/conf.d/omero-web.conf').exists


def test_nginx_not_installed(Package):
    assert not Package('nginx').is_installed


def test_omeroweb_systemd_configured(File):
    assert File('/etc/systemd/system/omero-web.service').exists
