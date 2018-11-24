# Org Protocol Handler #

The Org Protocol Handler is a small AppleScript/Python application that
registers itself as the handler for all `org-protocol://` links.

If your system wants to visit an `org-protocol://` link, it will pass the value
to this application, which will urldecode it and pass it to `emacsclient`. The
net effect is that you can use a bookmarklet to build an `org-protocol://` link
in your browser for things like saving the current page as a link in Org and
that bookmarket will launch and focus Emacs.

## Configuration ##

In order for this application to work for you, you will need to be sure that it
is pointed to the correct copy of `emacsclient` on your system.

Out of the box, it will run `/usr/local/bin/emacsclient`, which should be the
correct copy if you are using Emacs from Homebrew. If you are not, or if that
path differs in some way, you will need to create a configuration file.

Create a file called `~/.orgprotocol.ini`. Note the leading period in the
filename. This file should simply contain these two lines:

```
[emacsclient]
path=/path/to/your/emacsclient
```

## How does it work? ##

In OS X, any application that exists in your root `/Applications` directory and
that contains a `CFBundleURLTypes` stanza in its `Info.plist` will be registered
as a handler for the URL schemes described there.

In the case of this application, the stanza looks like this:

```
<key>CFBundleURLTypes</key>
<array>
    <dict>
        <key>CFBundleURLName</key>
        <string>EmacsClientCapture</string>
        <key>CFBundleURLSchemes</key>
        <array>
            <string>org-protocol</string>
        </array>
    </dict>
</array>
```

In my understanding, the `CFBundleURLName` makes no difference at all, it just
needs to be set to something. When any program on your system attempts to visit
a URL beginning with `org-protocol://`, OS X will launch this application and
hand it the URL through some known OS X API mechanism.

In AppleScript, accessing that data is quite simple, you need only define an `on
open location` subroutine that accepts the whole URL as a string and then you
can do what you like with it.

This application is designed to accept an `org-protocol://` URL and it simply
launches `emacsclient` and hands that URL to it. This enables your
already-running Emacs server to be triggered by `org-protocol://` links from
anywhere on your system.

Neither the `emacsclient` program nor Emacs itself will decode the URL; it
expects to receive a raw URL with spaces and all, but the URL will need to be
encoded to preserve spaces (especially) when the handler is called by your
browser, so this handler uses a small Python script to decode the URL and also
extract the page title from it so we can display a notification.

## Why? ##

In short, so that you can save things from your web browser directly into Org
capture templates or simply save the links to pages for later insertion into Org
documents.
