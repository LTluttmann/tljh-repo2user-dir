from setuptools import setup
setup(
    name="tljh-repo2user-dir",
    url="https://github.com/LTluttmann/tljh-repo2user-dir",
    entry_points={"tljh": ["repo2user-dir = tljh_repo2user_dir"]},
    py_modules=["tljh_repo2user_dir"],
    install_requires=["GitPython"]
)
