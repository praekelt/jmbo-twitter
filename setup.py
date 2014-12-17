import multiprocessing
from setuptools import setup, find_packages

setup(
    name='jmbo-twitter',
    version='0.4.2',
    description='Pull, cache, display tweets.',
    long_description=(open('README.rst', 'r').read() +
                        open('AUTHORS.rst', 'r').read() +
                        open('CHANGELOG.rst', 'r').read()),
    author='Praekelt Foundation',
    author_email='dev@praekelt.com',
    license='BSD',
    url='http://github.com/praekelt/jmbo-twitter',
    packages = find_packages(),
    install_requires = [
        'python-twitter>=1.1',
        'jmbo>=1.1.1',
        'jmbo-foundry>=1.1.20',
        'django-celery',
        'requests',
    ],
    include_package_data=True,
    tests_require=[
        'django-setuptest>=0.1.4',
        'coverage',
    ],
    test_suite="setuptest.setuptest.SetupTestSuite",
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License",
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    zip_safe=False,
)
