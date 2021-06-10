import os
import random
import string
import json
import urllib
import urllib.request
from urllib.parse import urlparse


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
    serializer[param] = "{}://{}{}".format(
        front, os.getenv("BASE_URL"), serializer[param]
    )
    return serializer


def get_random_alphanumeric_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    result_str = "".join((random.choice(letters_and_digits) for i in range(length)))
    return result_str


def set_max_res_thumbnail(data):
    slitted = data['thumbnail_url'].split("/")
    slitted.pop()
    slitted.append("maxresdefault.jpg")
    slitted = "/".join(slitted)
    data['thumbnail_url'] = slitted
    return data


def get_id_of_youtube_url(video_url):
    url_data = urllib.parse.urlparse(video_url)
    query = urllib.parse.parse_qs(url_data.query)
    video = query["v"][0]
    return video


def get_youtube_video_data(video_url):
    video_id = get_id_of_youtube_url(video_url)

    params = {
        "format": "json",
        "url": "https://www.youtube.com/watch?v=%s" % video_id
    }

    url = "https://www.youtube.com/oembed"

    query_string = urllib.parse.urlencode(params)
    url = url + "?" + query_string

    with urllib.request.urlopen(url) as response:
        response_text = response.read()
        data = json.loads(response_text.decode())
        return set_max_res_thumbnail(data)
