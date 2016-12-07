__author__ = 'NovikovII'

import pytest
import json
import os.path
import importlib
import jsonpickle
from fixture.application import Application

fixture = None
target = None

@pytest.fixture
def app(request):
    global fixture
    global target
    browser = request.config.getoption("--browser")
    if target is None:
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), request.config.getoption("--target"))
        with open(config_file) as file:
            target = json.load(file)

    if fixture is None or not fixture.is_valid():
        fixture = Application(browser=browser, base_url=target['baseUrl'])
    fixture.session.ensure_login(username=target['user'], password=target['pass'])
    return fixture


@pytest.fixture(scope="session", autouse=True)
def stop(request):
    def fin():
        fixture.session.ensure_logout()
        fixture.destroy()
    request.addfinalizer(fin)
    return fixture

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="firefox")
    parser.addoption("--target", action="store", default="target.json")

def pytest_generate_tests(metafunc):
    for fixture in metafunc.fixturenames:
        if fixture.startswith("data_"):
            testdata = load_from_module(fixture[5:])
            metafunc.parametrize(fixture, testdata, ids=[str(x) for x in testdata])
        elif fixture.startswith("json_"):
            testdata = load_from_json(fixture[5:])
            metafunc.parametrize(fixture, testdata, ids=[str(x) for x in testdata])

#загружаются данные из файла data/module.testdata, где testdata - данные уже в файле (может быть constant для data/contacts.py
def load_from_module(module):
    return importlib.import_module("data.%s" % module).constant

#загружаются данные из файла data/module.json
def load_from_json(file):
    testdata_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/%s.json" % file)
    with open(testdata_file) as f:
        return jsonpickle.decode(f.read())
