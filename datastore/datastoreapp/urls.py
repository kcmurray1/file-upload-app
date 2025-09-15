from django.urls import path
from datastoreapp.views import FileCollection, FileRecord, FileDownload

urlpatterns = [
    path("files", FileCollection.as_view(), name='file-collection'),
    path("file/<int:pk>", FileRecord.as_view(), name='file-record'),
    path("files/<str:filename>/download", FileDownload.as_view(), name="file-download"),

]