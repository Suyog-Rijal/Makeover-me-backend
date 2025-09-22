from django.urls import path, include
from api.views import LocationsApiView


urlpatterns = [
	path('auth/', include('account.urls')),
    path('locations/', LocationsApiView.as_view(), name='locations')
]

