from django.conf import settings
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from verification.models import VerificationApplication
from .models import Document
from .serializers import DocumentSerializer

class DocumentListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        qs = Document.objects.select_related("application", "uploaded_by")
        if request.user.is_owner:
            qs = qs.filter(application__owner=request.user)
        elif request.user.is_gatc:
            qs = qs.filter(application__assigned_gatc=request.user)
        return Response(DocumentSerializer(qs, many=True, context={"request": request}).data)

    def post(self, request):
        application_id = request.data.get("application")
        try:
            application = VerificationApplication.objects.get(application_id=application_id)
        except VerificationApplication.DoesNotExist:
            return Response({"detail": "Application not found."}, status=404)

        if request.user.is_owner and application.owner_id != request.user.id:
            return Response({"detail": "You do not have permission to upload to this application."}, status=403)
        if request.user.is_gatc and application.assigned_gatc_id != request.user.id:
            return Response({"detail": "You do not have permission to upload to this application."}, status=403)

        uploaded = request.FILES.get("file")
        if not uploaded:
            return Response({"detail": "A file is required."}, status=400)
        if uploaded.size > getattr(settings, "MAX_UPLOAD_SIZE", 10 * 1024 * 1024):
            return Response({"detail": "File is too large. Maximum size is 10 MB."}, status=400)

        serializer = DocumentSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        document = serializer.save(uploaded_by=request.user, application=application)
        return Response(DocumentSerializer(document, context={"request": request}).data, status=201)
