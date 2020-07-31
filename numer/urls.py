"""numer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.utils import timezone
from django.views.decorators.cache import cache_page
from django.views.decorators.http import last_modified
from django.views.i18n import JavaScriptCatalog

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.core import urls as wagtail_urls

from frontend.urls import urls as frontend_urls
from favorites.urls import urls as numer_favs_api
from schoolform.urls import urls as numer_school_form_api
from blog.urls import urls as wgtail_custom_api
from comments.urls import urls as wgtail_post_comments_api
from likes.urls import urls as wgtail_likes_api
from app.urls import urls as numer_app_api
from service.urls import urls as numer_service_api
from promocode.urls import urls as codes_api
from events.urls import urls as events_api
from smsgate.urls import urls as smsgate_api
from schoolpub.urls import urls as schoolpub_urls

from misago.users.forms.auth import AdminAuthenticationForm
from blog.api import api_router
from django_tinkoff_merchant.urls import urlpatterns as tinkoff_urls
from push_notifications.api.rest_framework import APNSDeviceAuthorizedViewSet, GCMDeviceAuthorizedViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'device/apns', APNSDeviceAuthorizedViewSet)
router.register(r'device/gcm', GCMDeviceAuthorizedViewSet)



admin.autodiscover()
admin.site.login_form = AdminAuthenticationForm


urlpatterns = [
    url(r'^forum/', include('misago.urls', namespace='misago')),
    url(r'^social', include('social_django.urls', namespace='social')),

    # Javascript translations
    url(
        r'^django-i18n.js$',
        last_modified(lambda req, **kw: timezone.now())(
            cache_page(86400 * 2, key_prefix='misagojsi18n')(
                JavaScriptCatalog.as_view(
                    packages=['misago'],
                ),
            ),
        ),
        name='django-i18n',
    ),

    # Uncomment next line if you plan to use Django admin for 3rd party apps
    url(r'^django-admin/', admin.site.urls),

    url(r'^cms/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),
    url(r'^pages/', include(wagtail_urls)),
    url(r'^api/v2/',api_router.urls),
    url(r'^', include(smsgate_api)),
    url(r'^', include(numer_app_api)),
    url(r'^', include(numer_favs_api)),
    url(r'^', include(numer_school_form_api)),
    url(r'^', include(schoolpub_urls)),
    url(r'^', include(frontend_urls)),
    url(r'^', include(wgtail_custom_api)),
    url(r'^', include(wgtail_post_comments_api)),
    url(r'^', include(wgtail_likes_api)),
    url(r'^', include(tinkoff_urls)),
    url(r'^', include(numer_service_api)),
    url(r'^', include(codes_api)),
    url(r'^', include(events_api)),
    url(r'^', include(router.urls)),

]

if 'users' in settings.INSTALLED_APPS:
    from users.urls import urls as users_urls
    urlpatterns += [url(r'^', include(users_urls)),]


# If debug mode is enabled, include debug toolbar
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]


urlpatterns += [url(r'^', include(wagtail_urls)),]

# Use static file server for static and media files (debug only)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# Error Handlers
# Misago needs those handlers to deal with errors raised by it's middlewares
# If you replace those handlers with custom ones, make sure you decorate them
# with shared_403_exception_handler or shared_404_exception_handler
# decorators that are defined in misago.views.errorpages module!
# handler403 = 'misago.core.errorpages.permission_denied'
# handler404 = 'misago.core.errorpages.page_not_found'
