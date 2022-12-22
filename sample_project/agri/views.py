from http.client import HTTPResponse
from django.shortcuts import render
from django.http import HttpResponse
from joblib import load
from .models import District
recommend = load("SavedModels/Crop_recommendation_model.sav")
soil = ['Alluvial', 'Black', 'Clayey', 'Laterite', 'Loamy', 'Red', 'Sandy']
season_list = ['Kharif', 'Rabi']
crops = ['banana', 'coconut', 'tea', 'rubber', 'tapioca', 'coffee', 'cardamom', 'betel', 'bamboo','ladiesfinger','brinjal',
'moringa', 'potato', 'mango', 'cloves', 'chillies', 'cashew', 'arecanut', 'cocoa']
# Create your views here.
def index(request):
    return render(request, 'index.html')

def results(request):
    print("fffff", request)
    season = request.GET['season']
    district = request.GET['district']
    soil_type = request.GET['soil_type']
    pH = float(request.GET['ph'])
    nitrogen = float(request.GET['nitrogen'])
    potassium = float(request.GET['potassium'])
    phosphorus = float(request.GET['phosphorus'])
    area = float(request.GET['area'])
    soil_index = soil.index(soil_type)
    season_index = season_list.index(season)
    dists = District.objects.filter(Name = district).values()
    Rainfall, Humidity, Min_temp, Max_temp = 0, 0, 0, 0
    for i in dists:
        Rainfall = i['Rainfall']
        Humidity = i['Humidity']
        Min_temp = i['Min_Temp']
        Max_temp = i['Max_Temp']

    inputs = [nitrogen, potassium, phosphorus, Humidity, pH, Rainfall, Min_temp, Max_temp]
    for i in range(2):
        if(i == season_index):
            inputs.append(1)
        else:
            inputs.append(0)
    for i in range(0,7):
        if(i == soil_index):
            inputs.append(1)
        else:
            inputs.append(0)
    crop = recommend.predict([inputs])
    print("Result is:", crop)
    crop_temp = crop[0].lower()
    crop_temp = crop_temp[:3]
    for i in crops:
        if(i[:3] == crop_temp):
            yield_predict = load("SavedModels/{0}.sav".format(i))
            break

    yield_list = [area, 50, soil_index]
    answer = yield_predict.predict([yield_list])
    print("Total yield: ", answer)
    return render(request, 'results.html', {'crop':crop[0], 'yield': round(answer[0], 4)})
