#! /usr/bin/env python

from rec_env import load_configuration


TEST_YAML = '''
carrier: mycarrier
environment: uat
url: "{carrier}.{hosts[{environment}]}"
features:
  contacts: true
  backup: False
hosts:
  production: "{environment}.urlprod.com"
  uat: "{environment}.urltest.net"
  dev: localhost
clients:
  ios:
     provision: "{url}"
'''


def test_recursive_replace():
    env = load_configuration(TEST_YAML)
    assert env['url'] == "mycarrier.uat.urltest.net"


def test_recursive_replace_with_keywords():
    env = load_configuration(TEST_YAML, {'environment': 'dev'})
    assert env['url'] == "mycarrier.localhost"


def test_recursive_replace_boolean_values():
    env = load_configuration(TEST_YAML)
    assert env['features']['contacts'] is True
    assert env['features']['backup'] is False


def test_recursive_replace_nested():
    env = load_configuration(TEST_YAML)
    assert env['clients']['ios']['provision'] == "mycarrier.uat.urltest.net"
