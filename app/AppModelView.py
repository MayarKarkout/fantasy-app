from flask import url_for, request
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from werkzeug.utils import redirect


class AppModelView(ModelView):
    page_size = 50  # the number of entries to display on the list view

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))