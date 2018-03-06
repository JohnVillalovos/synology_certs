synology_certs
==============

This is an Ansible role to update existing certificates on a Synology system
running DiskStation Manager (DSM) 6.0 or higher. It has been designed with Lets
Encrypt (https://letsencrypt.org/) in mind. And in particular used the Lets
Encrypt client https://github.com/Neilpang/acme.sh. The reason for this role is
that I use DNS-01 authentication mode for Lets Encrypt certificates which
Synology does not yet support.

Requirements
------------

This requires a top-level directory where under it are directories named for
each host and in those directories are the certificates. This is the format
used by https://github.com/lukas2511/dehydrated which is the Lets Encrypt
client this was used with.

Role Variables
--------------

* ``cert_dir``: The top-level directory where under it are directories named for
              each host and in those directories are the certificates.

Dependencies
------------

N/A

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: synology_servers
      tasks:
      - include_role:
          name: synology_certs
        vars:
          cert_dir: '~/sources/acme.sh/certs/'

Notes
-----

Synology DiskStation Manager (DSM) 6.0 and greater store the SSL certificates under two different directories:
  * NGINX certificates: ``/usr/syno/etc/certificate/``
  * Package certificates: ``/usr/local/etc/certificate/``

Ideas:
Maybe this role should parse the JSON file at: ``/usr/syno/etc/certificate/_archive/INFO``

License
-------

Apache License, 2.0 (http://www.apache.org/licenses/LICENSE-2.0)

Author Information
------------------

https://github.com/JohnVillalovos
