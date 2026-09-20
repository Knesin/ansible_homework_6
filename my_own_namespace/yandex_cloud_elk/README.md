# Ansible Collection - my_own_namespace.yandex_cloud_elk

Ansible Collection containing a custom module and role for creating
and updating text files on remote hosts.

## Requirements

- Ansible Core 2.19+
- Python 3.13+

## Included Content

### Modules

#### `my_own_module`

Creates or updates a text file on a remote host.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `path` | string | yes | Path to the file |
| `content` | string | yes | File content |

### Roles

#### `my_own_module`

Role for creating a text file using the `my_own_module` module.

Role defaults:

```yaml
path: /tmp/test.txt
content: "Hello from Ansible!"
```

## Example Playbook
```yml
---
- name: Create text file
  hosts: all

  roles:
    - role: my_own_namespace.yandex_cloud_elk.my_own_module
      path: /tmp/test.txt
      content: "Hello from my collection!"
```
