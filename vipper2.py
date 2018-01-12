#!/usr/bin/env python3
"""

              _.---..._     
           ./^         ^-._       
         ./^C===.         ^\.   /\
        .|'     \\        _ ^|.^.|
   ___.--'_     ( )  .      ./ /||
  /.---^T\      ,     |     / /|||
 C'   ._`|  ._ /  __,-/    / /-,||  thanks for visiting 
      \ \/    ;  /O  / _    |) )|,  this fine file
       i \./^O\./_,-^/^    ,;-^,'      
        \ |`--/ ..-^^      |_-^       
         `|  \^-           /|:       
          i.  .--         / '|.                                   
           i   =='       /'  |\._                                 
         _./`._        //    |.  ^-ooo.._                        
  _.oo../'  |  ^-.__./X/   . `|    |#######b                  
 d####     |'      ^^^^   /   |    _\#######               
 #####b ^^^^^^^^--. ...--^--^^^^^^^_.d######                
 ######b._         Y            _.d#########              
 ##########b._     |        _.d#############   
"""
import asyncio
import re

import discord

import api
import handlers
import settings


CLIENT = discord.Client()

@CLIENT.event
@asyncio.coroutine
def on_message(message):
    print('[{channel}] <{username}> {message}'.format(
        channel=message.channel.name,
        username=message.author,
        message=message.content))


    # test regexps in dispatch table
    if message.author != CLIENT.user:
        for regexp, args, handler in api.DISPATCH_TABLE:
            if re.match(regexp, message.content, *args):
                yield from handler(CLIENT, message)
    
    
def main():
    CLIENT.run(settings.TOKEN)


if __name__ == '__main__':
    main()
    
