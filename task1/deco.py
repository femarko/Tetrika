from typing import Callable, Dict, Any
from types import FunctionType


def strict(func: FunctionType) -> Callable[..., Any]:
    def wrapper(*args: Any, **kwargs: Any):
        func_annotations: Dict[str, type] = func.__annotations__.copy()  # typing.Dict - for backward compatibility
        func_annotations.pop('return', None)
        param_names: list[str] = list(func_annotations)
        if len(args) > len(param_names):
            raise TypeError(f"Only {len(param_names)} positional arguments are allowed, got {len(args)}.")
        params_with_names: Dict[str, Any] = dict(zip(param_names, args))
        extra_kwargs: set[str] = set(kwargs) & set(params_with_names)
        if extra_kwargs:
            raise TypeError(f"Argument(s) passed both positionally and by keyword: {', '.join(extra_kwargs)}.")
        params_with_names.update(kwargs)
        for param_name, param_type in func_annotations.items():
            if not param_name in params_with_names:
                raise TypeError(f"Missing argument {param_name}.")
            if type(params_with_names[param_name]) != param_type:
                raise TypeError(
                    f"{param_name} must be of type {param_type.__name__}, "
                    f"got {type(params_with_names[param_name]).__name__}."
                )
        return func(*args, **kwargs)
    return wrapper
