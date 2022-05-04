# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    "name" : "Email Notification for Activity",
    "version" : "12.0.0.1",
    "category" : "Extra Tools",
    'summary': 'Scheduled Activity Email notification for Scheduled Activity email notify activity management notification for activity notification activity notify activity notification for user activities email notification for employee schedule activities notification',
    "description": """
    
    This odoo app helps user to send email notification for scheduled activity, On edit, done or cancel scheduled activity both create user and assigned user will get email notification.
    
    """,
    "author": "BrowseInfo",
    'website': 'https://www.browseinfo.in',
    "price": 19,
    "currency": 'EUR',
    "depends" : ['base','mail','crm'],
    "data": [
        'views/res_config_settings_view.xml',
        'data/edit_notification_template.xml',
        'data/done_notification_template.xml',
        'data/cancel_notification_template.xml',
    ],
    "auto_install": False,
    "installable": True,
    "live_test_url":'https://youtu.be/5V299TGR5Dw',
    "images":["static/description/Banner.png"],
}

