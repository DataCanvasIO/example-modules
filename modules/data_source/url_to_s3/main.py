#!/usr/bin/env python
# -*- coding: utf-8 -*-

from specparser import get_settings_from_file
import os
import sys
import boto
import requests
from StringIO import StringIO

def percent_cb(complete, total):
    sys.stdout.write('.')
    sys.stdout.flush()

def s3_multipart_upload(bucket, url, remote_filename):
    from urlparse import urlparse

    r = requests.get(url, stream=True)

    fn_remote = urlparse(remote_filename).path
    fn_remote_full = remote_filename

    print("Multi-Part upload...")
    print("From : %s" % url)
    print("To   : %s" % fn_remote_full)
    buffer_size = 10 * 1024 * 1024
    mp = bucket.initiate_multipart_upload(fn_remote)
    num_part = 1
    try:
        for buf in r.iter_content(buffer_size):
            if not buf:
                break
            io = StringIO(buf)
            mp.upload_part_from_file(io, num_part, cb=percent_cb, num_cb=1, size=len(buf))
            num_part += 1
            io.close()
    except IOError as e:
        raise e
    mp.complete_upload()
    print("")

    return fn_remote_full

def get_s3_working_dir(settings, s3_bucket, path=""):
    ps = settings
    glb_vars = ps.GlobalParam
    remote_path = os.path.normpath(os.path.join(s3_bucket.name, 'zetjob', glb_vars['userName'], "job%s" % glb_vars['jobId'], "blk%s" % glb_vars['blockId'], path))
    return os.path.join("s3://", remote_path)

def main():
    settings = get_settings_from_file("spec.json")
    print(settings)

    p = settings.Param
    s3_conn = boto.connect_s3(p.AWS_ACCESS_KEY_ID, p.AWS_ACCESS_KEY_SECRET)
    s3_bucket = s3_conn.get_bucket(p.S3_BUCKET)

    remote_filename = get_s3_working_dir(settings, s3_bucket, "OUTPUT_dest_s3")

    remote_path = s3_multipart_upload(s3_bucket, p.SOURCE_URL, remote_filename)
    with open(settings.Output.dest_s3, "w") as f:
        f.write(remote_path)

    print("Done")

if __name__ == "__main__":
    main()
