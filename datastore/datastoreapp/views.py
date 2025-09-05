from django.shortcuts import render
from rest_framework import generics
from datastoreapp.models import File
from datastoreapp.serializers import FileSerializer

# Create your views here.
class FileRecord(generics.RetrieveUpdateDestroyAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status

class FileCollection(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request, *args, **kwargs):
        files = File.objects.all()
        serializer = FileSerializer(files, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        uploaded_file = request.FILES.get("file")
        if not uploaded_file:
            return Response({"detail": "No file provided"}, status=400)

        # Save to MySQL
        file_record = File.objects.create(
            name=uploaded_file.name,
            size=uploaded_file.size,
        )

        # Successful upload
        return Response(FileSerializer(file_record).data, status=status.HTTP_201_CREATED)