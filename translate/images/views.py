from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status
from django.http import HttpResponse
from django.http import FileResponse

from .models import Webtoon
from .translate import TranslateImage
from .forms import WebtoonForm
import requests

class ImageViewSet(viewsets.ViewSet):
    def retrieve(self, request):
        print("POST Translate Image")
        if request.method == 'POST':
            form = WebtoonForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                print("Form saved")
            else:
                print("form invalid")
            filename = request.FILES['webtoon_img'].name
            response_path = TranslateImage(filename)
            img = open(response_path, 'rb')
            response = FileResponse(img)
            return response
            #return Response(response, status=status.HTTP_201_CREATED)
            #return HttpResponse(response, content_type="image/png")

        else:
            form = WebtoonForm()
        return Response(None, status=status.HTTP_201_CREATED)