import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


def test_tomcat_service_exists(host):
    assert host.file("/etc/systemd/system/tomcat.service").exists


def test_tomcat_folder_exists(host):
    assert host.file("/opt/tomcat").exists


def test_fcrepo_listening(host):
    socket = host.socket("tcp://0.0.0.0:8080")

    assert socket.is_listening


def test_fcrepo_active(host):
    response = host.check_output("curl http://127.0.0.1:8080/fcrepo/rest")

    assert (
        """<http://127.0.0.1:8080/fcrepo/rest/>
        rdf:type                       ldp:RDFSource ;
        rdf:type                       ldp:Container ;
        rdf:type                       ldp:BasicContainer ;
        fedora:writable                "true"^^<http://www.w3.org/2001/XMLSchema#boolean> ;
        rdf:type                       fedora:RepositoryRoot ;
        rdf:type                       fedora:Resource ;
        rdf:type                       fedora:Container ;
        fedora:hasTransactionProvider  <http://127.0.0.1:8080/fcrepo/rest/fcr:tx> ."""
        in response
    )
