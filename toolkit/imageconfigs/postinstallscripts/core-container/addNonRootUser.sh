#!/bin/bash

# Add nonroot user
groupadd --system --gid=65532 nonroot
adduser --uid 65532 --gid nonroot --shell /bin/false --no-create-home --system nonroot
