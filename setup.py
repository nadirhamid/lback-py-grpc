try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

from distutils.command.build_py import build_py
from distutils.command.install import install

class installsetup(install):
    def run(self):
      install.run(self)

deps = [
   "grpcio==1.0.0",
   "grpcio-tools==1.2.1",
   "futures==3.1.1"
]

setup(name="LinuxOpenSuseBackupToolGRPC",
      version="0.1.0",
      description="GRPC for Lback",
      maintainer="Nadir Hamid",
      maintainer_email="matrix.nad@gmail.com",
      url="https://",
      download_url = "https://pypi.python.org/pypi/",
      license="MIT",
      long_description="",
      packages=["lback_grpc"],
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: Implementation :: CPython',
          'Programming Language :: Python :: Implementation :: PyPy',
          'Topic :: Communications',
          'Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware',
          'Topic :: Internet :: WWW/HTTP :: WSGI :: Server',
          'Topic :: Software Development :: Libraries :: Python Modules'
      ],
      install_requires=deps,
      cmdclass=dict(install=installsetup))
