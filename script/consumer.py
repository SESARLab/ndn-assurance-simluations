#!/usr/bin/env python3
import asyncio as aio
import logging
import sys
import time
from argparse import ArgumentParser
from itertools import cycle
from os import environ
from pprint import pprint
from urllib.parse import unquote

import numpy as np
import pandas as pd
from ndn.app import NDNApp
from ndn.encoding import Name
from ndn.types import InterestNack, InterestTimeout, InterestCanceled, ValidationFailure
from numpy import random

pd.set_option('display.max_rows', 20)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 600)

np.random.seed = 123


def setup_logging():
    logging.basicConfig(
        level=environ.get("LOGLEVEL", "INFO"),
        format="%(levelname)s [%(name)s] %(message)s")


setup_logging()
app = NDNApp()

if __name__ == '__main__':
    log = logging.getLogger("app:main")

    arg_parser = ArgumentParser()
    arg_parser.add_argument("-p", "--prefixes", type=str, nargs="*", help="Prefix for all requests")
    arg_parser.add_argument("-i", "--interval", type=float, default=1.0, help="Time between requests")
    arg_parser.add_argument("-r", "--range", type=int, nargs=2, help="Range of requests")
    arg_parser.add_argument("-z", "--zipf", type=float, help="Zipf alpha parameter")
    # arg_parser.add_argument("-l", "--length", type=int, help="Max name length")
    arg_parser.add_argument("-lt", "--log-times", type=str, help="Log requests RTT")
    arg_parser.add_argument("--dry", "--dry-run", action="store_true", help="Only print requests")
    arg_parser.add_argument("--n_consumers", type=int)
    arg_parser.add_argument("--consumer_id", type=int)
    arg_parser.add_argument("--info", action="store_true", help="Only print dataset info")
    arg_parser.add_argument("requests", type=str, help="File containing the requests")

    print(sys.argv)
    args = arg_parser.parse_args()
    print("ARGS:", args)

    requests = pd.read_csv(args.requests, keep_default_na=False)["destination"].unique()

    log.info(args)

    if args.prefixes is not None:
        pref = args.prefixes
        l_pref = len(args.prefixes)
        requests = ["/%s/%s" % (pref.strip("/"), r.lstrip("/")) for pref, r in zip(cycle(args.prefixes), requests)]

    if args.range is not None:
        requests = requests[args.range[0]:args.range[1]]

    if args.n_consumers is not None and args.consumer_id is not None:
        requests = [r for i, r in enumerate(requests)
                    if i % args.n_consumers == args.consumer_id]

    if args.info:
        print("Content domain: %d" % len(requests))
        pprint(requests[:5])
        print("...")
        pprint(requests[-6:-1])
        exit(0)

    generator = random.default_rng()
    weights = None
    if args.zipf:
        n = len(requests)
        x = np.arange(1, n + 1)
        a = args.zipf
        weights = x ** (-a)
        weights /= weights.sum()


    async def send_request(name: Name):
        interest_time = time.time()
        try:
            data_name, meta_info, content = await app.express_interest(
                name=name, must_be_fresh=False, can_be_prefix=True, lifetime=5000)
            data_time = time.time()
            log.info(
                "%.5f [%.5f] Data: %s -> %s" % (
                    time.time(), data_time - interest_time, unquote(Name.to_str(data_name)),
                    content.tobytes().decode("utf-8")))
        except InterestNack as e:
            log.warning("NACK: %s (%s)" % (unquote(str(name)), e.reason))
        except InterestTimeout:
            log.warning("Timeout: %s" % unquote(name))
        except InterestCanceled:
            log.warning("Interest cancelled")
        except ValidationFailure:
            log.warning("Data failed to validate")


    async def iter_requests():
        while True:
            name = str(random.choice(requests, replace=True, p=weights))
            if args.dry:
                log.info("Dry: %s" % Name.to_str(name))
                return
            aio.ensure_future(send_request(name))
            await aio.sleep(args.interval)
            # await asyncio.gather(
            #     send_request(name),
            #     asyncio.sleep(args.interval))


    # Run client and check for exceptions
    try:
        app.run_forever(after_start=iter_requests())
    except (KeyboardInterrupt, SystemExit):
        sys.exit("Ok, bye!")

    print("Completed!")
