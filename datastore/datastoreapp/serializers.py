from rest_framework import serializers
from datastoreapp.models import File

class FileSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    def get_children(self, obj):
        return FileSerializer(obj.children.all(), many=True).data
    
    class Meta:
        model = File
        fields = "__all__"