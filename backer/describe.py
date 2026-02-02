import yaml


def defaults(cls):
    desc = describe(cls)
    return {k: v["default"] for k, v in desc.items()}


def describe(cls, desc=None):
    desc = desc or {}

    try:
        fields = cls.__dataclass_fields__
    except AttributeError:
        return desc

    hidden = getattr(cls, "_HIDDEN_FIELDS", ())
    fields = {k: v for k, v in fields.items() if k not in hidden}

    docs = getattr(cls, "__dataclass_docs__", {})
    if isinstance(docs, str):
        docs = yaml.safe_load(docs)

    for base in cls.__bases__:
        describe(base, desc)

    for name, field in fields.items():
        desc[name] = {
            "name": name,
            "type": field.type.__name__,
            "default": field.default,
            "doc": docs.get(name, ""),
        }

    return desc
