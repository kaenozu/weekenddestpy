import logging
from unittest import skip
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from driving.forms import SrcForm
from driving.models import Dest, Src, geoCash, routeCash
from geopy.distance import geodesic
import random

from driving.utils.geo import Geo
from driving.utils.route import Route
from driving.utils.wiki import Wiki
from django.contrib import messages

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
            try:
                geo = Geo().getGeo(srcParam)
            except:
                messages.error(request, "場所が特定できません")
                return render(request,
                      'driving/index.html', params)
           
            src.append(str(geo["result"]["latitude"]))
            src.append(str(geo["result"]["longitude"]))
            geoCash.objects.create(
                src=srcParam, latitude=geo["result"]["latitude"], longitude=geo["result"]["longitude"])

        randomDest = []
        for d in Dest.objects.all():
            dis = geodesic((float(src[0]), float(src[1])),
                           (float(d.latitude), float(d.longitude))).km
            if dis <= distanceParam and dis >= distanceParam * 0.9:
                randomDest.append(d)

        if not randomDest:
            # 空ならすべてからランダムにする
            for d in Dest.objects.all():
                randomDest.append(d)
                
        # ランダムに１つ選ぶ
        choiced = random.choice(randomDest)

        routecashmodel = routeCash.objects.filter(
            src=src[0] + "," + src[1], dest=choiced.latitude + "," + choiced.longitude).first()

        if routecashmodel is not None:
            params = dict(
                name=choiced.name, src=src[0] + "," + src[1], dest=choiced.latitude + "," + choiced.longitude, highway=routecashmodel.highway, localway=routecashmodel.localway)
        else:
            try:
                route = Route().getRoute(
                [dict(src=srcParam, dest=choiced.latitude + "," + choiced.longitude, place_name=choiced.name)])
                params = dict(
                name=choiced.name, src=src[0] + "," + src[1], dest=choiced.latitude + "," + choiced.longitude, highway=route["result"][0]["distance"]["highway"], localway=route["result"][0]["distance"]["localway"])
                routeCash.objects.create(src=src[0] + "," + src[1], dest=choiced.latitude + "," + choiced.longitude,
                                     highway=route["result"][0]["distance"]["highway"], localway=route["result"][0]["distance"]["localway"])
            finally:
                # 距離計算のAPIがエラーの場合は何も出さない
                pass
                

        wikiSumally = Wiki().getWiki(choiced.name)

        params["wiki"] = wikiSumally if wikiSumally is not None else ""

        return render(request,
                      'driving/list.html', params)
    else:
        # それ以外
        return render(request,
                      'driving/index.html', params)
