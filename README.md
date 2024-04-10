# Demo of dlt's REST API source

Watch tutorial video: https://youtu.be/OSSSgWrrnyY

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
