from django.urls import path
from django.views.generic import RedirectView

from . import album_views, report_views

app_name = 'albums'
urlpatterns = [
    path('', RedirectView.as_view(url='album/index/')),
    path('album/data/', album_views.data, name='album_data'),
    path('album/edit/', album_views.edit, name='album_edit'),
    path('album/edit/<int:album_id>/', album_views.edit, name='album_edit'),
    path('album/index/', album_views.index, name='album_index'),
    path('album/report/', album_views.report, name='album_report'),
    path('album/save/', album_views.save, name='album_save'),
    path('report/edit/', report_views.edit, name='report_edit'),
    path('report/run/', report_views.run, name='report_run'),
    path('report/save/<str:report_type>/', report_views.save, name='report_save'),
]