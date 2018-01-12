"""Holds handles for regexps defined in vipper2.DISPATCH_TABLE.

Each of these functions is called when the message matches the listed
regexp.
"""
from sqlalchemy import create_engine

import api
import settings


# SQL Alchemy Engine for the Byes Databases. Used by the byes handler
BYES_ENGINE = create_engine('mysql://{user}:{passwd}@{hostname}/{dbname}'.format(
    user=settings.MARIADB_USER,
    passwd=settings.MARIADB_PASSWORD,
    hostname=settings.MARIADB_HOSTNAME,
    dbname=settings.MARIADB_BYES_DB
))


@api.bot_response('(.*)bye(.*)')
def handle_bye(client, message):
    """Handler for message containing bye. Responds with a random bye from the
    byes database table and adds the message to the database table if it doesn't
    already exist.
    
    Args
    ----
    client : discord client
    message : discord message
    """
    # Add to database after checking for existence
    lookup_query = 'SELECT * FROM {table} WHERE bye = %s LIMIT 1'.format(
        table=settings.MARIADB_BYES_TABLE)
    
    cursor = BYES_ENGINE.connect()
    results = cursor.execute(lookup_query, message.content)
    row_exists = bool(list(results))

    if not row_exists:
        insert_query = 'INSERT INTO {table} (bye) VALUES (%s)'.format(
            table=settings.MARIADB_BYES_TABLE)
        cursor.execute(insert_query, message.content)

    # Query a random bye
    rand_query = 'SELECT bye FROM {table} ORDER BY RAND() LIMIT 1'.format(
        table=settings.MARIADB_BYES_TABLE)
    results = list(cursor.execute(rand_query))
    
    if results:
        content = results.pop()[0]
        yield from client.send_message(message.channel, content)

