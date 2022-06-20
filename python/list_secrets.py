#!/usr/bin/env python
from kubernetes import client, config  # type: ignore
import argparse
import logging
import urllib3  # type: ignore

urllib3.disable_warnings()


def setup() -> argparse.Namespace:
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description="List names of all secrets or configmaps in a namespace")
    parser.add_argument("-n", "--namespace", default="default", help='Namespace (default: "%(default)s")')
    parser.add_argument("-c", "--config-maps", action="store_true", help="Show config maps instead of secrets")
    parser.add_argument("-d", "--debug", action="store_true", help="Debug logging")
    args = parser.parse_args()
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    logging.debug("Using arguments: %s", args)
    return args


if __name__ == "__main__":
    args = setup()
    try:
        config.load_kube_config()
    except Exception as e:
        logging.fatal("Could not load config: %s", e)

    try:
        ret = (client.CoreV1Api().list_namespaced_secret(args.namespace)
            if not args.config_maps
            else client.CoreV1Api().list_namespaced_config_map(args.namespace))
    except Exception as e:
        logging.fatal("Could not get data: %s", e)

    for i in ret.items:
        print(i.metadata.name)
