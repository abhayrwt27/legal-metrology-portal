from datetime import date
from django.db import transaction
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User
from certificates.models import Certificate
from .models import Inspection, VerificationApplication
from .permissions import IsGATC, IsLMOOrAdmin
from .serializers import ApplicationSerializer, InspectionSerializer

class ApplicationListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = VerificationApplication.objects.select_related(
            "owner", "instrument", "assigned_gatc"
        ).prefetch_related("inspection")
        if request.user.is_owner:
            qs = qs.filter(owner=request.user)
        elif request.user.is_gatc:
            qs = qs.filter(assigned_gatc=request.user)
        return Response(ApplicationSerializer(qs, many=True, context={"request": request}).data)

    def post(self, request):
        if not request.user.is_owner:
            return Response({"detail": "Only owners can submit verification applications."}, status=403)
        serializer = ApplicationSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        application = serializer.save(
            owner=request.user,
            status=VerificationApplication.Status.SUBMITTED,
            submission_date=timezone.now(),
        )
        return Response(
            ApplicationSerializer(application, context={"request": request}).data,
            status=201,
        )

class ApplicationDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, application_id):
        try:
            app = VerificationApplication.objects.select_related(
                "owner", "instrument", "assigned_gatc"
            ).get(application_id=application_id)
        except VerificationApplication.DoesNotExist:
            return Response({"detail": "Application not found."}, status=404)

        if request.user.is_owner and app.owner_id != request.user.id:
            return Response({"detail": "You do not have permission to view this application."}, status=403)
        if request.user.is_gatc and app.assigned_gatc_id != request.user.id:
            return Response({"detail": "You do not have permission to view this application."}, status=403)

        return Response(ApplicationSerializer(app, context={"request": request}).data)

class AssignGATCView(APIView):
    permission_classes = [IsLMOOrAdmin]

    def post(self, request, application_id):
        try:
            app = VerificationApplication.objects.get(application_id=application_id)
        except VerificationApplication.DoesNotExist:
            return Response({"detail": "Application not found."}, status=404)

        gatc_id = request.data.get("gatc_id")
        try:
            gatc = User.objects.get(id=gatc_id, role=User.Role.GATC, is_active=True)
        except User.DoesNotExist:
            return Response({"detail": "Valid GATC officer not found."}, status=400)

        if app.status != VerificationApplication.Status.SUBMITTED:
            return Response({"detail": "Only submitted applications can be assigned."}, status=400)

        app.assigned_gatc = gatc
        app.status = VerificationApplication.Status.ASSIGNED
        app.save(update_fields=["assigned_gatc", "status", "updated_at"])
        return Response(ApplicationSerializer(app, context={"request": request}).data)

class InspectionCreateView(APIView):
    permission_classes = [IsGATC]

    def post(self, request, application_id):
        try:
            app = VerificationApplication.objects.get(
                application_id=application_id,
                assigned_gatc=request.user,
            )
        except VerificationApplication.DoesNotExist:
            return Response({"detail": "Assigned application not found."}, status=404)

        if app.status != VerificationApplication.Status.ASSIGNED:
            return Response({"detail": "This application is not ready for inspection."}, status=400)

        serializer = InspectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            inspection = serializer.save(application=app, inspector=request.user)
            app.status = VerificationApplication.Status.INSPECTION_COMPLETED
            app.save(update_fields=["status", "updated_at"])
        return Response(
            InspectionSerializer(inspection, context={"request": request}).data,
            status=201,
        )

class ApproveApplicationView(APIView):
    permission_classes = [IsLMOOrAdmin]

    def post(self, request, application_id):
        try:
            app = VerificationApplication.objects.select_related("instrument", "owner").get(
                application_id=application_id
            )
        except VerificationApplication.DoesNotExist:
            return Response({"detail": "Application not found."}, status=404)

        if app.status != VerificationApplication.Status.INSPECTION_COMPLETED:
            return Response(
                {"detail": "Application can only be approved after inspection is completed."},
                status=400,
            )

        inspection = getattr(app, "inspection", None)
        if not inspection:
            return Response({"detail": "Inspection record is missing."}, status=400)
        if inspection.result != Inspection.Result.PASS:
            return Response({"detail": "A failed inspection cannot be approved."}, status=400)

        expiry_date = date.today().replace(year=date.today().year + 1)
        certificate = Certificate.objects.create(
            instrument=app.instrument,
            application=app,
            issue_date=date.today(),
            expiry_date=expiry_date,
            verification_details=inspection.remarks,
        )
        app.status = VerificationApplication.Status.APPROVED
        app.lmo_remarks = request.data.get("remarks", "")
        app.save(update_fields=["status", "lmo_remarks", "updated_at"])

        return Response({
            "message": "Application approved and certificate generated.",
            "certificate_number": certificate.number,
            "application": ApplicationSerializer(app, context={"request": request}).data,
        })

class RejectApplicationView(APIView):
    permission_classes = [IsLMOOrAdmin]

    def post(self, request, application_id):
        try:
            app = VerificationApplication.objects.get(application_id=application_id)
        except VerificationApplication.DoesNotExist:
            return Response({"detail": "Application not found."}, status=404)

        if app.status != VerificationApplication.Status.INSPECTION_COMPLETED:
            return Response(
                {"detail": "Application can only be rejected after inspection is completed."},
                status=400,
            )

        reason = request.data.get("reason", "").strip()
        if not reason:
            return Response({"detail": "Rejection reason is required."}, status=400)

        app.status = VerificationApplication.Status.REJECTED
        app.rejection_reason = reason
        app.save(update_fields=["status", "rejection_reason", "updated_at"])
        return Response({"message": "Application rejected."})

class GATCUsersView(APIView):
    permission_classes = [IsLMOOrAdmin]

    def get(self, request):
        users = User.objects.filter(role=User.Role.GATC, is_active=True).order_by("first_name", "username")
        return Response([
            {"id": user.id, "name": user.get_full_name() or user.username, "username": user.username}
            for user in users
        ])

class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        apps = VerificationApplication.objects.all()
        certificates = Certificate.objects.all()
        if request.user.is_owner:
            apps = apps.filter(owner=request.user)
            certificates = certificates.filter(instrument__owner=request.user)
            return Response({
                "role": request.user.role,
                "total_instruments": request.user.instruments.count(),
                "active_certificates": certificates.filter(
                    status=Certificate.Status.ACTIVE, expiry_date__gte=timezone.localdate()
                ).count(),
                "expiring_certificates": certificates.filter(
                    expiry_date__gte=timezone.localdate(),
                    expiry_date__lte=timezone.localdate() + timezone.timedelta(days=30),
                ).count(),
                "pending_applications": apps.exclude(
                    status__in=[VerificationApplication.Status.APPROVED, VerificationApplication.Status.REJECTED]
                ).count(),
                "applications_by_status": list(
                    apps.values("status").order_by("status")
                ),
            })
        if request.user.is_gatc:
            apps = apps.filter(assigned_gatc=request.user)
            return Response({
                "role": request.user.role,
                "assigned_applications": apps.count(),
                "pending_inspections": apps.filter(status=VerificationApplication.Status.ASSIGNED).count(),
                "completed_inspections": apps.filter(status=VerificationApplication.Status.INSPECTION_COMPLETED).count(),
                "passed_inspections": apps.filter(inspection__result=Inspection.Result.PASS).count(),
                "failed_inspections": apps.filter(inspection__result=Inspection.Result.FAIL).count(),
            })
        return Response({
            "role": request.user.role,
            "total_applications": apps.count(),
            "submitted_applications": apps.filter(status=VerificationApplication.Status.SUBMITTED).count(),
            "assigned_applications": apps.filter(status=VerificationApplication.Status.ASSIGNED).count(),
            "completed_inspections": apps.filter(status=VerificationApplication.Status.INSPECTION_COMPLETED).count(),
            "approved_applications": apps.filter(status=VerificationApplication.Status.APPROVED).count(),
            "rejected_applications": apps.filter(status=VerificationApplication.Status.REJECTED).count(),
            "active_certificates": certificates.filter(status=Certificate.Status.ACTIVE).count(),
            "expiring_certificates": certificates.filter(
                expiry_date__gte=timezone.localdate(),
                expiry_date__lte=timezone.localdate() + timezone.timedelta(days=30),
            ).count(),
        })
