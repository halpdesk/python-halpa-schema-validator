# Package

This package is a wrapper for jsonschema and simplejson to simplyfy JSON schema validation specified by [JSON Schema Draft 7](https://json-schema.org/specification-links.html#draft-7) (link to [IETF](https://tools.ietf.org/html/draft-handrews-json-schema-01)).

## Example

```python

from validator import validate

# Define the validation schema
schema = {
    "type": "object",
    "required": [
        "name",
        "age",
    ],
    "properties": {
        "name": { "type": "string" },
        "age": { "type": "number" },
    }
}

# Data to be validated
data = {
    "name": "Daniel",
    "age": 30,
}

# Validate and run
validation = validate(schema, data)
if validation==True:
    # do something with data, e.g. create a new friend
else:
    print(validation) # will show a well formated dict with errors
```

> Note: More examples can be shown in the tests

## Contribute

This package is intended to be used by private projects. But go ahead if you like and make comments and pull requests and I might look into it.

### Install the package

```sh
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Run tests

```sh
python -m pytest -m validator -s
```
