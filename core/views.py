#coding: utf-8

from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from core.models import FBUser
from jsonview.decorators import json_view
import requests
import json

import logging
logger = logging.getLogger(__name__)

@csrf_exempt
def person_add_n_list(request):
    if request.method == 'POST':
        fbid = request.POST['facebookId']
        url = settings.FB_GRAPH_URL % (fbid, settings.APP_ID, settings.APP_SECRET)
        req = requests.get(url).json()
        if 'error' in req.keys():
            logger.error(u'FB id invalid!')
            return HttpResponse(u'id de usuário inválido', status=404)
        name = req['name']
        id = req['id']
        fbuser = FBUser(name=name, fbid=id)
        fbuser.save()
        logger.info(u'FBUser=%s added with success' % fbid)
        return HttpResponse(status=201)

    fbusers = FBUser.objects.all()
    limit = request.GET.get('limit', None)
    if limit:
        fbusers = fbusers[:limit]
    fbusers_data = [{'id': fbuser.id, 'name': fbuser.name} for fbuser in fbusers]
    logger.info(u'Showing the users')
    return HttpResponse(json.dumps(fbusers_data))


@csrf_exempt
@json_view
def person_detail_n_delete(request, fbid):
    fbuser = get_object_or_404(FBUser, fbid=fbid)
    if request.method == 'DELETE':
        fbuser.delete()
        logger.info(u'Deleting the FBUser=%s' % fbid)
        return HttpResponse(status=204)
    fbuser_data = {'fbid': fbuser.fbid, 'name': fbuser.name}
    logger.info(u'Showing the details of fbuser=%s' % fbuser.fbid)
    return HttpResponse(json.dumps(fbuser_data))