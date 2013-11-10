#!/usr/bin/env python

import pytest

errcode = pytest.main("--cov rec_env --cov-report xml --cov-report term-missing --junitxml=tests.xml")
raise SystemExit(errcode)
