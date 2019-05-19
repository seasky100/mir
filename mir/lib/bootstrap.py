#!/usr/bin/env python
"""
Application bootstrap functions
"""

from __future__ import absolute_import
import bcrypt
import threading


# -----------------------------------
# Application Bootstrap
# -----------------------------------

def create_admin(app):
    l = threading.Lock()
    l.acquire()
    try:
        with app.app_context():
            sub_resource = app.data.driver.db['accounts']
            admin = sub_resource.find_one({'username': app.config['DEFAULT_ADMIN_USER']})
            if not admin:
                default_admin_account = {
                    'username': app.config['DEFAULT_ADMIN_USER'],
                    'password': bcrypt.hashpw(app.config['DEFAULT_ADMIN_PW'].encode('utf-8'), bcrypt.gensalt()),
                    'roles': [{'role': 'superuser'}],
                    'owner': app.config['DEFAULT_ADMIN_USER'],
                }
                print("Creating default Admin user...")
                app.data.insert('accounts', default_admin_account)
    finally:
        l.release()
