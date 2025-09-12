from celery.bin.control import status
from django.http import JsonResponse
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from api.models import Region, City, Area
from api.serializers import SimpleRegionSerializer, SimpleCitySerializer, SimpleAreaSerializer


def csrf_failure(request, reason=""):
    return JsonResponse({
        "detail": "CSRF verification failed. Request aborted.",
        "reason": "Invalid or missing CSRF token."
    }, status=403)


class LocationsApiView(APIView):
    http_method_names = ['get']
    permission_classes = [AllowAny]

    @extend_schema(
        tags=['Locations'],
        auth=[],
        summary="Get regions, cities, or areas",
        parameters=[
            OpenApiParameter(name='region', type=str, required=False, description="Filter by region ID"),
            OpenApiParameter(name='city', type=str, required=False, description="Filter by city ID"),
        ],
        responses={
            200: SimpleRegionSerializer(many=True),
            400: None,
            500: None,
        }
    )
    def get(self, request, *args, **kwargs):
        reg_id = request.query_params.get('region', None)
        city_id = request.query_params.get('city', None)

        if reg_id and city_id:
            return JsonResponse({"detail": "Provide either 'region' or 'city' parameter, not both."}, status=status.HTTP_400_BAD_REQUEST)

        if not reg_id and not city_id:
            try:
                data = Region.objects.all()
                serializer = SimpleRegionSerializer(data, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                print(e)
                return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if reg_id:
            try:
                data = City.objects.filter(region_id=reg_id)
                serializer = SimpleCitySerializer(data, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                print(e)
                return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if city_id:
            try:
                data = Area.objects.filter(city_id=city_id)
                serializer = SimpleAreaSerializer(data, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                print(e)
                return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return JsonResponse({"detail": "Not implemented"}, status=status.Http_501_not_implemented)
