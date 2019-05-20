from django.shortcuts import render

# Create your views here.
# importing required packages
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from TwitterApp import twittery
from django.http import HttpResponse

# disabling csrf (cross site request forgery)
@csrf_exempt
def getResult(request):
    if request.method == 'GET':
        return render(request, 'index.html')
    # if post request came
    if request.method == 'POST':
        # getting values from post
        inputer = request.POST.get('inputer')
        pttweets,nttweets,nuetweets,ptttweets,ntttweets,inputer = twittery.main(inputer)
        print(pttweets,nttweets,nuetweets,ptttweets,ntttweets,inputer)
        return render(request, 'response.html', {"r": pttweets,"s": nttweets,"t":nuetweets,"u":ptttweets,"v":ntttweets,"w":inputer})
