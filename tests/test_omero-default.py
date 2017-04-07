import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    '.molecule/ansible_inventory').get_hosts('all')

OMERO = '/opt/omero/web/OMERO.web/bin/omero'


def test_omero_web_config(Command, Sudo):
    with Sudo('omero-web'):
        cfg = Command.check_output("%s config get" % OMERO)
    assert cfg == (
        'omero.web.server_list=[["localhost", 12345, "molecule-test"]]')
