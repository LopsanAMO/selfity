from django.conf import settings
from django.urls import path, re_path, include, reverse_lazy
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView,\
    SpectacularSwaggerView
from .users.views import UserViewSet, UserCreateViewSet,\
    UserPhoneCreateViewSet, UserPhoneCreateSesionViewSet,\
    UserValidateTokenViewSet, PostCreateViewSet, PostRetrieveViewSet,\
    PostListViewSet, PostHashtagListViewSet
from selfity.curp.views import CurpViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'users', UserCreateViewSet)
router.register(r'signup', UserPhoneCreateViewSet)
router.register(r'verify-session', UserValidateTokenViewSet)
router.register(r'validate-number', UserPhoneCreateSesionViewSet)
router.register(r'post', PostCreateViewSet)
router.register(r'post', PostRetrieveViewSet)
router.register(r'posts', PostListViewSet)
router.register(r'posts/hashtags', PostHashtagListViewSet)
router.register(r'curp', CurpViewSet, basename='curp-detail')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api-token-auth/', views.obtain_auth_token),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # the 'api-root' from django rest-frameworks default router
    # http://www.django-rest-framework.org/api-guide/routers/#defaultrouter
    re_path(r'^$', RedirectView.as_view(url=reverse_lazy('api-root'), permanent=False)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
