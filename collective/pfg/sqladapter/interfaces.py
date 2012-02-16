from zope.interface import Interface


class ISQLAdapter(Interface):
    """A form action adapter that saves form input data in a SQL database"""
