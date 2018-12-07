#!/usr/bin/env python

from __future__ import print_function
from __future__ import absolute_import
from six.moves import configparser
import os
import subprocess
import sys
import six.moves.urllib.request, six.moves.urllib.parse, six.moves.urllib.error
import six.moves.urllib.parse


def read_config():
    """Read and parse ~/.orgprotocol.ini if it exists."""
    ini_path = os.path.expanduser("~/.orgprotocol.ini")
    config = six.moves.configparser.ConfigParser()
    try:
        config.read([ini_path])
    except Exception:
        print("Error reading %s" % ini_path)
    return config


def emacs_client_command(config):
    """Construct a list, each member of which is a part of the
    `emacsclient` command to be run by `subprocess` and used in
    main.scpt. Provides the default `emacsclient` executable if
    ~/.orgprotocol.ini doesn't exist."""
    path = emacsclient_path(config)
    options = emacsclient_options(config)
    cmd = path + options
    return cmd


def emacsclient_path(config):
    """Get the configured path to `emacsclient`, or the default."""
    try:
        path = config.get("emacsclient", "path")
    except Exception:
        path = "/usr/local/bin/emacsclient"
    return [path]


def emacsclient_options(config):
    """Unpack options from config file.  Options are appeneded to the final
    `emacsclient` command.  Returns an empty list if no options are specified.
    """
    try:
        return list(dict(config.items("options")).values())
    except Exception:
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
    url_fragments = six.moves.urllib.parse.urlparse(url)

    # url_fragments is a 6 tuple; index 4 is the querystring
    if not len(url_fragments[4]):
        return ""

    qs_parts = six.moves.urllib.parse.parse_qs(url_fragments[4])

    if "title" in list(qs_parts.keys()) and len(qs_parts["title"]):
        return qs_parts["title"][0]

    return ""


def get_old_style_title(url):
    """Get the title from an old style URL."""
    url_fragments = six.moves.urllib.parse.urlparse(url)

    path_parts = url_fragments[2].split("/")
    return six.moves.urllib.parse.unquote(path_parts[4])


def get_title(url, is_old_style=True):
    """Get the title from an org-protocol URL."""

    if is_old_style:
        return get_old_style_title(url)

    return get_new_style_title(url)


def main():
    if len(sys.argv) < 2:
        sys.exit(1)

    url = sys.argv[1]
    raw_url = six.moves.urllib.parse.unquote(url)
    config = read_config()
    cmd = emacs_client_command(config)
    cmd.append(raw_url)
    subprocess.check_output(cmd)
    print(get_title(url, is_old_style_link(url)))


if __name__ == '__main__':
    main()
