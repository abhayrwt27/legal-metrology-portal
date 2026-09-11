from django.conf import settings
from rest_framework import serializers
from .models import Document

class DocumentSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = [
            "id", "application", "document_type", "title",
            "file", "file_url", "uploaded_by", "uploaded_at"
        ]
        read_only_fields = ["id", "file_url", "uploaded_by", "uploaded_at"]

    def get_file_url(self, obj):
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(obj.file.url)
        return obj.file.url
