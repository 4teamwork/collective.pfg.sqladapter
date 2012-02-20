from zope.interface import implements
from AccessControl import ClassSecurityInfo
from Products.Archetypes import atapi
from Products.ATContentTypes.content import schemata
from Products.PloneFormGen.interfaces import IPloneFormGenActionAdapter
from Products.PloneFormGen.content.actionAdapter import FormAdapterSchema
from Products.PloneFormGen.content.actionAdapter import FormActionAdapter
from Products.PloneFormGen.config import FORM_ERROR_MARKER
from ZPublisher.HTTPRequest import FileUpload
from sqlalchemy import MetaData, Table
from sqlalchemy.exc import NoSuchTableError
from z3c.saconfig import named_scoped_session
from collective.pfg.sqladapter.interfaces import ISQLAdapter
from collective.pfg.sqladapter.config import PROJECTNAME
from collective.pfg.sqladapter import _


SQLAdapterSchema = FormAdapterSchema.copy() + atapi.Schema((

    atapi.StringField(
        'tablename',
        required=True,
        widget=atapi.StringWidget(
            label=_(u"label_tablename", default=u"Table Name"),
            description=_(u"help_tablename",
                default=u"Provide the name of the table where form input "
                         "data should be saved to. If the table doesn't "
                         "exist yet, it will be created."),
         ),
    ),

))

schemata.finalizeATCTSchema(SQLAdapterSchema, moveDiscussion=False)


class SQLAdapter(FormActionAdapter):
    """A form action adapter that saves form input data in a SQL database"""
    implements(IPloneFormGenActionAdapter, ISQLAdapter)

    portal_type = "SQLAdapter"
    schema = SQLAdapterSchema
    security = ClassSecurityInfo()

    def onSuccess(self, fields, REQUEST=None):
        """Save form input in SQL database.
        """

        session = self.getSession()
        metadata = MetaData(bind=session.bind)
        try:
            table = Table(self.getTablename(), metadata, autoload=True)
        except NoSuchTableError:
            return { FORM_ERROR_MARKER: 'Your form input could not be saved. '
                     'No such table: %s' % self.getTablename() }

        record = {}
        for field in fields:
            fname = field.fgField.getName()
            if fname in table.columns:
                val = REQUEST.form.get(fname, '')
                if field.isFileField():
                    file_ = REQUEST.form.get('%s_file' % fname)
                    if isinstance(file_, FileUpload) and file_.filename != '':
                        file_.seek(0)
                        val = file_.read()
                elif isinstance(val, str):
                    val = val.decode('utf-8')
                elif isinstance(val, list):
                    val = '\n'.join(val).decode('utf-8')
                record[fname] = val
        if record:
            # TODO: use the session for inserts
            #session.execute(table.insert().values(record))
            table.insert().execute(record)

    security.declarePrivate("getSession")
    def getSession(self):
        Session = named_scoped_session('collective.pfg.sqladapter')
        return Session()

atapi.registerType(SQLAdapter, PROJECTNAME)
