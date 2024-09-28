import datetime
import json
import logging

import trio
from django.conf import settings as project_settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from item_app.forms import RegistrationForm
from item_app.lib import version_helper
from item_app.lib.version_helper import GatherCommitAndBranchData


log = logging.getLogger(__name__)


# -------------------------------------------------------------------
# main urls
# -------------------------------------------------------------------


def info(request):
    """The "about" view.

    Can get here from 'info' url, and the root-url redirects here.
    """
    log.debug('starting info()')
    # prep data ----------------------------------------------------
    # context = { 'message': 'Hello, world.' }
    context = {
        'quote': ('The best life is the one in which the creative impulses play the '
                  'largest part and the possessive impulses the smallest.'),
        'author': 'Bertrand Russell'}
    # prep response ------------------------------------------------
    if request.GET.get('format', '') == 'json':
        log.debug('building json response')
        resp = HttpResponse(json.dumps(context, sort_keys=True, indent=2),
                            content_type='application/json; charset=utf-8')
    else:
        log.debug('building template response')
        resp = render(request, 'info.html', context)
    return resp


# -------------------------------------------------------------------
# support urls
# -------------------------------------------------------------------


def error_check(request):
    """Offers an easy way to check that admins receive error-emails (in development).

    To view error-emails in runserver-development:
        - run, in another terminal window: `python -m smtpd -n -c DebuggingServer localhost:1026`,
        - (or substitue your own settings for localhost:1026)
    """
    log.debug('starting error_check()')
    log.debug(f'project_settings.DEBUG, ``{project_settings.DEBUG}``')
    if project_settings.DEBUG is True:  # localdev and dev-server; never production
        log.debug('triggering exception')
        raise Exception('Raising intentional exception to check '
                        'email-admins-on-error functionality.')
    else:
        log.debug('returning 404')
        return HttpResponseNotFound('<div>404 / Not Found</div>')


def version(request):
    """Returns basic branch and commit data."""
    log.debug('starting version()')
    rq_now = datetime.datetime.now()
    gatherer = GatherCommitAndBranchData()
    trio.run(gatherer.manage_git_calls)
    info_txt = f'{gatherer.branch} {gatherer.commit}'
    context = version_helper.make_context(request, rq_now, info_txt)
    output = json.dumps(context, sort_keys=True, indent=2)
    log.debug(f'output, ``{output}``')
    return HttpResponse(output, content_type='application/json; charset=utf-8')


def root(request):
    return HttpResponseRedirect(reverse('info_url'))


def register(request):
    """Processes new user registrations."""
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.save()
            password = form.cleaned_data.get('password1')
            # Log the user, so they are ready to go
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request, user)
                return redirect('info_url')
            else:
                # Return an 'invalid login' error message.
                return 'error'
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


@login_required
def home(request):
    """Displays a users home page."""
    context = {
        'items': ['place holder'],
    }
    if request.GET.get('format', '') == 'json':
        resp = HttpResponse(json.dumps(context, sort_keys=True, indent=2),
                            content_type='application/json; charset=utf-8')
    else:
        resp = render(request, 'user_home.html', context)
    return resp
