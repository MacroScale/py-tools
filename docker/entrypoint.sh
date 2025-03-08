#!/bin/bash

uv run -m src.app &
nginx -g 'daemon off;'
