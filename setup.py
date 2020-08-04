from distutils.core import setup
setup(
  name = 'sort_visualizer',
  packages = ['sort_visualizer'],
  version = '1.0.1',
  license='MIT',
  description = 'Python package to visualize any sorting algorithm',
  author = 'dduck',
  author_email = 'famgui14@gmail.com',
  url = 'https://github.com/DirectDuck/sorting_visualizer',
  download_url = 'https://github.com/DirectDuck/sorting_visualizer/archive/1.0.tar.gz',
  keywords = ['SORT', 'SORTING', 'VISUALIZATION', 'VISUALIZE'],
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