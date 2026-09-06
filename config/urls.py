from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path( "admin/",admin.site.urls ),
    path("api/auth/",include("accounts.urls")),
    path("api/",include("doctors.urls")),
    path("api/",include("patients.urls")),
    path("api/",include("services.urls")),
    path("api/",include("appointments.urls"),),
    path("api/",include("medical_records.urls"),),
    path("api/payments/",include("payments.urls"),),

]
if settings.DEBUG:
    urlpatterns +=static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
