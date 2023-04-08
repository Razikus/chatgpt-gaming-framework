#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ "pydantic>=1.9.2", "redis>=4.3.4" ]

test_requirements = [ ]

setup(
    author="Adam Raźniewski",
    author_email='adam.razniewski@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="ChatGPT (in future other LLM) gaming framework",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='chatgpt_gaming_framework',
    name='chatgpt_gaming_framework',
    packages=find_packages(include=['chatgpt_gaming_framework', 'chatgpt_gaming_framework.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/Razikus/chatgpt_gaming_framework',
    version='0.1.0',
    zip_safe=False,
)
