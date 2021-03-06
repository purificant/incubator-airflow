#!/usr/bin/env python
# Licensed to Cloudera, Inc. under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  Cloudera, Inc. licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import re
import socket

from airflow.utils.net import get_hostname


def get_components(principal):
    """
    get_components(principal) -> (short name, instance (FQDN), realm)

    ``principal`` is the kerberos principal to parse.
    """
    if not principal:
        return None
    return re.split('[\/@]', str(principal))


def replace_hostname_pattern(components, host=None):
    fqdn = host
    if not fqdn or fqdn == '0.0.0.0':
        fqdn = get_hostname()
    return '%s/%s@%s' % (components[0], fqdn.lower(), components[2])


def get_fqdn(hostname_or_ip=None):
    # Get hostname
    try:
        if hostname_or_ip:
            fqdn = socket.gethostbyaddr(hostname_or_ip)[0]
            if fqdn == 'localhost':
                fqdn = get_hostname()
        else:
            fqdn = get_hostname()
    except IOError:
        fqdn = hostname_or_ip

    return fqdn


def principal_from_username(username, realm):
    if ('@' not in username) and realm:
        username = "{}@{}".format(username, realm)

    return username
