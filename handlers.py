import kopf

@kopf.on.create('codeformuenster.org', 'v1', 'kinto-objects')
def create_fn(spec, meta, status, **kwargs):
    print(f"And here we are! Creating: {spec}")
