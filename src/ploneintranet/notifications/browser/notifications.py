# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from plone import api
from plone.memoize.view import memoize
from ploneintranet.notifications.channel import AllChannel


class NotificationsView(BrowserView):

    @memoize
    def your_notifications(self):
        # count to show unread messages
        display_message = []
        user = api.user.get_current()
        # TODO a zope user like admin will fail from here
        try:
            channel = AllChannel(user)
            display_message = channel.get_unread_messages()
        except AttributeError:
            #AttributeError: getUserId
            display_message = []
        return display_message
