#!/usr/bin/env python

import os

DEPS = [
    dict(name="django-nonrel",
         packages=["django"],
         src="http://bitbucket.org/wkornewald/django-nonrel/get/tip.zip"),
    dict(name="djangoappengine",
         packages=["."],
         src="http://bitbucket.org/wkornewald/djangoappengine/get/tip.zip"),
    dict(name="djangotoolbox",
         packages=["djangotoolbox"],
         src="http://bitbucket.org/wkornewald/djangotoolbox/get/tip.zip"),
    dict(name="django-autoload",
         packages=["autoload"],
         src="http://bitbucket.org/twanschik/django-autoload/get/tip.zip"),
    dict(name="django-dbindexer",
         packages=["dbindexer"],
         src="http://bitbucket.org/wkornewald/django-dbindexer/get/tip.zip"),
    ]

LIB_DIR = "lib"

if __name__ == "__main__":

    curdir = os.getcwd()

    if not os.path.isdir(LIB_DIR):
        os.makedirs(LIB_DIR)
    os.chdir(LIB_DIR)

    try:
        for d in DEPS:
            name = d["name"]
            src = d["src"]
            packages = d["packages"] or []

            if os.path.exists(name):
                print "%s: already downloaded." % name
            else:
                print "%s: downloading..." % name
                os.system("wget -c -O '%s.zip' '%s'" % (name, src))
                print "%s: unzipping..." % name
                os.system("unzip -q '%s.zip'" % name)
                print "%s: renaming..." % name
                os.system("mv -v *-%s-tip %s" % (name, name))

            for packagedir in packages:
                print "%s: linking %s..." % (name, packagedir)
                if packagedir == ".":
                    source = os.path.join(LIB_DIR, name)
                else:
                    source = os.path.join(LIB_DIR, name, packagedir)

                os.system("(cd ..; ln -vsf %s .)" % source)

    finally:
        os.chdir(curdir)
