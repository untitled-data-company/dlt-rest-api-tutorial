# Demo of dlt's REST API source

[Watch tutorial video playlist](https://www.youtube.com/playlist?list=PLpTgUMBCn15rs2NkB4ise780UxLKImZTh)

In this repo we collect the code created in our data engineering tutorials on the dlt REST API source – the easiest way to create pipelines loading data from REST API sources into various destination systems.

This verified REST API source allows us to develop a source connector using just a Python dictionary. This gives us the maximum flexibility of Python becasue we're not restricted to JSON or YAML. At the same time, the code is very easy to read and write.

These video tutorials cover topics, such as:
1. [Basic Walkthrough: Configure Endpoints with parent-child relationship](https://youtu.be/OSSSgWrrnyY)
2. [Authentication: Bearer Token and HTTP Basic Auth](https://youtu.be/VqEghIg1cWI?)
3. [Incremental Loading](https://youtu.be/2AUqv0ojwm0)


# Video 1: Basic Walkthrough
We cover in [pokemon_pipeline.py](pokemon_pipeline.py):
1. Import endpoints
2. Adding custom query parameters
3. Specify parent-child relationship between endpoints `/berry/{berry_name}`
4. Install dlt and rest_api source
5. Inspect loaded data

[Video](https://youtu.be/OSSSgWrrnyY)

## Installation
```shell
poetry install
dlt init rest_api duckdb
```

## Run
```shell
python pokemon_pipeline.py
```

## Inspect Data
Using streamlit app with GUI in web browser:
```shell
dlt pipeline pokemon_pipeline show
```

Alternatively, using duckdb CLI:
```shell
duckdb pokemon_pipeline.duckdb
```

```sql
use pokemon;
select
  berry_details.name,
  berry_details.size,
  berry_details__flavors.flavor__name,
  berry_details__flavors.potency
from berry_details
join berry_details__flavors on berry_details._dlt_id = berry_details__flavors._dlt_parent_id;
```
# Video 2: Authentication
We cover:
1. simple bearer token authentication in [github_pipeline.py](github_pipeline.py)
2. more complex HTTP Basic authentication in [freshdesk_pipeline.py](freshdesk_pipeline.py)

We add the secrets into the hidden `.dlt/secrets.toml`. For production use cases, we recommend using environment variables provided by a secrets manager.

[More infos on dlt secrets and configs](https://dlthub.com/docs/general-usage/credentials/configuration)

[Video](https://youtu.be/VqEghIg1cWI?)

# Video 3: Incremental Loading
We load github issues incrementally in [github_pipeline.py](github_pipeline.py).

As explained in the video, if you want to load a resource incrementally which was previously loaded with the `write_disposition=(append, replace)` we need to [reset the pipeline state](https://dlthub.com/docs/general-usage/state#reset-the-pipeline-state-full-or-partial). You can use:
```shell
dlt pipeline github_pipeline drop issues
```
This avoids dlt from attempting to apply an `ALTER TABLE` statement adding a constraint on the `ID` field which duckdb does not support at the moment (v0.9.2).

[Video](https://youtu.be/2AUqv0ojwm0)

# Tutorial 4: Custom Authentication
In [zoom.py](zoom.py), we implement a connector to the Zoom API to load meeting and webinar information.
We implemented the specific OAuth 2.0 implementation for Zoom.
Also, we implemented response actions, such as ignoring certain error messages or HTTP status codes.

See tutorial blog post here: [How To Create A dlt Source With A Custom Authentication Method](https://untitleddata.company/blog/How-to-create-a-dlt-source-with-a-custom-authentication-method-rest-api-vs-airbyte-low-code)
