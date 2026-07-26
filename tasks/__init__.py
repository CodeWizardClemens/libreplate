from invoke import Collection

from . import db, dev, maintenance, setup

ns = Collection()

ns.add_collection(Collection.from_module(setup))
ns.add_collection(Collection.from_module(dev))
ns.add_collection(Collection.from_module(db))
ns.add_collection(Collection.from_module(maintenance))
