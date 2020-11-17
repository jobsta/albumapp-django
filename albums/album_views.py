import datetime
import io
import json

from django.forms.models import model_to_dict
from django.http import HttpResponseBadRequest, HttpResponseServerError, HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.safestring import SafeString
from django.utils.translation import gettext as _
from django.views.decorators.csrf import ensure_csrf_cookie
from reportbro import Report, ReportBroError

from .models import Album, ReportDefinition
from .utils import create_album_report_template, get_menu_items


def data(request):
    """Returns available albums from the database. Can be optionally filtered by year.

    This is called from templates/albums/album/index.html when the year input is changed.
    """
    year = request.GET.get('year')
    if year:
        try:
            year = int(year)
        except (ValueError, TypeError):
            return HttpResponseBadRequest('invalid year parameter')
    else:
        year = None
    return JsonResponse(list(get_albums(year)), safe=False)


@ensure_csrf_cookie
def edit(request, album_id=None):
    """Shows an edit form to add new or edit an existing album."""
    context = dict(is_new=album_id is None)
    context['menu_items'] = get_menu_items('album')
    if album_id is not None:
        album = Album.objects.get(id=album_id)
        context['album'] = SafeString(json.dumps(model_to_dict(album)))
    else:
        context['album'] = SafeString(json.dumps(dict(id='', name='', year=None, best_of_compilation=False)))
    return render(request, 'albums/album/edit.html', context)


@ensure_csrf_cookie
def index(request):
    """Shows a page where all available albums are listed."""
    context = dict()
    context['menu_items'] = get_menu_items('album')
    context['albums'] = SafeString(json.dumps(list(get_albums())))
    return render(request, 'albums/album/index.html', context)


def report(request):
    """Prints a pdf file with all available albums.

    The albums can be optionally filtered by year. reportbro-lib is used to
    generate the pdf file. The data itself is retrieved
    from the database (*get_albums*). The report_definition
    is also stored in the database and is created on-the-fly if not present (to make
    this Demo App easier to use).
    """
    year = request.GET.get('year')
    if year:
        try:
            year = int(year)
        except (ValueError, TypeError):
            return HttpResponseBadRequest('invalid year parameter')
    else:
        year = None

    # NOTE: these params must match exactly with the parameters defined in the
    # report definition in ReportBro Designer, check the name and type (Number, Date, List, ...)
    # of those parameters in the Designer.
    params = dict(year=year, albums=list(get_albums(year)), current_date=datetime.datetime.now())

    if ReportDefinition.objects.filter(report_type='albums_report').count() == 0:
        create_album_report_template()

    report_definition = ReportDefinition.objects.get(report_type='albums_report')
    if not report_definition:
        return HttpResponseServerError('no report_definition available')

    try:
        report_inst = Report(json.loads(report_definition.report_definition), params)
        if report_inst.errors:
            # report definition should never contain any errors,
            # unless you saved an invalid report and didn't test in ReportBro Designer
            raise ReportBroError(report_inst.errors[0])

        pdf_report = report_inst.generate_pdf()
        response = HttpResponse(pdf_report, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="{filename}"'.format(filename='albums.pdf')
        return response
    except ReportBroError as ex:
        return HttpResponseServerError('report error: ' + str(ex.error))
    except Exception as ex:
        return HttpResponseServerError('report exception: ' + str(ex))


def save(request):
    """Saves a music album in the db."""
    json_data = json.loads(request.body.decode('utf-8'))
    if not isinstance(json_data, dict):
        return HttpResponseBadRequest('invalid values')
    album = json_data.get('album')
    if not isinstance(album, dict):
        return HttpResponseBadRequest('invalid values')
    album_id = None
    if album.get('id'):
        try:
            album_id = int(album.get('id'))
        except (ValueError, TypeError):
            return HttpResponseBadRequest('invalid album id')

    values = dict(best_of_compilation=album.get('best_of_compilation'))
    rv = dict(errors=[])

    # perform some basic form validation
    if not album.get('name'):
        rv['errors'].append(dict(field='name', msg=str(_('error.the field must not be empty'))))
    else:
        values['name'] = album.get('name')
    if not album.get('artist'):
        rv['errors'].append(dict(field='artist', msg=str(_('error.the field must not be empty'))))
    else:
        values['artist'] = album.get('artist')
    if album.get('year'):
        try:
            values['year'] = int(album.get('year'))
            if values['year'] < 1900 or values['year'] > 2100:
                rv['errors'].append(dict(field='year', msg=str(_('error.the field must contain a valid year'))))
        except (ValueError, TypeError):
            rv['errors'].append(dict(field='year', msg=str(_('error.the field must contain a number'))))
    else:
        values['year'] = None

    if not rv['errors']:
        # no validation errors -> save album
        if album_id:
            Album.objects.filter(id=album_id).update(**values)
        else:
            Album.objects.create(**values)
    return JsonResponse(rv)


def get_albums(year=None):
    """Returns available albums from the database. Can be optionally filtered by year."""
    albums = Album.objects.all().order_by('name')
    if year is not None:
        albums = albums.filter(year=year).order_by('name')
    return albums.values()
