import os


def get_keys_from_ordered_dict(od):
    keys = []
    if isinstance(od, dict):
        for k, v in od.items():
            keys.append(k)
        return keys


def generate_url_for_media_resources(serializer, param):
    for target in serializer.data:
        front = "http" if os.getenv("IS_SECURE") else "https"
        target[param] = "{}://{}{}".format(front, os.getenv("BASE_URL"), target[param])
    return serializer


def generate_url_for_media_resource(serializer, param):
    front = "http" if os.getenv("IS_SECURE") else "https"
    serializer[param] = "{}://{}{}".format(front, os.getenv("BASE_URL"), serializer[param])
    return serializer
