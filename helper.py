# -*- coding: utf-8 -*-
"""
Helper classes and functions.
"""
import json

import flask
import flask.views


def disable_browser_caching(response):
    response.headers['Cache-Control'] = 'no-cache, no-store'
    response.headers['Pragma'] = 'no-cache'
    return response


def setup_static_handlers(app):
    @app.route('/')
    def index():
        return app.send_static_file('index.html')

    @app.route('/favicon.ico')
    def favicon():
        return app.send_static_file('favicon.ico')

    @app.route('/s/<path:filename>')
    def static_file(filename):
        return app.send_static_file(filename)


def make_dict(id, obj):
    d = obj.to_dict()
    d.update({'id': id})
    return d


def make_dicts(ids, objects):
    dicts = []
    for id, obj in zip(ids, objects):
        dicts.append(make_dict(id, obj))
    return dicts


class Endpoint(flask.views.MethodView):
    entity_class = None

    def __init__(self, entity_class):
        self.entity_class = entity_class

    def make_response(self, data, meta=None):
        wrapped = {self.entity_class.singular: data}
        if isinstance(data, (list, tuple, set)):
            wrapped = {self.entity_class.plural: data, 'meta': meta}
        serialized = json.dumps(wrapped, indent=4)
        response = flask.make_response(serialized)
        response.headers['Content-Type'] = 'application/json'
        return response

    def get_submitted_dict(self):
        content = flask.request.get_json(cache=False)
        if self.entity_class.singular in content:
            return content[self.entity_class.singular]
        return content

    def get(self, id):
        if id is None:
            offset = int(flask.request.args.get('offset', '0'))
            limit = int(flask.request.args.get('limit', '10'))
            ids, objects = self.entity_class.get(offset, limit)
            meta = {
                'offset': offset,
                'limit': limit,
                'total': self.entity_class.count(),
            }
            return self.make_response(make_dicts(ids, objects), meta=meta)
        else:
            id, obj = self.entity_class.details(id)
            return self.make_response(make_dict(id, obj))

    def post(self):
        content = self.get_submitted_dict()
        id, obj = self.entity_class.create(self.entity_class.next_id(), content)
        return self.make_response(make_dict(id, obj))

    def put(self, id):
        content = self.get_submitted_dict()
        id, obj = self.entity_class.update(id, content)
        return self.make_response(make_dict(id, obj))

    def delete(self, id):
        self.entity_class.delete(id)
        return ''


def register_endpoint(app, entity_class):
    entity_class.setup()
    plural = entity_class.plural
    url = '/api/%s' % plural
    view_func = Endpoint.as_view('%s_api' % plural, entity_class)
    app.add_url_rule(url, view_func=view_func, methods=['GET'], defaults={'id': None})
    app.add_url_rule(url, view_func=view_func, methods=['POST'])
    app.add_url_rule('%s/<int:id>' % url, view_func=view_func, methods=['GET', 'PUT', 'DELETE'])


class Entity(object):
    storage = {}
    last_id = 0
    singular = 'object'
    plural = 'objects'
    fields = []

    def to_dict(self):
        data_dict = {}
        for field in self.fields:
            data_dict[field] = getattr(self, field)
        return data_dict

    def update_from_dict(self, data_dict):
        for key, val in data_dict.items():
            if key in self.fields:
                setattr(self, key, val)

    @classmethod
    def create_from_dict(cls, data_dict):
        obj = cls()
        for field in cls.fields:
            setattr(obj, field, data_dict.get(field))
        return obj

    @classmethod
    def count(cls):
        return len(cls.storage)

    @classmethod
    def get(cls, offset=0, limit=10):
        storage = sorted(cls.storage.items(), key=lambda x: x[0])
        data = storage[offset:offset + limit]
        ids, objs = [], []
        for d in data:
            ids.append(d[0])
            objs.append(d[1])
        return ids, objs

    @classmethod
    def create(cls, id, data_dict):
        obj = cls.create_from_dict(data_dict)
        cls.storage[id] = obj
        return id, obj

    @classmethod
    def details(cls, id):
        return id, cls.storage[id]

    @classmethod
    def update(cls, id, data_dict):
        cls.storage[id].update_from_dict(data_dict)
        return id, cls.storage[id]

    @classmethod
    def delete(cls, id):
        cls.storage.pop(id)

    @classmethod
    def next_id(cls):
        cls.last_id += 1
        return cls.last_id

    @classmethod
    def setup(cls):
        pass
