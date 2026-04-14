def create_cache_key(prefix: str, **kwargs) -> str:
    result = [prefix]
    for key, value in kwargs.items():
        result.append(f"{key}:{value}")
    return ":".join(result)
