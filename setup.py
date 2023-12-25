from setuptools import setup, find_packages

setup(
    name='Personal-assistant-Group-6-main',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'markdown-it-py==3.0.0',
        'mdurl==0.1.2',
        'prompt-toolkit==3.0.43',
        'Pygments==2.17.2',
        'rich==13.7.0',
        'wcwidth==0.2.12',
    ],
   entry_points={
    'console_scripts': ['personal-assistant=personal_assistant:main'],
},


)
