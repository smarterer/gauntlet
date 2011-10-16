#!/usr/bin/env python

import os

DEPS = [
    dict(name="django-nonrel",
         src="http://bitbucket.org/wkornewald/django-nonrel/get/tip.zip"),
    dict(name="djangoappengine",
         src="http://bitbucket.org/wkornewald/djangoappengine/get/tip.zip"),
    dict(name="djangotoolbox",
         src="http://bitbucket.org/wkornewald/djangotoolbox/get/tip.zip"),
    dict(name="django-autoload",
         src="http://bitbucket.org/twanschik/django-autoload/get/tip.zip"),
    dict(name="django-dbindexer",
         src="http://bitbucket.org/wkornewald/django-dbindexer/get/tip.zip"),
    ]

if __name__ == "__main__":
    for d in DEPS:
        name = d["name"]
        src = d["src"]
        if os.path.exists(name):
            print "%s: already installed." % name
        else:
            print "%s: downloading..." % name
            os.system("wget -c -O '%s.zip' '%s'" % (name, src))
            print "%s: unzipping..." % name
            os.system("unzip -q '%s.zip'" % name)
            print "%s: renaming..." % name
            os.system("mv -v *-%s-tip %s" % (name, name))
