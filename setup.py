from setuptools import setup, find_packages

setup(name='pyspc',
      version='0.1.0',
      description='Library to plot control charts',
      long_description='Statistical Process Control for Humans',
      url='https://github.com/carlosqsilva/pyspc',
      author='Carlos Silva',
      author_email='carlosqsilva@outlook.com',
      license='MIT',
      packages=find_packages(),
      package_dir={ "pyspc": "pyspc" },
      package_data={
      "pyspc": ["sampledata/*.csv"]},
      install_requires=['pandas', 'matplotlib', 'numpy',],
      keywords='SPC CEQ CEP UEPA',
      classifiers=[
      'Intended Audience :: Developers',
      'Intended Audience :: Science/Research',
      'License :: MIT License',
      'Topic :: Scientific/Engineering',
      'Operating System :: Microsoft :: Windows',
      'Operating System :: POSIX',
      'Operating System :: Unix',
      'Operating System :: MacOS',
      'Programming Language :: Python :: 3.3'
      'Programming Language :: Python :: 3.4',
      'Programming Language :: Python :: 3.5'],
      zip_safe=False)