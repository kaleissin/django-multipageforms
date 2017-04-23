from __future__ import unicode_literals

import json

from django.http import QueryDict
from django.utils.datastructures import MultiValueDict

SERIALIZE_INDENT = 1

def strip_csrftoken(data):
    if 'csrfmiddlewaretoken' in data:
        data.pop('csrfmiddlewaretoken')
    return data

def fill_form(data, Form):
    """Makes a form filled with <data> out of <Form>

    The data needs to be a dict of lists or a MultiValueDict
    """
    qdata = QueryDict('', mutable=True)
    qdata.update(data)
    form = Form(data=qdata)
    form.is_valid()
    return form

def serialize(simple_object):
    adict = simple_object
    # Naively converting a MultiValueDict() to dict() loses information
    if isinstance(simple_object, MultiValueDict):
        adict = {}
        for key in simple_object:
            adict[key] = simple_object.getlist(key)
    return json.dumps(adict, indent=SERIALIZE_INDENT)

def unserialize(serialized_object):
    try:
        u'' + serialized_object
    except TypeError:  # `serialized_object` is not a string
        raise TypeError('The parameter given must be a string')
    unserialized = json.loads(serialized_object)
    out = MultiValueDict()
    # Naively converting a dict() to MultiValueDict() loses information
    for key, value in unserialized.items():
        out.setlist(key, value)
    return out

def update_multivaluedict(old, new):
    """Use instead of MultiValueDict.update()

    MultiValueDict.update() appends instead of overwrites, so a helper function
    is needed if overwrite is what you want.
    """
    if not old:
        return new
    if not new:
        return old
    out = MultiValueDict()
    new = new.copy()
    for key, value in old.lists():
        if not key in new:
            out.setlist(key, value)
            continue
        newvalue = new.getlist(key)
        if newvalue == value:
            out.setlist(key, value)
            new.pop(key)
            continue
        out.setlist(key, newvalue)
    for key, value in new.lists():
        out.setlist(key, value)
    return out
