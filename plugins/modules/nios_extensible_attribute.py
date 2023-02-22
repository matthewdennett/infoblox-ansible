#!/usr/bin/python
# Copyright (c) 2018-2019 Red Hat, Inc.
# Copyright (c) 2020 Infoblox, Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: nios_extensible_attribute
author: "Matthew Dennett (@matthewdennett)"
short_description: Configure Infoblox NIOS extensible attribute definition
version_added: "1.5.0"
description:
  - Adds and/or removes a extensible attribute definition objects from
    Infoblox NIOS servers.  This module manages NIOS C(extensibleattributedef)
    objects using the Infoblox WAPI interface over REST.
requirements:
  - infoblox-client
extends_documentation_fragment: infoblox.nios_modules.nios
notes:
    - This module supports C(check_mode).
options:
  comment:
    description:
      - Configures a text string comment to be associated with the instance
        of this object. The provided text string will be configured on the
        object instance.
    type: str
  default_value:
    description:
      - Configures the default value which is pre populated in the GUI when
        this attribute is used. Email, URL and string types the value is a
        with a maximum of 256 characters.
    type: str
  list_values:
    description:
      - Configures a list of preset values associated with the instance of this
        object. Only applicable when the attribute type is set to ENUM.
    type: list
  max:
    description:
      - Configures the maximum value to be associated with the instance of
        this object. When provided for an extensible attribute of type
        STRING the value represents the maximum number of characters the string
        can contain. When provided for an extensible attribute of type INTEGER
        the value represents the maximum integer value permitted.Not
        applicable for other attributes types.
    type: str
  min:
    description:
      - Configures the minimum value to be associated with the instance of
        this object. When provided for an extensible attribute of type
        STRING the value represents the minimum number of characters the string
        can contain. When provided for an extensible attribute of type INTEGER
        the value represents the minimum integer value permitted. Not
        applicable for other attributes types.
    type: str
  name:
    description:
      - Configures the intended name of the instance of the object on the
        NIOS server.
    type: str
    required: true
  type:
    description:
      - Configures the intended type for this attribute object definition
        on the NIOS server.
    type: str
    required: true
    default: STRING
    choices:
      - DATE
      - EMAIL
      - ENUM
      - INTEGER
      - STRING
      - URL
  state:
    description:
      - Configures the intended state of the instance of the object on
        the NIOS server.  When this value is set to C(present), the object
        is configured on the device and when this value is set to C(absent)
        the value is removed (if necessary) from the device.
    type: str
    default: present
    choices:
      - present
      - absent
'''

EXAMPLES = '''
- name: Configure an extensible attribute
  infoblox.nios_modules.nios_extensible_attribute:
    name: my_string
    type: STRING
    comment: Created by ansible
    state: present
    provider:
      host: "{{ inventory_hostname_short }}"
      username: admin
      password: admin
  connection: local

- name: Remove a extensible attribute
  infoblox.nios_modules.nios_extensible_attribute:
    name: my_string
    type: INTEGER
    state: absent
    provider:
      host: "{{ inventory_hostname_short }}"
      username: admin
      password: admin
  connection: local

- name: Create INT extensible attribute
  infoblox.nios_modules.nios_extensible_attribute:
    name: my_int
    type: INTEGER
    comment: Created by ansible
    min: 10
    max: 20
    state: present
    provider:
      host: "{{ inventory_hostname_short }}"
      username: admin
      password: admin
  connection: local

- name: Update an extensible attribute
  infoblox.nios_modules.nios_extensible_attribute:
    name: my_int
    type: INTEGER
    comment: Updated by ansible
    state: present
    provider:
      host: "{{ inventory_hostname_short }}"
      username: admin
      password: admin
  connection: local

- name: Create an list extensible attribute
  infoblox.nios_modules.nios_extensible_attribute:
    name: my_list
    type: ENUM
    state: present
    list_values:
      - _struct: extensibleattributedef:listvalues
        value: one
      - _struct: extensibleattributedef:listvalues
        value: two
      - _struct: extensibleattributedef:listvalues
        value: three
    provider:
      host: "{{ inventory_hostname_short }}"
      username: admin
      password: admin
  connection: local

'''

RETURN = ''' # '''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.six import iteritems
from ..module_utils.api import WapiModule
from ..module_utils.api import normalize_ib_spec


def options(module):
    ''' Transforms the module argument into a valid WAPI struct
    This function will transform the options argument into a structure that
    is a valid WAPI structure in the format of:
        {
            name: <value>,
            num: <value>,
            value: <value>,
            use_option: <value>,
            vendor_class: <value>
        }
    It will remove any options that are set to None since WAPI will error on
    that condition.  It will also verify that either `name` or `num` is
    set in the structure but does not validate the values are equal.
    The remainder of the value validation is performed by WAPI
    '''
    options = list()
    for item in module.params['options']:
        opt = dict([(k, v) for k, v in iteritems(item) if v is not None])
        if 'name' not in opt and 'num' not in opt:
            module.fail_json(msg='one of `name` or `num` is required for option value')
        options.append(opt)
    return options


def main():
    ''' Main entry point for module execution
    '''

    ib_spec = dict(
        comment=dict(type='str'),
        default_value=dict(type='str'),
        list_values=dict(type='list', elements='dict'),
        max=dict(type='str'),
        min=dict(type='str'),
        name=dict(type='str', required=True, ib_req=True),
        type=dict(type='str', required=True, default='STRING',
              choices=['DATE', 'EMAIL', 'ENUM', 'INTEGER', 'STRING', 'URL'])
    )

    argument_spec = dict(
        provider=dict(required=True),
        state=dict(default='present', choices=['present', 'absent'])
    )

    argument_spec.update(normalize_ib_spec(ib_spec))
    argument_spec.update(WapiModule.provider_spec)

    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=True)

    wapi = WapiModule(module)

    result = wapi.run('extensibleattributedef', ib_spec)

    module.exit_json(**result)


if __name__ == '__main__':
    main()