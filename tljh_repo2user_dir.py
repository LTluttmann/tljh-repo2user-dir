import os
import shutil
from pwd import getpwnam
from git import Repo
from tljh.utils import get_plugin_manager
from tljh.normalize import generate_system_username
from tljh.hooks import hookimpl


def clone_repo(user, git_url, repo_dir):
    """
    A function to clone a github repo into a specific directory of a user.
    """
    Repo.clone_from(git_url, repo_dir)
    uid = getpwnam(user).pw_uid
    gid = getpwnam(user).pw_gid
    for root, dirs, files in os.walk(repo_dir):
        for d in dirs:
            shutil.chown(os.path.join(root, d), user=uid, group=gid)
        for f in files:
            shutil.chown(os.path.join(root, f), user=uid, group=gid)


@hookimpl
def tljh_new_user_create(username):
    """
    A function to clone a github repo into a specific directory of a
    JupyterHub user when the server spawns a new notebook instance.
    args: spawner is of type tljh UserCreateSpawner
    """

    user_root_dir = os.path.join("/home", username)
    # get repo url from environment variable
    git_url = os.getenv('REPO_URL')
    # nothing to do if no repo is specified
    if git_url is None:
        return

    repo_dir = os.path.join(user_root_dir, 'repos')

    if not os.path.isdir(repo_dir):
        os.makedirs(repo_dir)
        clone_repo(username, git_url, repo_dir)
    else:
        # user already has the repo downloaded
        pass
