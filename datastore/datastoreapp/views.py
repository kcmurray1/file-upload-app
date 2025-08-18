from django.shortcuts import render
from rest_framework import generics
from datastoreapp.models import File
from datastoreapp.serializers import FileSerializer

# Create your views here.
class FileRecord(generics.RetrieveUpdateDestroyAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer

class FileCollection(generics.ListCreateAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer