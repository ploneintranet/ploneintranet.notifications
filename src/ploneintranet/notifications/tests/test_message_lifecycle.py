# -*- coding: utf-8 -*-

from ploneintranet.notifications.adapters import fake_adapter
from ploneintranet.notifications.interfaces import INotificationsTool
from ploneintranet.notifications.message import create_message
from ploneintranet.notifications.testing import \
    PLONEINTRANET_NOTIFICATIONS_INTEGRATION_TESTING
from zope.component import queryUtility
import unittest2 as unittest


class TestMessageLifecycle(unittest.TestCase):

    layer = PLONEINTRANET_NOTIFICATIONS_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_create_msgs_mark_as_read_delete(self):
        tool = queryUtility(INotificationsTool)

        predicate = 'page_deleted'

        # Step 1, something creates a bunch of messages
        for user in 'test1', 'test2', 'test3', 'test4', 'test5':
            actor = dict(fullname='John Doe', userid='johndoe',
                         email='join@test.com')
            obj = {'id': self.portal.id,
                   'url': self.portal.absolute_url(relative=True),
                   'title': 'I deleted the front page'}
            msg = create_message([actor], predicate, obj)
            user_queue = tool.get_user_queue(user)

            # This should be an adapter
            fake_adapter(user_queue, predicate).add(msg)

        # Step 2, test1 sees his message
        queue = tool.get_user_queue('test1')
        first_msg = queue[0]
        handler = fake_adapter(queue, predicate)
        handler.mark_as_read(first_msg)

        # Step 3, the regular clean up tasks from somewhere
        # cleans up queues

        handler = fake_adapter(queue, predicate)
        handler.cleanup()

        # Step 4, somebody else reads his messages

        queue = tool.get_user_queue('test2')
        first_msg = queue[0]
        handler = fake_adapter(queue, predicate)
        handler.mark_as_read(first_msg)

        # Final result

        self.assertEqual(0, len(tool.get_user_queue('test1')))
        self.assertEqual(1, len(tool.get_user_queue('test2')))
        self.assertEqual(1, len(tool.get_user_queue('test3')))
        self.assertEqual(1, len(tool.get_user_queue('test4')))
        self.assertEqual(1, len(tool.get_user_queue('test5')))
