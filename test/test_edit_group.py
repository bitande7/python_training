__author__ = 'NovikovII'

# -*- coding: utf-8 -*-
from model.group import Group

def test_edit_group(app):
    app.group.edit_first_group(Group(name="editTest", header="editTest", footer="editTest"))
