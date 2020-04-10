"""
URL patterns for `apps.iiif.canvases`
"""
from django.urls import path
from .views import IIIFV2Detail, IIIFV2List

urlpatterns = [
    path('iiif/<manifest>/canvas', IIIFV2List.as_view(), name='RenderCanvasList'),
    path('iiif/<manifest>/canvas/<pid>', IIIFV2Detail.as_view(), name='RenderCanvasDetail'),
]
