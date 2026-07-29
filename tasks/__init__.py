from invoke import Collection

from . import data, dev, docs, manage, setup

ns = Collection()

ns.add_collection(Collection.from_module(data))
ns.add_collection(Collection.from_module(dev))
ns.add_collection(Collection.from_module(docs))
ns.add_collection(Collection.from_module(manage))
ns.add_collection(Collection.from_module(setup))
