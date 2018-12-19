from setuptools import setup
setup(
    name = 'pdpy',
    packages = ['pdpy'],
    version = '0.1.2',
    description = 'A package for downloading data from the Parliamentary Data Platform',
    author = 'Oliver Hawkins',
    author_email = 'oli@olihawkins.com',
    url = 'https://github.com/olihawkins/pdpy',
    license = 'BSD',
    download_url = 'https://github.com/olihawkins/pdpy/tarball/0.1.0',
    keywords = ['Parliament', 'MP', 'House of Commons', 'House of Lords'],
    install_requires = ['numpy', 'pandas', 'requests'],
    classifiers = [],
)
