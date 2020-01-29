"""CS201Daemon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls.static import static

from .codesite import view_codesite, view_tracker, view_grades, login_page, logout_page, settings_page, code_submit, submit_ticket

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', view_codesite),
    path('tracker', view_tracker),
    path('grades', view_grades),
    path('accounts/login/', login_page),
    path('logout', logout_page),
    path('settings', settings_page),
    re_path('code-submit', code_submit),
    path('submit-ticket', submit_ticket),
]
