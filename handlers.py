import kopf
import asyncio

from kubernetes import client
from base64 import b64decode
from ruamel import yaml

from kinto_http import Client
from concurrent.futures import ThreadPoolExecutor
from kinto_wizard.async_kinto import AsyncKintoClient
from kinto_wizard.yaml2kinto import initialize_server


def get_kinto_client(server_url, auth):
    return Client(
        server_url=server_url,
        auth=auth,
    )


@kopf.on.create('codeformuenster.org', 'v1', 'kinto-objects')
def create_fn(spec, namespace, **kwargs):
    # TODO validate spec
    kinto_auth_secret = spec['authSecret']['name']
    kinto_objects_config_map = spec['objects']['configMap']['name']
    kinto_server_url = spec['server']

    api = client.CoreV1Api()

    secret_response = api.read_namespaced_secret(kinto_auth_secret, namespace)
    config_map_response = api.read_namespaced_config_map(
        kinto_objects_config_map, namespace)

    kinto_auth_b64 = secret_response.data['auth']
    kinto_auth = b64decode(kinto_auth_b64)
    kinto_auth = auth = tuple(kinto_auth.decode('utf-8').split(":", 1))

    kinto_objects = config_map_response.data['objects']

    kinto_client = get_kinto_client(kinto_server_url, kinto_auth)

    thread_pool = ThreadPoolExecutor()
    # event_loop = asyncio.get_event_loop()
    event_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(event_loop)
    async_client = AsyncKintoClient(kinto_client, event_loop, thread_pool)

    config = yaml.safe_load(kinto_objects)
    event_loop.run_until_complete(
        initialize_server(
            async_client,
            config,
        )
    )

    print('done')
