import dlt

from rest_api import RESTAPIConfig, rest_api_source
from rest_api.auth import HttpBasicAuth

basic_auth = HttpBasicAuth(dlt.secrets['sources.freshdesk.token'], "")

config: RESTAPIConfig = {
  "client": {
    "base_url": "https://untitleddatacompany.freshdesk.com/api/v2/",
    "auth": basic_auth
  },
  "resources": [ "tickets" ]
}

freshdesk_source = rest_api_source(config)

pipeline = dlt.pipeline(
    pipeline_name="freshdesk_pipeline",
    destination="duckdb",
    dataset_name="freshdesk",
)

load_info = pipeline.run(freshdesk_source)
print(load_info)
