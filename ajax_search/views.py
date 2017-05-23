import datetime

import simplejson
from ajax_search.forms import SearchForm
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext


def xhr_search(request):
    num = settings.AJAX_SEARCH_LIMIT
    c = settings.AJAX_SEARCH_HELPER
    parts = c.split('.')
    m = __import__(parts[0])
    for comp in parts[1:]:
        m = getattr(m, comp)

    req = {}
    if request.is_ajax():
        query = request.POST['query']

        words = query.split()
        count = len(words)

        model_list = m(count, query)

        req['name'] = ''
        for e in model_list[0:num]:
            req['name'] += """<div class="searchdropdowndiv"><a href='"""
            req['name'] += e.get_absolute_url()
            req['name'] += """' style="text-decoration:none;"><p style="font-size:14px; color:#000000;">"""
            req['name'] += e
            req['name'] += """</p></a></div>"""
        if model_list.count() > num:
            req[
                'name'] += """<div class="searchdropdowndiv" style="border-top:1px solid #e8e8e8;"><a href='ajax_search/search/?q="""
            req['name'] += query
            req[
                'name'] += """' style="text-decoration:none;"><p style="font-size:14px; color:#a2a2a2;">See all results</p></a></div>"""



        #					user_list = user_list | User.objects.filter(Q(penname__icontains=query1) | Q(first_name__icontains=query1) | Q(last_name__icontains=query1))
        #			user_list.distinct().order_by('-numfollowers')

    else:
        req['name'] = ""
    response = simplejson.dumps(req)
    return HttpResponse(response, mimetype="application/json")


def search(request):
    c = settings.AJAX_SEARCH_HELPER
    parts = c.split('.')
    m = __import__(parts[0])
    for comp in parts[1:]:
        m = getattr(m, comp)

    template_name = settings.SEARCH_RESULT_TEMPLATE
    c = RequestContext(request)

    if 'q' in request.GET:
        query = request.GET['q']
        if query == "":
            return render_to_response(template_name,
                                      {'searchform': SearchForm(), 'query': query, 'timenow': datetime.datetime.now()},
                                      c)

        words = query.split()
        count = len(words)
        model_list = m(count, query)
        return render_to_response(template_name, {'searchform': SearchForm(), 'query': query, 'items_list': model_list,
                                                  'timenow': datetime.datetime.now()}, c)
    else:
        return render_to_response(template_name, {'searchform': SearchForm()})
