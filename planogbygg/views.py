# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.shortcuts import render_to_response, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

from models import *
import etatparser

import re

def viewMap(request):
    pattern = re.compile("(.*?)([0-9]+)")
    cases = Case.objects.all()
    for c in cases:
        m = pattern.search(c.address)
        if m:
            c.address = "%s %s" % (m.group(1), m.group(2))
    return render_to_response(
        "map.html",
        {"cases": cases})


def runParser(request):
    main = etatparser.Main()
    main.main()
    return render_to_response(
        "map.html")