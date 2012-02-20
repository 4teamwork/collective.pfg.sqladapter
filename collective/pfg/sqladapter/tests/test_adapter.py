import unittest2 as unittest
from collective.pfg.sqladapter.testing import INTEGRATION_TESTING
from collective.pfg.sqladapter.handlers import create_table
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from zope.configuration import xmlconfig
from sqlalchemy import MetaData
from StringIO import StringIO
import z3c.saconfig


class TestSQLAdapter(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def test_correctly_installed(self):
        portal = self.layer['portal']
        self.assertIn('SQLAdapter', portal.portal_types.objectIds())
        self.assertIn('SQLAdapter', portal.portal_factory.getFactoryTypes())

    def test_creation(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Contributor'])
        form = portal[portal.invokeFactory('FormFolder', 'form')]
        sql_adapter = form[form.invokeFactory('SQLAdapter', 'sql')]
        self.assertEqual(sql_adapter.portal_type, 'SQLAdapter')

    def test_table_creation(self):
        # Configure the db
        xmlconfig.XMLConfig('meta.zcml', z3c.saconfig)()
        xmlconfig.xmlconfig(StringIO("""
        <configure xmlns="http://namespaces.zope.org/db">
            <engine name="collective.pfg.sqladapter" url="sqlite:///:memory:" />
            <session name="collective.pfg.sqladapter" engine="collective.pfg.sqladapter" />
        </configure>"""))

        # Create a form folder with a sql adapter
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Contributor'])
        form = portal[portal.invokeFactory('FormFolder', 'form')]
        sql_adapter = form[form.invokeFactory('SQLAdapter', 'sql', tablename='table1')]
        create_table(sql_adapter, None)

        # Verify the created table
        metadata = MetaData(bind=sql_adapter.getSession().bind)
        metadata.reflect()
        self.assertIn('table1', metadata.tables)
        table = metadata.tables['table1']
        for field in sql_adapter.fgFields():
            self.assertIn(field.getName(), table.columns)

    def test_saving_data(self):
        # Configure the db
        xmlconfig.XMLConfig('meta.zcml', z3c.saconfig)()
        xmlconfig.xmlconfig(StringIO("""
        <configure xmlns="http://namespaces.zope.org/db">
            <engine name="collective.pfg.sqladapter" url="sqlite:///:memory:" />
            <session name="collective.pfg.sqladapter" engine="collective.pfg.sqladapter" />
        </configure>"""))

        # Create a form folder with a sql adapter
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Contributor'])
        form = portal[portal.invokeFactory('FormFolder', 'form')]
        sql_adapter = form[form.invokeFactory('SQLAdapter', 'sql', tablename='table1')]
        create_table(sql_adapter, None)

        # Fill the request with some test values and call the adapter
        fields = [fo for fo in form._getFieldObjects()]
        request = self.layer['request']
        request.form.update({'replyto': 'foo@bar.com', 'topic': 'Test', 'comments': 'Foo bar'})
        sql_adapter.onSuccess(fields, request)

        # Verify the data stored in the table
        session = sql_adapter.getSession()
        res = session.execute("SELECT * FROM table1")
        self.assertEquals(res.fetchone(), (1, u'foo@bar.com', u'Test', u'Foo bar'))
