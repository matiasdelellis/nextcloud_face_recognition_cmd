#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = [
    'face_recognition>=1.0.0',
    'face_recognition_models>=0.2.0'
]

setup(
    name='nextcloud_face_recognition_cmd',
    version='0.5.0',
    description="Recognize faces tool used to Nextcloud facerecognition app",
    long_description=readme,
    author="Matias De lellis",
    author_email='mati86dl@gmail.com',
    url='https://github.com/matiasdelellis/face_recognition_cmd',
    packages=[
        'nextcloud_face_recognition_cmd',
    ],
    package_dir={'nextcloud_face_recognition_cmd': 'nextcloud_face_recognition_cmd'},
    entry_points={
        'console_scripts': [
            'nextcloud-face-recognition-cmd=nextcloud_face_recognition_cmd.nextcloud_face_recognition_cmd:main'
        ]
    },
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='face_recognition',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
