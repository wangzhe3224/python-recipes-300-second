import requests
from starlette.requests import Request
from typing import Any, Dict

from ray import serve


@serve.deployment(route_prefix='/')
class MyModelDeployment:
    def __init__(self, msg) -> None:
        self._msg = msg

    def __call__(self, request: Request) -> Any:
        return {"result": self._msg}

        
app = MyModelDeployment.bind(msg="Hi Zhe")

serve.run(app)

print(requests.get("http://127.0.0.1:8000/").json())