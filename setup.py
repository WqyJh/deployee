import setuptools

from pipenv.project import Project
from pipenv.utils import convert_deps_to_pip

from deployee import __version__


pfile = Project(chdir=False).parsed_pipfile
requirements = convert_deps_to_pip(pfile['packages'], r=False)
test_requirements = convert_deps_to_pip(pfile['dev-packages'], r=False)

entry_points = {
    'console_scripts': [
        'deployee = deployee.main:main'
    ]
}

setuptools.setup(
    version=__version__,
    install_requires=requirements,
    test_require=test_requirements,
    entry_points=entry_points,
)
