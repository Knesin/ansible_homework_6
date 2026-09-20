#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: my_test
short_description: "Создание текстового файла с заданным содержимым"
version_added: "1.0.0"
description:
    - "Создает текстовый файл на удаленном узле по заданному пути."
    - "Обеспечивает идемпотентность: не перезаписывает файл, если его содержимое уже идентично."
    - "Перезаписывает файл только в случае несовпадения содержимого."
options:
    path:
        description:
            - "Абсолютный или относительный путь к создаваемому файлу на удаленном узле."
        required: true
        type: str
    content:
        description:
            - "Текстовое содержимое файла."
        required: true
        type: str
author:
    - Maksim Klochek (@Knesin)
'''

EXAMPLES = r'''
- name: Create text file
  my_test:
    path: /tmp/greeting.txt
    content: "Hello, Ansible!"
'''

RETURN = r'''
path:
    description: Path to the file.
    type: str
    returned: always
    sample: /tmp/greeting.txt

changed:
    description: Whether the file was created or modified.
    type: bool
    returned: always
    sample: true
'''

import os
from ansible.module_utils.basic import AnsibleModule


def run_module():
    module_args = dict(
        path=dict(
            type='str',
            required=True
        ),
        content=dict(
            type='str',
            required=True
        )
    )

    result = dict(
        changed=False,
        path=''
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )


    path = module.params['path']
    content = module.params['content']
    result['path'] = path

    if os.path.exists(path):
        if not os.path.isfile(path):
            module.fail_json(
                msg='Path exists but is not a regular file: {0}'.format(path),
                **result
            )
        try:
            with open(path, 'r') as f:
                current_content = f.read()
        except Exception as e:
            module.fail_json(
                msg="Cannot read file '{0}': {1}".format(path, str(e)),
                **result
            )
        if current_content != content:
            result['changed'] = True
    else:
        result['changed'] = True

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    if result['changed']:
        try:
            parent_dir = os.path.dirname(path)
            if parent_dir and not os.path.exists(parent_dir):
                os.makedirs(parent_dir, exist_ok=True)

            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
        except (IOError, OSError) as e:
            module.fail_json(
                msg="Cannot write file '{0}': {1}".format(path, str(e)),
                **result
            )
    
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()

