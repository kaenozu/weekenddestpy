import logging
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from driving.forms import SrcForm
from driving.models import Dest, Src, geoCash, routeCash
from geopy.distance import geodesic
import random

from driving.utils.geo import Geo
from driving.utils.route import Route
from driving.utils.wiki import Wiki

# Create your views here.


@require_http_methods(['GET'])
def driving_index(request):
    """検索画面"""

    params = {
        'form': SrcForm(request.GET or None),
    }

    if "src" in request.GET and "distance" in request.GET:
        # 出発地が設定されている場合
        srcParam = request.GET.get("src")
        distanceParam = int(request.GET.get("distance"))
        src = []
        # 検索したことがある場所ならcashから取得

        geocash = geoCash.objects.filter(src=srcParam).first()
        if geocash is not None:
            src.append(geocash.latitude)
            src.append(geocash.longitude)
        else:
            geo = Geo().getGeo(srcParam)
            src.append(str(geo["result"]["latitude"]))
            src.append(str(geo["result"]["longitude"]))
            geoCash.objects.create(
                src=srcParam, latitude=geo["result"]["latitude"], longitude=geo["result"]["longitude"])

        randomDest = []
        for d in Dest.objects.all():
            dis = geodesic((float(src[0]), float(src[1])),
                           (float(d.latitude), float(d.longitude))).km
            if dis <= 50:
                randomDest.append(d)

        # ランダムに１つ選ぶ
        choiced = random.choice(randomDest)

        routecashmodel = routeCash.objects.filter(
            src=src[0] + "," + src[1], dest=choiced.latitude + "," + choiced.longitude).first()

        if routecashmodel is not None:
            params = dict(
                name=choiced.name, src=src[0]+ "," + src[1], dest=choiced.latitude + "," + choiced.longitude, highway=routecashmodel.highway, localway=routecashmodel.localway)
        else:
            route = Route().getRoute(
                [dict(src=srcParam, dest=choiced.latitude + "," + choiced.longitude, place_name=choiced.name)])
            params = dict(
                name=choiced.name, src=src[0]+ "," + src[1], dest=choiced.latitude + "," + choiced.longitude, highway=route["result"][0]["distance"]["highway"], localway=route["result"][0]["distance"]["localway"])
            routeCash.objects.create(src=src[0] + "," + src[1], dest=choiced.latitude + "," + choiced.longitude,
                                     highway=route["result"][0]["distance"]["highway"], localway=route["result"][0]["distance"]["localway"])

        wikiSumally = Wiki().getWiki(choiced.name)
        
        params["wiki"] = wikiSumally if wikiSumally is not None else ""

        # params = dict(
        #     name=choiced.name, src=src[0]+ "," + src[1], dest=choiced.latitude + "," + choiced.longitude, highway=100, localway=200)

        return render(request,
                      'driving/list.html', params)
    else:
        # それ以外
        return render(request,
                      'driving/index.html', params)
