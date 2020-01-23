from validator import is_valid, validate as base_validate

def validate(schema, data):
    def decorator(f):
        def validate_f(*args, **kwargs):
            return base_validate(schema, data)
        return validate_f
    return decorator
