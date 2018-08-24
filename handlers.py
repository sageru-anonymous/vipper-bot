"""Holds handles for regexps defined in api.DISPATCH_TABLE.

Each of these functions is called when the message matches the listed regexp.
"""
import random
import re

from nltk.tokenize import word_tokenize
from sqlalchemy import create_engine

import api
import settings

@api.bot_response('^irc$')
def handle_irc(client, message):
    yield from client.send_message(message.channel, 'rip')
                  


@api.bot_response('^!timeout$')
def handle_timeout(client, message):
    target = str(message.author).split('#')[0]

    yield from client.send_message(
        message.channel,
        "_puts {target} in time out_"
        .format(target=target)
    )


@api.bot_response('^!kill (.*)$')
def handle_kill(client, message):
    """Handler for !kill commmand. The Dragon Eats You Game.

    Args
    ----
    client : discord client
    message : discord message
    """
    rand_val = random.randint(1, 6)
    target = message.content.split(' ')[1]
    source = str(message.author).split('#')[0]
    
    if rand_val == 1:
        yield from client.send_message(
            message.channel,
            "{source} rolled the die, and it landed on 1.... A dragon "
            "eats {target}!"
            .format(source=source, target=target)
        )
    else:
        yield from client.send_message(
            message.channel,
            "{source} rolled the die, and it landed on {rand_val}. The dragon "
            "eats him!"
            .format(source=source, rand_val=rand_val)
        )


@api.bot_response('^penis$')
def handle_penis(client, message):
    """Handler for message containing the string "penis". Replies by saying
    "yes".

    Args
    ----
    client : discord client
    message : discord message
    """
    yield from client.send_message(message.channel, 'yes')


@api.bot_response('^pump$')
def handle_pump(client, message):
    """Handler for message containing the string "pump". Replies by saying
    "yes".

    Args
    ----
    client : discord client
    message : discord message
    """
    yield from client.send_message(message.channel, 'yes')


@api.bot_response('^same$')
def handle_same(client, message):
    """Handler for message containing the string "same". Replies by saying same
    as well.
    
    Args
    ----
    client : discord client
    message : discord message
    """
    yield from client.send_message(message.channel, 'same')


@api.bot_response('^nice$')
def handle_nice(client, message):
    """Handler for message containing the string "nice". Replies by saying nice
    as well.
    
    Args
    ----
    client : discord client
    message : discord message
    """
    yield from client.send_message(message.channel, 'nice')


@api.bot_response(r'^o/$')
def handle_cheer_right(client, message):
    """Handler for message containing the string "o/". Replies by saying "\o".

    Args
    ----
    client : discord client
    message : discord message
    """
    yield from client.send_message(message.channel, '\o')



@api.bot_response(r'^\\o$')
def handle_cheer_left(client, message):
    """Handler for message containing the string "\o". Replies by saying "o/".

    Args
    ----
    client : discord client
    message : discord message
    """
    yield from client.send_message(message.channel, 'o/')
    


@api.bot_response('^amirite$')
def handle_amirite(client, message):
    """Handler for message containing the string "amirite". Replies by saying
    "yes".

    Args
    ----
    client : discord client
    message : discord message
    """
    yield from client.send_message(message.channel, 'yes')


    
@api.bot_response('^:3$')
def handle_colonthree(client, message):
    """Handler for message containing the string ":3". Replies by saying ":3"

    Args
    ----
    client : discord client
    message : discord message
    """
    yield from client.send_message(message.channel, ':3')


@api.bot_response('^jews$')
def handle_jews(client, message):
    """Handler for message containing the string "jews". Replies by saying
    "did wtc".

    Args
    ----
    client : discord client
    message : discord message
    """
    yield from client.send_message(message.channel, 'did wtc')


@api.bot_response('^cocks$')
def handle_jews(client, message):
    """Handler for message containing the string "cocks". Replies by saying
    "ill suck em".

    Args
    ----
    client : discord client
    message : discord message
    """
    yield from client.send_message(message.channel, 'ill suck em')

    
@api.bot_response('^(.*)(bye|no)(.*)$', re.IGNORECASE)
def handle_bye(client, message):
    """Handler for message containing bye. Responds with a random bye from the
    byes database table and adds the message to the database table if it doesn't
    already exist.
    
    Args
    ----
    client : discord client
    message : discord message
    """
    tokens = [tok.lower() for tok in word_tokenize(message.content)]

    if 'bye' in tokens:
        table = settings.MARIADB_BYES_TABLE
    elif 'no' in tokens:
        table = settings.MARIADB_NOS_TABLE
    else:
        return
        
    # SQL Alchemy Engine for the Byes Databases.
    byes_engine = create_engine('mysql://{user}:{passwd}@{hostname}/{dbname}'
                                .format(
                                    user=settings.MARIADB_USER,
                                    passwd=settings.MARIADB_PASSWORD,
                                    hostname=settings.MARIADB_HOSTNAME,
                                    dbname=settings.MARIADB_BYES_DB
                                ))
    cursor = byes_engine.connect()

    # Add to database after checking for existence
    lookup_query = 'SELECT * FROM {table} WHERE bye = %s LIMIT 1'.format(
        table=table)
    results = cursor.execute(lookup_query, message.content)
    row_exists = bool(list(results))

    if not row_exists:
        insert_query = 'INSERT INTO {table} (bye) VALUES (%s)'.format(
            table=table)
        cursor.execute(insert_query, message.content)

    # Query a random bye if message is just 'bye' or 'no'
    if message.content.lower() in ('no', 'bye'):
        rand_query = 'SELECT bye FROM {table} ORDER BY RAND() LIMIT 1'.format(
            table=table)
        results = list(cursor.execute(rand_query))
        
        if results:
            content = results.pop()[0]
            yield from client.send_message(message.channel, content)

 
