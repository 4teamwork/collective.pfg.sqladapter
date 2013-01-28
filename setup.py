from setuptools import setup, find_packages
import os

version = '1.0.1.dev0'

tests_require = [
    'plone.app.testing',
    ]

setup(name='collective.pfg.sqladapter',
      version=version,
      description="A PloneFormGen adapter that saves form input data in a SQL database",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),

      # Get more strings from
      # http://www.python.org/pypi?%3Aaction=list_classifiers

      classifiers=[
        'Framework :: Plone',
        'Framework :: Plone :: 4.1',
        'Framework :: Plone :: 4.2',
        'Programming Language :: Python',
        ],

      keywords='',
      author='4teamwork GmbH',
      author_email='mailto:info@4teamwork.ch',
      url='https://github.com/4teamwork/collective.pfg.sqladapter',
      license='GPL2',

      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective', 'collective.pfg'],
      include_package_data=True,
      zip_safe=False,

      install_requires=[
          'setuptools',
          'Products.PloneFormGen',
          'z3c.saconfig',
      ],

      extras_require=dict(tests=tests_require),
      tests_require=tests_require,

      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
