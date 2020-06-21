import requests
import json
import xmltodict

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from config.settings.base import tourAPI_key


# f'listYN=Y&arrange=A&mapX=126.981611&mapY=37.568477&radius=1000').content
@api_view(['GET'])
def tourAPI(request):
    lang = request.query_params.get('language')
    mapX = request.query_params.get('mapX')  # 126.981611
    mapY = request.query_params.get('mapY')  # 37.568477
    radius = request.query_params.get('radius') # 1000
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
    request_language = language[lang]
    response = requests.get(
        f'http://api.visitkorea.or.kr/openapi/service/rest/{request_language}/locationBasedList?serviceKey={tourAPI_key}'
        f'&numOfRows=10&pageSize=10&pageNo=1&startPage=1&MobileOS=ETC&MobileApp=AppTest&'
        f'listYN=Y&arrange=A&mapX={mapX}&mapY={mapY}&radius={radius}').content
    xmlObj = xmltodict.parse(response)
    json_data = json.dumps(xmlObj)
    dict_data = json.loads(json_data)

    data = {'response': dict_data}
    return Response(data, status=status.HTTP_200_OK)
