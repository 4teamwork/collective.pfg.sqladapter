from sqlalchemy import MetaData, Table, Column, Sequence
from sqlalchemy import String, Text, Boolean, Integer, DateTime, Float, LargeBinary


def get_column(field):
    """Get an appropriate SA column for the given AT field.
    """
    name = field.getName()
    type_ = field.type
    if type_ == 'string':
        return Column(name, String(255))
    elif type_ in ['text', 'lines']:
        return Column(name, Text)
    elif type_ == 'boolean':
        return Column(name, Boolean)
    elif type_ == 'integer':
        return Column(name, Integer)
    elif type_ == 'datetime':
        return Column(name, DateTime)
    elif type_ == 'fixedpoint':
        return Column(name, Float)
    elif type_ in ['file', 'image']:
        return Column(name, LargeBinary)
    return None


def create_table(obj, event):
    """Create the table in the database.
    """
    table_name = obj.getTablename()
    session = obj.getSession()
    metadata = MetaData(bind=session.bind)
    metadata.reflect()

    # Table already exists
    if table_name in metadata.tables:
        return

    # Create a bare table
    table = Table(table_name, metadata,
        Column('id', Integer, Sequence('id_seq'), primary_key = True),
    )

    # Add columns for each form field
    for field in obj.fgFields():
        column = get_column(field)
        if column is not None:
            table.append_column(column)

    metadata.create_all(session.bind)
