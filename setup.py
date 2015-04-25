from setuptools import setup, find_packages

requirements = ['six']

desc = ''
with open('README.rst') as f:
    desc = f.read()

setup(
    name='cuckoo',
    version='0.0.1',
    description=(''),
    long_description=(desc),
    url='https://github.com/jmvrbanac/cuckoo',
    author='John Vrbanac',
    author_email='john.vrbanac@linux.com',
    license='Apache License 2.0',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.4',
        'Operating System :: POSIX :: Linux'
    ],
    keywords='',
    packages=find_packages(exclude=['contrib', 'docs', 'spec*']),
    install_requires=requirements,
    package_data={},
    data_files=[],
    entry_points={}
)
