# Org Protocol Handler #

The Org Protocol Handler is a small AppleScript application that registers
itself as the handler for all `org-protocol://` links.

## Configuration ##

In order for this application to work for you, you will need to be sure that it
is pointed to the correct copy of `emacsclient` on your system.

Out of the box, it will run `/usr/local/bin/emacsclient`, which should be the
correct copy if you are using Emacs from Homebrew. If you are not, or if that
path differs in some way, you will need to open this application in Script
Editor and adjust that path.

## How? ##

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

## Why? ##

In short, so that you can save things from your web browser directly into Org
capture templates or simply save the links to pages for later insertion into Org
documents.
