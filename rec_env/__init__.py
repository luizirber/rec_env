#!/usr/bin/env python

from __future__ import print_function, division
import re

import yaml


class NoEnvironmentSetException(Exception):
    pass


def load_configuration(yaml_string, kw=None):
    environ = yaml.safe_load(yaml_string)
    environ = _expand_config_vars(environ, updates=kw)

    if environ is None:
        raise NoEnvironmentSetException

    return environ


def _rec_replace(env, value):
    finder = re.compile('\[\{(\w*)\}\]')
    ret_value = value

    try:
        keys = finder.findall(value)
    except TypeError:
        return value

    for k in keys:
        ret_value = _rec_replace(env, ret_value.replace("{%s}" % k, env[k]))

    return ret_value.format(**env)


def _env_replace(old_env, ref=None):
    new_env = {}
    for k in old_env:
        try:
            # tests if value is a string
            old_env[k].split(' ')
        except AttributeError:
            # if it's not a string, let's test if it is a dict
            try:
                old_env[k].keys()
            except AttributeError:
                # if it's not, just set new_env with it
                new_env[k] = old_env[k]
            else:
                # Yup, a dict. Need to replace recursively too.
                all_data = dict(old_env)
                if ref:
                    all_data.update(ref)
                new_env[k] = _env_replace(old_env[k], all_data)
        else:
            # if it is, check if we can substitute for booleans
            if old_env[k].lower() == 'false':
                new_env[k] = False
            elif old_env[k].lower() == 'true':
                new_env[k] = True
            else:
                # else start replacing vars
                new_env[k] = _rec_replace(ref if ref else old_env,
                                         old_env[k])
    return new_env


def _expand_config_vars(d, updates=None):

    if updates:
        d.update(updates)
    new_d = _env_replace(d)

    return new_d
