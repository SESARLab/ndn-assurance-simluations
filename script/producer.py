#!/usr/bin/env python3

import logging
import sys
from argparse import ArgumentParser
from os import environ
from random import choices
from string import digits, ascii_lowercase
from typing import Optional, Set

import pandas as pd
from ndn.app import NDNApp
from ndn.encoding import InterestParam, BinaryStr, FormalName, Name

try:
    import asyncio
except ImportError:
    import trollius as asyncio

pd.set_option('display.max_rows', 20)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 600)

SERVER_RESTART_TIMEOUT = 5000.0  # ms
FRESHNESS_PERIOD = 10000  # ms
ALPHABET = ascii_lowercase + digits


def setup_logging():
    logging.basicConfig(
        level=environ.get("LOGLEVEL", "INFO"),
        format="%(levelname)s [%(name)s] %(message)s")


def rand_string(length: int, alphabet=ALPHABET) -> str:
    return ''.join(choices(alphabet, k=length))


setup_logging()
log = logging.getLogger("app:main")


def get_arg_parser() -> ArgumentParser:
    arg_parser = ArgumentParser()
    arg_parser.add_argument("-p", "--prefix", type=str, default="", help="Prefix for all requests")
    arg_parser.add_argument("-f", "--freshness", type=int, default=FRESHNESS_PERIOD,
                            help="Data packet freshness in ms")
    arg_parser.add_argument("-d", "--domain", type=str, help="Path to domain file")
    arg_parser.add_argument("-n", "--n_producers", type=int, help="Number of producers")
    arg_parser.add_argument("-i", "--i_producer", type=int, help="Index of producer")
    arg_parser.add_argument("-l", "--response_length", type=int, default=20, help="Response length")
    return arg_parser


def get_domain(args) -> Set[str]:
    res = None
    if args.domain is not None:
        res = ["/%s/%s" % (args.prefix.strip("/"), d.lstrip("/")) for d in
               pd.read_csv(args.domain)["destination"].unique()]
    if args.n_producers is not None and args.i_producer is not None:
        res = [n for i, n in enumerate(res) if (i % args.n_producers) == args.i_producer]
    if args.domain:
        res = {n for n in res}
    if res is not None:
        log.info("Domain size: %d" % len(res))
        # log.info("Domain: %s" % pformat(res))
    return res


if __name__ == '__main__':
    log.info(sys.argv)
    arg_parser = get_arg_parser()
    args = arg_parser.parse_args()
    log.info(args)
    domain = get_domain(args)

    app = NDNApp()


    @app.route(args.prefix)
    def on_interest(name: FormalName, param: InterestParam, _app_param: Optional[BinaryStr]):

        should_respond = True

        if domain is not None:
            should_respond = False
            target = Name.to_str(name)
            if target in domain:
                should_respond = True

        if should_respond:
            content = rand_string(args.response_length)
            app.put_data(
                name,
                content=content.encode(),
                freshness_period=args.freshness)


    try:
        app.run_forever()
    except (KeyboardInterrupt, SystemExit):
        sys.exit("Ok, bye!")

    print("Completed!")
