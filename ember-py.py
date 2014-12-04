# -*- coding: utf-8 -*-
"""
ember.js playground, using python backend (flask based)
"""
import flask
import api
import helper

app = flask.Flask('ember-py')
app.after_request(helper.disable_browser_caching)

helper.setup_static_handlers(app)
helper.register_endpoint(app, api.Contact)

if __name__ == '__main__':
    app.run(debug=True)
