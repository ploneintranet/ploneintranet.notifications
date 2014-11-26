# -*- coding: utf-8 -*-
from ..message import create_message
from plone import api


def added(obj, event):
    ''' What to do when a status update is added to its container
    '''
    member = api.user.get(username=obj.creator)
    actors = dict(
        fullname=member.getProperty('fullname'),
        userid=member.getId(),
        email=member.getProperty('email')
    )
    predicate = 'StatusUpdate'
    obj_dict = obj.__dict__
    if 'title' not in obj_dict:
        obj_dict['title'] = obj_dict.get('text', u'Status update')
    message = create_message(actors, predicate, obj_dict)

    pin = api.portal.get_tool('ploneintranet_notifications')
    for user in api.user.get_users():
        queue = pin.get_user_queue(user)
        queue.append(message)
