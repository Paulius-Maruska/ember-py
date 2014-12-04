# -*- coding: utf-8 -*-
"""
contact - simple entity for testing purposes
"""
from helper import Entity


class Contact(Entity):
    storage = {}
    last_id = 0
    singular = 'contact'
    plural = 'contacts'
    fields = [
        'nick_name',
        'first_name',
        'last_name',
        'email',
    ]

    @classmethod
    def setup(cls):
        def name_generator():
            first_names = [
                'John', 'Jack', 'Robert', 'Bob', 'Andy', 'George', 'Brian', 'Josh', 'Paul', 'Luke', 'Jessica',
                'Jennifer', 'Jane', 'Carl', 'Carla', 'Emily', 'Lucie', 'Kate', 'James',
            ]
            last_names = [
                'Smith', 'Robertson', 'Fox', 'Cox', 'Santos', 'Prince', 'Reed', 'Clark', 'Allen', 'Morris', 'Williams',
                'Shields',
            ]
            for fn in first_names:
                for ln in last_names:
                    yield fn, ln

        for fn, ln in name_generator():
            content = {
                'nick_name': '%s-%s' % (ln.lower(), fn.lower()),
                'first_name': fn,
                'last_name': ln,
                'email': '%s.%s@email.zz' % (ln.lower(), fn.lower()),
            }
            cls.create(cls.next_id(), content)
