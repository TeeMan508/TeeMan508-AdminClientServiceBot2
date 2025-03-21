from starlette.exceptions import HTTPException
from pydantic import ValidationError
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .logger import logger, correlation_id_ctx
from ..user.facades import *
from ..user.schemas.request import (RegisterAdminRequestData,
                                    RegisterClientRequestData,
                                    SetClientToAdminRequestData,
                                    FreeAdminRequestData,
                                    GetClientRequestData,
                                    GetAdminByClientRequestData,
                                    SetNextClientRequestData,
                                    )
from ..user.schemas.domain import AdminCredentials, ClientCredentials
from ..user.schemas.response import EmptyResponseData, IdResponseData, ComplaintResponse


class RegisterAdminView(APIView):
    def post(self, request: Request): # noqa
        try:
            correlation_id_ctx.set(request.META.get('HTTP_X_CORRELATION_ID'))

            body = RegisterAdminRequestData.model_validate(request.POST.dict())
            creds = AdminCredentials.model_validate(body.model_dump())
            register_admin(creds)

            logger.info("Admin registered.")
            return Response(EmptyResponseData().model_dump(), status=status.HTTP_200_OK)

        except HTTPException:
            logger.info("Admin already registered.")
            return Response(EmptyResponseData().model_dump(), status=status.HTTP_400_BAD_REQUEST)
        except ValidationError:
            logger.info("Wrong request format.")
            return Response(EmptyResponseData().model_dump(), status=status.HTTP_400_BAD_REQUEST)


class RegisterClientView(APIView):
    def post(self, request: Request): # noqa
        try:
            correlation_id_ctx.set(request.META.get('HTTP_X_CORRELATION_ID'))

            body = RegisterClientRequestData.model_validate(request.POST.dict())
            creds = ClientCredentials.model_validate(body.model_dump())
            register_client(creds)

            logger.info("Client registered.")
            return Response(EmptyResponseData().model_dump(), status=status.HTTP_200_OK)

        except HTTPException:
            logger.info("Client already registered.")
            return Response(EmptyResponseData().model_dump(), status=status.HTTP_400_BAD_REQUEST)
        except ValidationError:
            logger.info("Wrong request format.")
            return Response(EmptyResponseData().model_dump(), status=status.HTTP_400_BAD_REQUEST)


class SetClientToRandomAdminView(APIView):
    def post(self, request: Request): # noqa
        try:
            correlation_id_ctx.set(request.META.get('HTTP_X_CORRELATION_ID'))

            body = SetClientToAdminRequestData.model_validate(request.POST.dict())
            admin_id = set_client_to_random_admin(body.tg_id)
            response_model = IdResponseData.model_validate({"tg_id": admin_id})

            logger.info("Client set to admin.")
            return Response(response_model.model_dump(), status=status.HTTP_200_OK)

        except HTTPException:
            logger.info("No free admins.")
            return Response(EmptyResponseData().model_dump(), status=status.HTTP_400_BAD_REQUEST)
        except ValidationError:
            logger.info("Wrong request format.")
            return Response(EmptyResponseData().model_dump(), status=status.HTTP_400_BAD_REQUEST)


class FreeAdminAndDeleteClientView(APIView):
    def post(self, request: Request): # noqa
        try:
            correlation_id_ctx.set(request.META.get('HTTP_X_CORRELATION_ID'))

            body = FreeAdminRequestData.model_validate(request.POST.dict())
            free_admin_and_clear_client(AdminCredentials(tg_id=body.tg_id))

            logger.info("Admin free and client deleted.")
            return Response(EmptyResponseData().model_dump(), status=status.HTTP_200_OK)

        except HTTPException:
            logger.info("No such admin or client.")
            return Response(EmptyResponseData().model_dump(), status=status.HTTP_400_BAD_REQUEST)
        except ValidationError:
            logger.info("Wrong request format.")
            return Response(EmptyResponseData().model_dump(), status=status.HTTP_400_BAD_REQUEST)


class GetCurrentClientView(APIView):
    def get(self, request: Request): # noqa
        try:
            correlation_id_ctx.set(request.META.get('HTTP_X_CORRELATION_ID'))

            body = GetClientRequestData.model_validate(request.data.dict())
            client_id = get_current_client(body.tg_id)
            response_model = IdResponseData.model_validate({"tg_id": client_id})

            logger.info("Client found.")
            return Response(response_model.model_dump(), status=status.HTTP_200_OK)

        except HTTPException:
            logger.info("No current client.")
            return Response(EmptyResponseData().model_dump(), status=status.HTTP_400_BAD_REQUEST)
        except ValidationError:
            logger.info("Wrong request format.")
            return Response(EmptyResponseData().model_dump(), status=status.HTTP_400_BAD_REQUEST)



class GetAdminByClientView(APIView):
    def get(self, request: Request): # noqa
        try:
            correlation_id_ctx.set(request.META.get('HTTP_X_CORRELATION_ID'))

            body = GetAdminByClientRequestData.model_validate(request.data.dict())
            admin_id = get_admin_by_client(body.tg_id)
            response_model = IdResponseData.model_validate({"tg_id": admin_id})

            logger.info("Admin found.")
            return Response(response_model.model_dump(), status=status.HTTP_200_OK)

        except HTTPException:
            logger.info(f"No such admin found for client")
            return Response(EmptyResponseData().model_dump(), status=status.HTTP_400_BAD_REQUEST)
        except ValidationError:
            logger.info("Wrong request format.")
            return Response(EmptyResponseData().model_dump(), status=status.HTTP_400_BAD_REQUEST)


class SetNextClientToAdminView(APIView):
    def post(self, request: Request): # noqa
        try:
            correlation_id_ctx.set(request.META.get('HTTP_X_CORRELATION_ID'))

            body = SetNextClientRequestData.model_validate(request.POST.dict())
            complaint = set_next_client_to_admin(body.tg_id)
            response_model = ComplaintResponse.model_validate({"complaint": complaint})
            logger.info("Next client set to admin.")
            return Response(response_model.model_dump(), status=status.HTTP_200_OK)

        except HTTPException:
            logger.info("No unhandled clients.")
            return Response(EmptyResponseData().model_dump(), status=status.HTTP_400_BAD_REQUEST)
        except ValidationError:
            logger.info("Wrong request format.")
            return Response(EmptyResponseData().model_dump(), status=status.HTTP_400_BAD_REQUEST)