#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datacanvas import DatacanvasRuntime
import db
import sys
import requests
import tempfile


db_types = { "PostgreSQL": "postgres", "MySQL": "mysql", "SQLite": "sqlite" }


def db_query(db_meta, query):
    mydb = db.DB(dbtype=db_types.get(db_meta['type']),
                    hostname=db_meta['host'],
                    username=db_meta['user'],
                    password=db_meta['password'],
                    port=int(db_meta['port']),
                    dbname=db_meta['database'])
    df = mydb.query(query)
    return df


def db_query_local(db_meta, query):
    with tempfile.NamedTemporaryFile(delete=False) as f:
        r = requests.get(db_meta['path'])
        f.write(r.content)
        f.close()

        mydb = db.DB(dbtype="sqlite", filename=f.name)
        df = mydb.query(query)
        if not f.delete:
            f.unlink(f.name)
        return df


def main():
    rt = DatacanvasRuntime()
    settings = rt.settings
    print(settings)

    # TODO: Add your code here
    ds = settings.Input.DB.as_datasource()
    db_meta = ds['Meta']
    if ds['Type'] not in ['DB']:
        print "Can only handle datasource 'DB'"
        sys.exit(-1)

    if db_meta['type'] not in db_types:
        print "Do not support DB Types: '%s'" % db_meta['type']
        print "Now, only support database types: '%s'" % db_types.keys()
        sys.exit(-2)

    if db_meta['type'] in ["PostgreSQL", "MySQL"]:
        df = db_query(db_meta, settings.Param.query)
    elif db_meta['type'] in ["SQLite"]:
        df = db_query_local(db_meta, settings.Param.query)
    else:
        pass
    df.to_csv(settings.Output.O)

    print("Done")

if __name__ == "__main__":
    main()
