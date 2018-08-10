#!/usr/bin/env bash

source .env/bin/activate
make deps
make run-tagger
