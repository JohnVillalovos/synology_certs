#!/usr/bin/env python3
# vim: ai ts=4 sts=4 et sw=4

# Copyright (c) 2018-2023 John L. Villalovos
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import os
import subprocess
import sys

# This is based on using Synology DiskStation Manager (DSM) 6.1. Unsure if it
# works on previous versions. At the time of writing this (5-Mar-2018) I was
# using "DSM 6.1.5-15254 Update 1"

# Directory where certificates used by NGINX are stored
SYNOLOGY_NGINX_CERTS_DIR = os.path.abspath("/usr/syno/etc/certificate")
# Directory where certificates used by various packages are stored.
SYNOLOGY_PACKAGES_CERTS_DIR = os.path.abspath("/usr/local/etc/certificate")


def main():
    args = parse_args()
    if args.mode == 'nginx':
        get_certificates(SYNOLOGY_NGINX_CERTS_DIR)
    elif args.mode == "packages":
        get_certificates(SYNOLOGY_PACKAGES_CERTS_DIR)
    else:
        sys.exit("Unknown mode: {}".format(args.mode))


def get_certificates(dirname):
    if not os.path.isdir(dirname):
        sys.exit("The certificate directory does not exist: {}".format(
            dirname))

    for package_name in sorted(os.listdir(dirname)):
        service_dir = os.path.join(dirname, package_name)
        if not os.path.isdir(service_dir):
            continue

        for (dirpath, dirnames, filenames) in os.walk(service_dir):
            if 'cert.pem' in filenames:
                full_path = os.path.join(dirpath, 'cert.pem')
                host_name = find_cert_host(full_path)
                print("{}::{}::{}".format(host_name, dirpath, package_name))


def find_cert_host(filename):
    cmd_line = ['openssl', 'x509', '-noout', '-subject', '-in', filename]
    stdout = subprocess.check_output(cmd_line, universal_newlines=True)
    # Format is: "subject=CN = hostname.example.com"
    _, host_name = stdout.split('subject=CN =', 1)
    host_name = host_name.strip()
    return host_name


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['nginx', 'packages'])
    args = parser.parse_args()
    return args


if '__main__' == __name__:
    sys.exit(main())
