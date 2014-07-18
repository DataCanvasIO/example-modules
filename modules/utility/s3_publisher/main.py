#!/usr/bin/env python
# -*- coding: utf-8 -*-

from specparser import HadoopRuntime
from collections import OrderedDict
import boto
import json
import os
import sys
from StringIO import StringIO

def s3_delete(s3_path, settings):
    from urlparse import urlparse
    pr = urlparse(s3_path)
    if pr.scheme != "s3" and pr.scheme != "s3n":
        raise ValueError("Invalid scheme for path: '%s'" % s3_path)

    import boto
    p = settings.Param
    s3_conn = boto.connect_s3(p.AWS_ACCESS_KEY_ID, p.AWS_ACCESS_KEY_SECRET)
    bucket = s3_conn.get_bucket(pr.netloc)

    print("s3_delete %s" % s3_path)
    prefix_path = urlparse(s3_path).path[1:]
    for key in bucket.list(prefix=prefix_path):
        key.delete()
    return True

def s3_set_metadata(s3_path, settings, metadata):
    print("s3_set_metadata : %s" % s3_path)
    from urlparse import urlparse
    pr = urlparse(s3_path)
    if pr.scheme != "s3" and pr.scheme != "s3n":
        raise ValueError("Invalid scheme for path: '%s'" % s3_path)

    import boto
    p = settings.Param
    s3_conn = boto.connect_s3(p.AWS_ACCESS_KEY_ID, p.AWS_ACCESS_KEY_SECRET)
    bucket = s3_conn.get_bucket(pr.netloc)

    prefix_path = urlparse(s3_path).path[1:]
    for key in bucket.list(prefix=prefix_path):
        for meta_key,meta_val in metadata.items():
            # key.set_metadata(meta_key, meta_val)
            key.copy(key.bucket, key.name, preserve_acl=True, metadata=metadata)

def s3_set_acl(s3_path, settings, acl):
    print("s3_set_acl : %s" % s3_path)

    from urlparse import urlparse
    pr = urlparse(s3_path)
    if pr.scheme != "s3" and pr.scheme != "s3n":
        raise ValueError("Invalid scheme for path: '%s'" % s3_path)

    import boto
    p = settings.Param
    s3_conn = boto.connect_s3(p.AWS_ACCESS_KEY_ID, p.AWS_ACCESS_KEY_SECRET)
    bucket = s3_conn.get_bucket(pr.netloc)

    prefix_path = urlparse(s3_path).path[1:]
    for key in bucket.list(prefix=prefix_path):
        for acl_key,acl_val in acl.items():
            if acl_val:
                key.set_acl(acl_key, acl_val)
            else:
                key.set_acl(acl_key)

def s3_make_list(s3_path, settings):
    print("s3_make_list : %s" % s3_path)

    from urlparse import urlparse
    pr = urlparse(s3_path)
    print(pr)
    if pr.scheme != "s3" and pr.scheme != "s3n":
        raise ValueError("Invalid scheme for path: '%s'" % s3_path)

    import boto
    p = settings.Param
    s3_conn = boto.connect_s3(p.AWS_ACCESS_KEY_ID, p.AWS_ACCESS_KEY_SECRET)
    bucket = s3_conn.get_bucket(pr.netloc)

    cnt = StringIO()
    cnt.write("<html><head></head><body>")
    prefix_path = urlparse(s3_path).path[1:]
    if prefix_path[-1] != "/":
        prefix_path += "/"
    for key in bucket.list(prefix=prefix_path):
        key_url = "https://s3.amazonaws.com/%s/%s" % (pr.netloc, key.name)
        cnt.write('<a href="%s">%s</a><br />' % (key_url, key.name))
    cnt.write("</body></html>")

    # upload
    k = boto.s3.key.Key(bucket)
    k.key = os.path.join(prefix_path, "list.html")
    k.set_metadata("Content-Type", "text/html")
    k.set_contents_from_string(cnt.getvalue())

    return "https://s3.amazonaws.com/%s/%s" % (pr.netloc, k.name)

def main():
    hr = HadoopRuntime("spec.json")
    settings = hr.settings
    print(settings)

    s3_path = settings.Input.s3_path.val
    content_type = settings.Param.Metadata_Type

    s3_set_metadata(s3_path, settings, {"Content-Type" : content_type})
    list_html_link = s3_make_list(s3_path, settings)
    s3_set_acl(s3_path, settings, {"public-read" : None})

    settings.Output.list_html.val = list_html_link

    print("Done")

if __name__ == "__main__":
    main()
