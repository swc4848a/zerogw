import logging

from . import loop
from . import chat
from . import auth

def get_options():
    from argparse import ArgumentParser
    ap = ArgumentParser()
    ap.add_argument('--auth-connect', metavar="ZMQADDR",
        help="Zerogw's main forwarding address (repeatable)",
        default=[], action="append")
    ap.add_argument('--auth-bind', metavar="ZMQADDR",
        help="Zerogw's main forwarding address (repeatable)",
        default=[], action="append")
    ap.add_argument('--chat-connect', metavar="ZMQADDR",
        help="Zerogw's chat route address (repeatable)",
        default=[], action="append")
    ap.add_argument('--chat-bind', metavar="ZMQADDR",
        help="Zerogw's chat route address (repeatable)",
        default=[], action="append")
    ap.add_argument('--output-connect', metavar="ZMQADDR",
        help="Zerogw's subsription address (repeatable)",
        default=[], action="append")
    ap.add_argument('--output-bind', metavar="ZMQADDR",
        help="Zerogw's subsription address (repeatable)",
        default=[], action="append")
    ap.add_argument('--log-file', metavar="FILE",
        help="Log file name",
        dest="log_file", default="./run/python.log")
    ap.add_argument('--redis-socket', metavar="FILE",
        help="Redis socket (only unix sockets supported)",
        dest="redis_sock", default='./run/redis.sock')
    return ap

def main():
    ap = get_options()
    options = ap.parse_args()

    logging.basicConfig(filename=options.log_file, level=logging.WARNING)

    lp = loop.Loop()
    lp.add_output('output',
        connect=options.output_connect,
        bind=options.output_bind,
        )
    lp.add_redis('redis', socket=options.redis_sock)
    lp.add_service('auth', auth.Service(),
        connect=options.auth_connect,
        bind=options.auth_bind,
        )
    lp.add_service('chat', chat.Service(),
        connect=options.chat_connect,
        bind=options.chat_bind,
        )
    lp.run()

if __name__ == '__main__':
    main()
