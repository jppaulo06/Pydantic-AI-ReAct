# ReAct Agents in Different Frameworks

This repository contains the implementation of the ReAct agent in different
frameworks. The goal is to compare and contrast the different implementations.

## Pydantic AI

It's possible to implement a ReAct agent using pydantic AI. However, it may
come with some drawbacks using the presented approach. The main issue is that
it's necessary 2 requests to get a step (think + act). This may lead to more
delay, as well as more input tokens used.

## LiteLLM

To do

## Atomic Agent

To do

## Crew AI

Builtin - the most easy one
