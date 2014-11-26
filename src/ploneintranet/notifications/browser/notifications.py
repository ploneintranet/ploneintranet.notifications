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
        channel = AllChannel(user)
        display_message = channel.get_unread_messages()
        return display_message
