from .parse import parse as _parse, parse_blueprint as _parse_blueprint, Embed, EmbedBlueprint


_cache = {}
_name_cache = {}

_blueprint_name_cache = {}
_blueprint_cache = {}
cache_enabled = True


def disable_caching():
    global cache_enabled
    cache_enabled = False


def load_embed(name: str) -> dict:
    try:
        return _name_cache[name]
    except KeyError:
        raise ValueError(f"Embed \"{name}\" is not loaded")


def load_blueprint(name: str) -> EmbedBlueprint:
    try:
        return _blueprint_name_cache[name]
    except KeyError:
        raise ValueError(f"Embed \"{name}\" is not loaded")


def parse(filename: str) -> dict:
    if not cache_enabled:
        return _parse(filename).to_json()
    if filename not in _cache.keys():
        out = _parse(filename)
        json = out.to_json()
        if out.name:
            _name_cache[out.name] = json
        _cache[filename] = json
    return _cache[filename]


def parse_blueprint(filename: str):
    if not cache_enabled:
        return _parse_blueprint(filename)
    if filename not in _blueprint_cache.keys():
        out = _parse_blueprint(filename)
        if out.name:
            _blueprint_name_cache[out.name] = out
        _blueprint_cache[filename] = out
    return _blueprint_cache[filename]
