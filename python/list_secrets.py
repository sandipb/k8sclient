from kubernetes import client, config
import argparse
import logging
import urllib3

urllib3.disable_warnings()


def setup() -> argparse.Namespace:
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--namespace", default="default", help="Namespace")
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
        ret = client.CoreV1Api().list_namespaced_config_map(args.namespace)
    except Exception as e:
        logging.fatal("Could not get secrets: %s", e)

    for i in ret.items:
        print(i.metadata.name)
