import dlt

import rest_api.typing
from rest_api import rest_api_source

config: rest_api.typing.RESTAPIConfig = {
    "client": {
        "base_url": "https://api.github.com/repos/dlt-hub/verified-sources",
        "auth": {"token": dlt.secrets["sources.github.token"]},
    },
    "resources": [
        {
            "name": "issues",
            "endpoint": {
                "params": {
                    "creator": "@me",
                }
            },
        }
    ],
}

source = rest_api_source(config)

pipeline = dlt.pipeline(
    pipeline_name="github_pipeline",
    destination="duckdb",
    dataset_name="github",
    progress="log",
)

load_info = pipeline.run(source)
print(load_info)
