from invoke import Collection

from . import db, dev, docs, maintenance, setup

ns = Collection()

ns.add_collection(Collection.from_module(db))
ns.add_collection(Collection.from_module(dev))
ns.add_collection(Collection.from_module(docs))
ns.add_collection(Collection.from_module(maintenance))
ns.add_collection(Collection.from_module(setup))
