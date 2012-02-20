Introduction
============
`collective.pfg.sqladapter` adds a form action adapter to PloneFormGen that
saves form input data in a SQL database using SQLAlchemy.

Setup
=====
To install `collective.pfg.sqladapter` add it to the list of eggs in your buildout.

To configure the database, use z3c.saconfig and define a named scoped session
"collective.pfg.sqladapter" in your configure.zcml or in the "zcml-additional" 
parameter of your buildout.

Example::

    <configure xmlns="http://namespaces.zope.org/db">
        <engine name="collective.pfg.sqladapter" url="mysql://user:password@localhost/database" />
        <session name="collective.pfg.sqladapter" engine="collective.pfg.sqladapter" />
    </configure>

Run buildout and restart your instance. Then install the product using Quickinstaller.

Usage
=====
To save form input data in your SQL database add a "SQLAdapter" in your Form Folder
and enter the name of the table where the input data should be stored.

If a table with the given name does not exist in your database, it will be
created with columns corresponding to the fields in your form. Thus the "SQLAdapter"
should be added after all fields were added.
