import unittest2 as unittest
from collective.pfg.sqladapter.testing import INTEGRATION_TESTING
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles


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

    # TODO: more tests
