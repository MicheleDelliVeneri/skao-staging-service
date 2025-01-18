#!/bin/bash
# build_docs.sh

sphinx-apidoc -o docs/source/ app/
cd docs
make html