# ReAct Agents in Different Frameworks

This repository contains the implementation of the ReAct agent in different
frameworks. The goal is to compare and contrast the different implementations.

## Pydantic AI

It's possible to implement a ReAct agent using pydantic AI. The implementation
is in the `pydantic_ai_react.pydantic_ai_test` module. The agent thinks using
an argument of the function call, `thought`, that should be put together with
every agent tool.

In this module, it is implemented the decorator `@react_agent` that can be used
to decorate the tools of the ReAct agent. 

Run a test with
```bash
uv run -m pydantic_ai_react.pydantic_ai_test
```

## LiteLLM

To do

## Atomic Agent

To do

## Crew AI

Implementing a ReAct agent in Crew AI is straightforward, since it is already
there. A test implementation is in the `crew_ai_react.crew_ai_test` module.

To run it:
```bash
uv run -m crew_ai_react.crew_ai_test
```
