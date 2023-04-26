import os
import shutil
from pwd import getpwnam
from git import Repo
from tljh.hooks import hookimpl
import logging


logger = logging.getLogger(__name__)
flog = logging.FileHandler("/home/tdi2023/usrhooks.log")
flog.setFormatter(logging.Formatter("%(asctime)s %(message)s"))
logger.addHandler(flog)
logger.setLevel(logging.INFO)


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
    logger.info("Gonna clone for user %s" % username)
    user_root_dir = os.path.join("/home", username)
    # get repo url from environment variable
    git_url = os.getenv("REPO_URL", "https://github.com/LTluttmann/tljh-repo2user-dir.git")
    # nothing to do if no repo is specified
    if git_url is None:
        logger.warning("No repo url found in environment variables. Skip cloning")
        return
    
    logger.info("Cloning repo %s" % git_url)
    repo_dir = os.path.join(user_root_dir, 'repos')

    if not os.path.isdir(repo_dir):
        os.makedirs(repo_dir)
        clone_repo(username, git_url, repo_dir)
        logger.info("Done cloning")
    else:
        # user already has the repo downloaded
        logger.info("User already got repo")
