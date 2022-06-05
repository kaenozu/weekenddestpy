import logging
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from driving.forms import SrcForm, destForm
from driving.models import Dest, Src, geoCash
from geopy.distance import geodesic
import random

from driving.utils.geo import Geo

# Create your views here.


@require_http_methods(['GET'])
def driving_index(request):
    """検索画面"""

    params = {
        'form': SrcForm(request.GET or None),
    }

    if "src" in request.GET:
        # 出発地が設定されている場合
        srcParam = request.GET.get("src")
        src = []
        # 検索したことがある場所ならcashから取得
        
        geocash = geoCash.objects.filter(src=srcParam)
        if geocash.exists():
            src.append(geoCash.latitude)
            src.append(geoCash.longitude)
        else:
            geo = Geo().getGeo(srcParam)
        
        dest = Dest.objects.all()

        randomDest = []
        for d in dest:
            dis = geodesic((float(src[0]), float(src[1])),
                           (float(d.latitude), float(d.longitude))).km
            if dis <= 50:
                randomDest.append(d)

        # ランダムに１つ選ぶ
        choiced = random.choice(randomDest)
        
        params["destForm"] = destForm(dict(name=choiced.name, latitude=choiced.latitude, longitude=choiced.longitude, localway=dis))

        return render(request,
                      'driving/list.html', params)
    else:
        # それ以外
        return render(request,
                      'driving/index.html', params)
