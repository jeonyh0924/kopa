from collections import defaultdict

import requests
import json

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from config.settings.base import tourAPI_key


# f'listYN=Y&arrange=A&mapX=126.981611&mapY=37.568477&radius=1000').content
@api_view(['GET'])
def tourAPI(request):
    import xmltodict
    mapX = request.query_params.get('mapX')  # 126.981611
    mapY = request.query_params.get('mapY')  # 37.568477
    radius = request.query_params.get('radius')  # 1000
    language = {
        "EngService": "EngService",
        "JpnService": "JpnService",
        "ChsService": "ChsService",
        "ChtService": "ChtService",
        "GerService": "GerService",
        "FreService": "FreService",
        "SpnService": "SpnService",
        "RusService": "RusService",
    }
    request_language = language[request.query_params.get('language')]
    response = requests.get(
        f'http://api.visitkorea.or.kr/openapi/service/rest/{request_language}/locationBasedList?serviceKey={tourAPI_key}'
        f'&numOfRows=10&pageSize=10&pageNo=1&startPage=1&MobileOS=ETC&MobileApp=AppTest&'
        f'listYN=Y&arrange=A&mapX={mapX}&mapY={mapY}&radius={radius}').content
    xmltodict = xmltodict.parse(response)

    json_data = json.dumps(xmltodict)

    dict_data = json.loads(json_data)

    first_request = dict_data['response']['body']['items']['item']

    for data in first_request:
        import xmltodict
        test_id = data['contentid']

        response = requests.get(
            f'http://api.visitkorea.or.kr/openapi/service/rest/{request_language}/detailCommon?serviceKey={tourAPI_key}'
            f'&numOfRows=10&pageSize=10&pageNo=1&MobileOS=ETC&MobileApp=AppTest&contentId={test_id}'
            f'&defaultYN=Y&addrinfoYN=Y&overviewYN=Y').content
        xmltodict = xmltodict.parse(response)
        json_data = json.dumps(xmltodict)
        dict_data = json.loads(json_data)
        if dict_data['response']['body']['items']['item'].get('overview'):
            overview_data = dict_data['response']['body']['items']['item']['overview']
            data['overview'] = overview_data

        if dict_data['response']['body']['items']['item'].get('homepage'):
            homepage_data = dict_data['response']['body']['items']['item']['homepage']
            # print(homepage_data)
            data['homepage'] = homepage_data

        data['overview'] = overview_data
        #
        # print(data)
        #
        # print('\n반복문\n')
    print(len(first_request))
    data = {
        'result': first_request,
    }
    return Response(data, status=status.HTTP_200_OK)

#
# @api_view(['GET'])
# def otherRequsetAPI(request):
#     import xmltodict
#     mapX = request.query_params.get('mapX')  # 126.981611
#     mapY = request.query_params.get('mapY')  # 37.568477
#     radius = request.query_params.get('radius')  # 1000
#     language = {
#         "EngService": "EngService",
#         "JpnService": "JpnService",
#         "ChsService": "ChsService",
#         "ChtService": "ChtService",
#         "GerService": "GerService",
#         "FreService": "FreService",
#         "SpnService": "SpnService",
#         "RusService": "RusService",
#     }
#     request_language = language[request.query_params.get('language')]
#     response = requests.get(
#         f'http://api.visitkorea.or.kr/openapi/service/rest/{request_language}/locationBasedList?serviceKey={tourAPI_key}'
#         f'&numOfRows=10&pageSize=10&pageNo=1&startPage=1&MobileOS=ETC&MobileApp=AppTest&'
#         f'listYN=Y&arrange=A&mapX={mapX}&mapY={mapY}&radius={radius}').content
#     xmltodict = xmltodict.parse(response)
#
#     json_data = json.dumps(xmltodict)
#
#     dict_data = json.loads(json_data)
#
#     first_request = dict_data['response']['body']['items']['item']
#     second_request = []
#     for data in first_request:
#         import xmltodict
#         test_id = data['contentid']
#
#         response = requests.get(
#             f'http://api.visitkorea.or.kr/openapi/service/rest/{request_language}/detailCommon?serviceKey={tourAPI_key}'
#             f'&numOfRows=10&pageSize=10&pageNo=1&MobileOS=ETC&MobileApp=AppTest&contentId={test_id}'
#             f'&defaultYN=Y&addrinfoYN=Y&overviewYN=Y').content
#         xmltodict = xmltodict.parse(response)
#         json_data = json.dumps(xmltodict)
#         dict_data = json.loads(json_data)
#         second_request.append(dict_data)
#         print('\n반복문\n')
#         print(dict_data)
#
#     result = defaultdict(list)
#     index = 1
#     for x, y in zip(first_request, second_request):
#         result[index].append(x)
#         result[index].append(y)
#         index += 1
#
#     data = {
#         'result': result,
#     }
#     return Response(data, status=status.HTTP_200_OK)
