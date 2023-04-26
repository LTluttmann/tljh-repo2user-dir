# tljh-repo2user-dir

A plugin for [The Littlest JupyterHub (TLJH)](https://tljh.jupyter.org) through which one can easily populate user directories with the content of a github repository. This is accomplished with the tljh_new_user_create hook. One only needs to specify a link to a github repo by setting a REPO_URL environment variable.

## Install

To deploy a new TLJH instance with this plugin installed simply call 

```
#!/bin/bash
curl -L https://tljh.jupyter.org/bootstrap.py \
  | sudo python3 - \
    --admin tdi2023 --plugin git+https://github.com/LTluttmann/tljh-repo2user-dir.git
```

and define the env variable REPO_URL with the repo of your choice. Setting up the environment variable can be a little cumbersome since it is needed in the root environment. One way is to override the `jupyterhub` settings as specified [here](https://github.com/jupyterhub/the-littlest-jupyterhub/blob/4aa96d92c32428a98fe60489e38a43114773468d/docs/howto/admin/systemd.md?plain=1#L39)

In short, provide a custom `/etc/systemd/system/jupyterhub.service.d/override.conf` file with following content

```
[Service]
Environment=REPO_URL="<YOUR REPO>"
```

Then make sure to reload the daemon and the `jupyterhub` service:

```bash
sudo systemctl daemon-reload
sudo systemctl restart jupyterhub
```

## Adding new Users

To add a new user:
```bash
sudo tljh-config add-item users.allowed <NEW USER>
sudo tljh-config reload
```

When logging in with this new user, the repo should be available within the subfolder "repos"

## License

We use a shared copyright model that enables all contributors to maintain the
copyright on their contributions.

This software is licensed under the BSD-3-Clause license. See the
[LICENSE](LICENSE) file for details.

