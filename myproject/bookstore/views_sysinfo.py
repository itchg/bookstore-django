# -*- encoding: utf-8 -*-

from urllib import request
import json

from django.db.models import Count
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from bookstore.models import Book


@csrf_exempt
def listContries(webReq):
    if webReq.method == 'GET':
        apiResp = request.urlopen('https://api.openaq.org/v1/countries', data = None, timeout = 3000)
        print('response %s' % apiResp)
        apiData = apiResp.read().decode()
        print('response data:%s' % apiData)

        apiDataDict = json.loads(apiData)
        print(type(apiDataDict))

        result = []
        if 'results' in apiDataDict:
            for item in apiDataDict['results']:
                print('item:%s' % item)
                name = 'NaN'
                if 'name' in item:
                    name = item['name']
                code = 'NaN'
                if 'code' in item:
                    code = item['code']
                count = 0
                if 'count' in item:
                    count = item['count']
                    #对数据做调整，不管对错，缩小数据范围区间
                    if count > 10000000:
                        count *= 0.00001
                    elif count > 1000000:
                        count *= 0.0001
                    elif count > 500000:
                        count /= 1000
                    elif count > 100000:
                        count /= 500
                    elif count > 10000:
                        count /= 100

                result.append({
                    'name': name + '(' + code + ')',
                    'count': count
                })
        print('result: %s' % result)
        response = HttpResponse(json.dumps(result), content_type="application/json")

    else:
        response = HttpResponse('only accept GET/POST request, but got %s' % webReq.method)

    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Allow-Headers"] = "*"
    return response


bookType = {
    'novel': '小说',
    'biography': '人物传记',
    'magazin': '杂志',
    'philosophy': '哲学',
    'education': '教育',
    'history': '历史',
    'literature': '文学',
    'art': '艺术',
    'economic': '经济',
}

@csrf_exempt
def countBookByCategory(webReq):
    if webReq.method == 'GET':
        countBookByCategory = Book.objects.values('type').annotate(cnt = Count('id')).all()
        print('raw sql:%s' % countBookByCategory.query)
        # print('result:%s' % countBookByCategory)

        result = list(countBookByCategory)
        #type里面的英文转中文
        for item in result:
            item['type'] = bookType[item['type']]
        print('result:%s' % result)
        response = HttpResponse(json.dumps(result), content_type="application/json")

    else:
        response = HttpResponse('only accept GET/POST request, but got %s' % webReq.method)

    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Allow-Headers"] = "*"
    return response