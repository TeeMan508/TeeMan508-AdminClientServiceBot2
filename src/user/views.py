import random

import requests
from django.http import JsonResponse, HttpResponse
from rest_framework import status
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings

from .logger import logger
from .models import Client
from .models import Admin

class RegisterClientView(APIView):
    def post(self, request: Request): # noqa
        body = request.data

        if Client.objects.filter(tg_id=body.get("tg_id", "0")).count() > 0:
            return JsonResponse({}, status=status.HTTP_200_OK)

        Client.objects.create(
            tg_id=body.get("tg_id", "0"),
            complaint=body.get("complaint", "blank_complaint")
        )

        return JsonResponse({}, status=status.HTTP_201_CREATED)


class RegisterAdminView(APIView):
    def post(self, request: Request): # noqa
        body = request.data

        if Admin.objects.filter(tg_id=body.get("tg_id", "0")).count() > 0:
            return Response(status=status.HTTP_200_OK, data=f"Admin with id {body.get('tg_id', '0')} already exists")

        Admin.objects.create(
            tg_id=body.get("tg_id", "0"),
        )

        return JsonResponse({}, status=status.HTTP_201_CREATED)


class HandleComplaintView(APIView):
    def post(self, request: Request): # noqa
        body = request.data
        qs = Admin.objects.filter(is_busy=False)

        if qs.count() == 0:
            return JsonResponse({}, status=status.HTTP_204_NO_CONTENT)

        tarnished: Admin = random.choice(qs)

        if client_id := body.get("tg_id", None):
            client = Client.objects.get(tg_id=client_id)
            client.is_handling = True
            client.save()

            tarnished.current_client = client
            tarnished.is_busy = True
            tarnished.save()

            return JsonResponse({"tg_id": tarnished.tg_id, "complaint": client.complaint}, status=status.HTTP_200_OK)

        return JsonResponse({}, status=status.HTTP_400_BAD_REQUEST)


class ClearClientView(APIView):
    def post(self, request: Request): # noqa
        body = request.data

        if client_id := body.get("tg_id", None):
            client = Client.objects.filter(tg_id=client_id)
            if client.count() == 0:
                return JsonResponse({}, status=status.HTTP_204_NO_CONTENT)

            client.delete()

            return JsonResponse({}, status=status.HTTP_200_OK)

        return JsonResponse({}, status=status.HTTP_204_NO_CONTENT)


HANDLE_COMPLAINT_URL = "http://web:8000/api/user/handle_complaint" # TODO: change for proper request to another apiview

class FreeAdminView(APIView):
    def post(self, request: Request): # noqa
        body = request.data

        if admin_id := body.get("tg_id", None):
            admin = Admin.objects.filter(tg_id=admin_id)

            if admin.count() == 0:
                return JsonResponse({}, status=status.HTTP_204_NO_CONTENT)

            current_admin = admin.first()
            current_admin.is_busy = False
            current_admin.save()

        clients_qs = Client.objects.filter(is_handling=False).order_by("created_at")

        if clients_qs.count() == 0:
            return JsonResponse({}, status=status.HTTP_207_MULTI_STATUS)

        oldest_client = clients_qs.first()
        oldest_client.is_handling = True
        oldest_client.save()

        response = requests.post(HANDLE_COMPLAINT_URL, data={"tg_id": oldest_client.tg_id}) # todo:

        return JsonResponse(response.json(), status=status.HTTP_200_OK)


class GetCurrentClientView(APIView):
    def post(self, request: Request): # noqa
        body = request.data

        if admin_id := body.get("tg_id", None):
            admin = Admin.objects.filter(tg_id=admin_id).select_related("current_client")[0]
            logger.info(admin.current_client.tg_id)
            return JsonResponse({"tg_id": admin.current_client.tg_id}, status=status.HTTP_200_OK)

        return JsonResponse({}, status=status.HTTP_204_NO_CONTENT)