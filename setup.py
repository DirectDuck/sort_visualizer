import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
  name = 'sort_visualizer',
  packages = ['sort_visualizer'],
  version = '1.0.4',
  license='MIT',
  description = 'Python package to visualize any sorting algorithm',
  long_description=README,
  long_description_content_type="text/markdown",
  author = 'dduck',
  author_email = 'famgui14@gmail.com',
  url = 'https://github.com/DirectDuck/sorting_visualizer',
  download_url = 'https://github.com/DirectDuck/sorting_visualizer/archive/1.0.4.tar.gz',
  keywords = ['SORT', 'SORTING', 'VISUALIZATION', 'VISUALIZE'],
  include_package_data=True,
  install_requires=[
          'PySimpleGUI',
      ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)