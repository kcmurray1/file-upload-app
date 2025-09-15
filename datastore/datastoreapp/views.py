from django.shortcuts import render
from rest_framework import generics
from datastoreapp.models import File
from datastoreapp.serializers import FileSerializer
import boto3
import mimetypes

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


        # upload to s3 and Save to MySQL
        try:
            s3 = boto3.client('s3')
            s3.upload_fileobj(uploaded_file, 'devop-bucket-01', uploaded_file.name)
             
            file_record = File.objects.create(
                name=uploaded_file.name,
                size=uploaded_file.size,
            )
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # Successful upload
        return Response(FileSerializer(file_record).data, status=status.HTTP_201_CREATED)

class FileDownload(APIView):
    def get(self, request, filename):
        s3 = boto3.client("s3")
        content_type, _ = mimetypes.guess_type(filename)
        if content_type is None:
            content_type = "application/octet-stream"

        url = s3.generate_presigned_url(
            "get_object",
            Params={
              "Bucket": "devop-bucket-01",
              "Key": filename,
              "ResponseContentDisposition" : f"inline; filename={filename}",
              "ResponseContentType" : content_type,
            },
            ExpiresIn=3600
        )
        return Response({"url": url})

