from setuptools import setup, find_namespace_packages

setup(name='Personal_assistant',
      version='1',
      description='Personal assistant to manage address book and notebook',
      url='https://github.com/palchyk1984/Personal-assistant-Group-6.git',
      author='GoIT Group-6',
      author_email='alexey.palchik@gmail.com',
      license='MIT',
      packages=find_namespace_packages(),
      install_requires=['markdown-it-py', 'mdurl', 'rich', 'prompt_toolkit', 'Pygments', 'wcwidth'],
      entry_points={'console_scripts': ['Personal_assistant = Personal_assistant.Personal_assistant:main']},
      include_package_data=True,
      package_data={"":["README.md", "requirements.txt"]}
      )