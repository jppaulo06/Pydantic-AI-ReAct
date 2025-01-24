from typing import Any, Callable, Optional
import inspect
import functools
import docstring_parser
from docstring_parser import DocstringParam


def react_tool(thought_callback: Optional[Callable[[str], Any]] = None):
    """
    Decorator to define a ReAct tool function.

    Args:
        thought_callback: A callback function to handle the thought parameter.
    """

    _THOUGHT_PARAM_NAME = "_thought"
    _THOUGHT_PARAM_DESCRIPTION = (
        "Your detailed reasoning about what to do next. Think step-by-step."
    )

    def react_decorator(func: Callable[..., Any]):
        original_signature = inspect.signature(func)
        original_docstring = docstring_parser.parse(func.__doc__ or "")
        original_annotations = func.__annotations__

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            thought = kwargs.pop(_THOUGHT_PARAM_NAME, None)
            if thought_callback:
                thought_callback(thought)
            bound = original_signature.bind(*args, **kwargs)
            bound.apply_defaults()
            return func(*bound.args, **bound.kwargs)

        def _overwrite_docstring():
            for param in original_docstring.params:
                if param.arg_name == _THOUGHT_PARAM_NAME:
                    raise ValueError(
                        f"Parameter name '{_THOUGHT_PARAM_NAME}' is reserved by ReAct wrapper. Please use a different parameter name."
                    )
            thought_param = DocstringParam(
                args=["param"],
                description=_THOUGHT_PARAM_DESCRIPTION,
                arg_name=_THOUGHT_PARAM_NAME,
                type_name="str",
                is_optional=None,
                default=None,
            )
            new_docstring = original_docstring
            new_docstring.meta = [thought_param, *new_docstring.meta]
            wrapper.__doc__ = docstring_parser.compose(new_docstring)

        def _overwrite_signature():
            thought_sig_param = inspect.Parameter(
                name=_THOUGHT_PARAM_NAME,
                kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
                annotation=str,
            )
            new_sig_params = [
                thought_sig_param,
                *original_signature.parameters.values(),
            ]
            new_sig = inspect.Signature(
                parameters=new_sig_params,
                return_annotation=original_signature.return_annotation,
            )
            wrapper.__signature__ = new_sig  # type: ignore

        def _overwrite_annotations():
            new_annotations = original_annotations
            new_annotations[_THOUGHT_PARAM_NAME] = str
            wrapper.__annotations__ = new_annotations

        _overwrite_docstring()
        _overwrite_signature()
        _overwrite_annotations()

        return wrapper

    return react_decorator


REACT_BASE_PROMPT = """You are a Helpful AI Assistant.

You have been asked to assist with a general purpose query.

Your goal is to reason about the query and decide on the best course of action to answer it accurately.

Instructions:
1. Analyze the query, previous reasoning steps, and observations.
2. Decide on the next action: think about what to do next, use the correct tool, or provide a final answer.
3. Always think before acting.

Remember:
- Be thorough in your reasoning.
- Use tools when you need more information.
- Always base your reasoning on the actual observations from tool use.
- If a tool returns no results or fails, acknowledge this and consider using a different tool or approach.
- Provide a final answer only when you're confident you have sufficient information.
- If you cannot find the necessary information after using available tools, admit that you don't have enough information to answer the query confidently.
"""
