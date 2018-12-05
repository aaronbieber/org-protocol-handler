#!/usr/bin/env python

import sys
import urlparse
import urllib
import subprocess
import os
import ConfigParser


def read_config():
    ini_path = os.path.expanduser("~/.orgprotocol.ini")
    config = ConfigParser.ConfigParser()
    config.read([ini_path])
    path = emacsclient_path(config)
    options = emacsclient_options(config)
    cmd = path + options
    return cmd


def emacsclient_path(config):
    """Get the configured path to `emacsclient`, or the default."""
    try:
        path = config.get("emacsclient", "path")
    except Exception, e:
        path = "/usr/local/bin/emacsclient"
    return [path]


def emacsclient_options(config):
    """Unpack options from config file"""
    try:
        return dict(config.items('options')).values()
    except Exception, e:
        return []


def is_old_style_link(url):
    """Determine which version of org-protocol link this URL is.

    The 'old style' link looks like:
    org-protocol://capture://<template>/<URL>/<title>/<body>

    While 'new style' links look like:
    org-protocol://capture?template=<template>&url=<URL>&title=<title>&body=<body>
    """
    return url.count("://") == 2


def get_new_style_title(url):
    """Get the title from a new style URL."""
    url_fragments = urlparse.urlparse(url)

    # url_fragments is a 6 tuple; index 4 is the querystring
    if not len(url_fragments[4]):
        return ""

    qs_parts = urlparse.parse_qs(url_fragments[4])

    if "title" in qs_parts.keys() and len(qs_parts["title"]):
        return qs_parts["title"][0]

    return ""


def get_old_style_title(url):
    """Get the title from an old style URL."""
    url_fragments = urlparse.urlparse(url)

    path_parts = url_fragments[2].split("/")
    return urllib.unquote(path_parts[4])


def get_title(url, is_old_style=True):
    """Get the title from an org-protocol URL."""

    if is_old_style:
        return get_old_style_title(url)

    return get_new_style_title(url)


def main():
    if len(sys.argv) < 2:
        sys.exit(1)

    url = sys.argv[1]
    raw_url = urllib.unquote(url)
    cmd = read_config()
    cmd.append(raw_url)
    subprocess.check_output(cmd)
    print(get_title(url, is_old_style_link(url)))


if __name__ == '__main__':
    main()
