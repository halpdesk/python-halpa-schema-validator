import json
from os import path
from os.path import dirname, join

from jsonschema import Draft7Validator, ErrorTree, FormatChecker, RefResolver
from jsonschema import validate as jsonschema_validate
from jsonschema.exceptions import ErrorTree, SchemaError
from jsonschema.exceptions import _Error as Error

def load_validator(schema):
    """ Validates JSON schema (Draft 7 Validator)
        Raises SchemaError if schema check shows errors in schema
    """
    # Instantiate the Draft 7 Validator with format checker
    validator = Draft7Validator(schema=schema, format_checker=FormatChecker())
    validator.check_schema(schema)
    return validator


def validate(schema, data):
    """ Validates JSON schema (Draft 7 Validator) and tests data (dictionary) against it\n
        Returns True if schema and data is valid, or otherwise a dictionary with well formatted errors
    """

    errors = {}

    # If schema is a file
    try:
        if type(schema) is not dict:
            schema = _load_json_file(schema)
    except FileNotFoundError as file_not_found:
        errors["schema"] = "schema file does not exist"
        return errors

    try:
        validator = load_validator(schema)
    except SchemaError as schema_error:
        errors["schema"] = schema_error.message
        return errors

    # Check that data is a dictionary
    if type(data) is not dict:
        errors["data"] = "data is not a dictionary"
        return errors


    # Check required fields
    try:
        validator.validate(instance=data)
    except Error as validate_errors:
        errors["fields"] = {}
        # if any required field is missing
        if validate_errors.validator == "required":
            # check all fields
            for required in schema["required"]:
                if required not in data:
                    errors["fields"][required] = required + " is required"


    # Build error tree
    tree = ErrorTree(validator.iter_errors(instance=data))
    if tree.total_errors > 0:
        for errorItem in tree:
            for requirementType in tree[errorItem].errors:
                errors["fields"][errorItem] = tree[errorItem].errors[requirementType].message
    if not validator.is_valid(instance=data):
        return errors

    return True

# https://medium.com/grammofy/testing-your-python-api-app-with-json-schema-52677fe73351
# Modified by Halpdesk

def is_valid(schema, data):
    """ Just checks validity. Gives no errors.
        Raises errors if schema can not be loaded
        Returns True if schema is valid, False otherwise
    """

    if type(schema) is not dict:
        schema = _load_json_file(schema)

    try:
        load_validator(schema)
    except SchemaError as schema_error:
        raise ValueError(schema_error.message)

    validation = validate(schema, data)
    return True if validation==True else False

def _load_json_file(filename):
    """ Loads schema from an existing file """

    if not path.exists(filename):
        raise FileNotFoundError(filename + " does not exist")

    with open(filename) as schema_file:
        return json.loads(schema_file.read())
