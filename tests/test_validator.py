import os
from pprint import pprint

import pytest

from validator import is_valid, validate

test_schema = {
    "type": "object",
    "required": ["name", "age", "hired_at"],
    "definitions": {
        "marrigeTypes": {
            "enum": [
                "married",
                "single",
            ]
        },
    },
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "number"},
        "hired_at": {
            "type": "string",
            "format": "date"
        },
        "pattern": {
            "type": "string",
            "format": "regex"
        },
        "readonly": {
            "type": "boolean",
        },
        "married": {
            "anyOf": [{ "$ref": "#definitions/marrigeTypes"}]
        }
    }
}

invalid_schema = {
    "type": "object",
    "required": ["name"],
    "properties": {
        "name": {"type": "sting"},
    }
}

@pytest.mark.validator
def test_validator_valid():
    validation = validate(test_schema, {
        "name": "Daniel",
        "age": 30,
        "hired_at": "1970-01-01",
        "married": "married"
    })
    print(validation)
    assert validation==True

@pytest.mark.validator
def test_validator_missing_required():
    validation = validate(test_schema, {
        "age": 30,
        "hired_at": "1970-01-01",
    })
    print(validation)
    assert validation=={'fields': {'name': 'name is required'}}

@pytest.mark.validator
def test_validator_wrong_type():
    validation = validate(test_schema, {
        "name": "Daniel",
        "age": "thirty",
        "hired_at": "1970-01-01",
    })
    print(validation)
    assert validation=={'fields': {'age': "'thirty' is not of type 'number'"}}

@pytest.mark.validator
def test_validator_missing_required_and_wrong_type():
    validation = validate(test_schema, {
        "age": "thirty",
        "hired_at": "1970-01-01",
    })
    print(validation)
    assert validation=={'fields': {
        'name': 'name is required',
        'age': "'thirty' is not of type 'number'"
    }}

@pytest.mark.validator
def test_validator_wrong_format():
    validation = validate(test_schema, {
        "name": "Daniel",
        "age": 30,
        "hired_at": "last year",
    })
    print(validation)
    assert validation=={'fields': {
        'hired_at': "'last year' is not a 'date'"
    }}

@pytest.mark.validator
def test_validator_wrong_anyof_from_reference():
    validation = validate(test_schema, {
        "name": "Daniel",
        "age": 30,
        "hired_at": "1970-01-01",
        "married": "poly"
    })
    print(validation)
    assert validation=={'fields': {
        'married': "'poly' is not valid under any of the given schemas"
    }}

@pytest.mark.validator
def test_validator_with_file():
    absolute_path = os.path.dirname(os.path.abspath(__file__))
    schema_file = os.path.join(absolute_path, "schemas/test-schema.json")

    validation = validate(schema_file, {
        "name": "Daniel",
        "age": 30,
        "hired_at": "1970-01-01"
    })
    print(validation)
    assert validation==True

@pytest.mark.validator
def test_validator_missing_required_with_file():
    absolute_path = os.path.dirname(os.path.abspath(__file__))
    schema_file = os.path.join(absolute_path, "schemas/test-schema.json")

    validation = validate(schema_file, {
        "age": 30,
        "hired_at": "1970-01-01"
    })
    print(validation)
    assert validation=={'fields': {'name': 'name is required'}}

@pytest.mark.validator
def test_validator_with_non_existing_file():
    absolute_path = os.path.dirname(os.path.abspath(__file__))
    schema_file = os.path.join(absolute_path, "schemas/does-not-exist.json")

    validation = validate(schema_file, {
        "name": "Daniel",
        "age": 30,
        "hired_at": "1970-01-01"
    })
    print(validation)
    assert validation=={'schema': 'schema file does not exist'}

@pytest.mark.validator
def test_validator_with_is_valid():
    validation = is_valid(test_schema, {
        "name": "Daniel",
        "age": 30,
        "hired_at": "1970-01-01",
    })
    print(validation)
    assert validation==True

@pytest.mark.validator
def test_validator_with_is_valid_wrong_format():
    validation = is_valid(test_schema, {
        "name": "Daniel",
        "age": 30,
        "hired_at": "last year",
    })
    print(validation)
    assert validation==False

@pytest.mark.validator
def test_validator_with_is_valid_with_file():
    absolute_path = os.path.dirname(os.path.abspath(__file__))
    schema_file = os.path.join(absolute_path, "schemas/test-schema.json")

    validation = is_valid(schema_file, {
        "name": "Daniel",
        "age": 30,
        "hired_at": "1970-01-01"
    })
    print(validation)
    assert validation==True

@pytest.mark.validator
def test_validator_with_is_valid_missing_required_with_file():
    absolute_path = os.path.dirname(os.path.abspath(__file__))
    schema_file = os.path.join(absolute_path, "schemas/test-schema.json")

    validation = is_valid(schema_file, {
        "age": 30,
        "hired_at": "1970-01-01"
    })
    print(validation)
    assert validation==False


@pytest.mark.validator
def test_validator_with_is_valid_with_non_existing_file():
    absolute_path = os.path.dirname(os.path.abspath(__file__))
    schema_file = os.path.join(absolute_path, "schemas/does-not-exist.json")

    exception_message = ""
    exception_raised = False
    try:
        is_valid(schema_file, {
            "name": "Daniel",
            "age": 30,
            "hired_at": "1970-01-01"
        })
    except FileNotFoundError as file_not_found:
        exception_raised = True
        exception_message = str(file_not_found)[-34:]
    
    assert exception_raised==True
    assert exception_message=="does-not-exist.json does not exist"


@pytest.mark.validator
def test_validator_with_is_valid_with_invalid_schema():
    exception_message = ""
    exception_raised = False
    try:
        is_valid(invalid_schema, {
            "name": "Daniel",
            "age": 30,
            "hired_at": "1970-01-01"
        })
    except ValueError as value_error:
        exception_raised = True
        exception_message = str(value_error)
    
    assert exception_raised==True
    assert exception_message=="'sting' is not valid under any of the given schemas"
