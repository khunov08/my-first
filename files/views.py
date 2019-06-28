from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse, HttpResponseBadRequest

from .file_storage import FileStorage, _create_file_object_from_json, _create_file_object_from_post

# Create your views here.


def index(request):
    """Выдаёт список файлов"""
    files = FileStorage().list()

    if request.is_ajax():
        return JsonResponse(files, safe=False)
    else:
        return render(request, 'files/index.html', {'files': files})


def del_file(request):
    """Удаляет файл из директории"""
    if not request.method == 'POST':
        return HttpResponseBadRequest()

    name = request.POST.get('filename')
    if not name:
        raise Http404()

    result = FileStorage().delete(name)

    if request.is_ajax():
        return JsonResponse({'result': 'Ok'})
    else:
        return HttpResponseRedirect(reverse_lazy('files:del_after'))


def del_file_after(request):
    return render(request, 'files/del-after.html')


def add_file(request):
    """Добавляет новый файл в директорию"""
    if not request.method == 'POST':
        return HttpResponseBadRequest()

    if request.FILES:
        file_object = _create_file_object_from_post(request.FILES['file'])
    # elif request.is_ajax() :
    #     file_object = _create_file_object_from_json(request.body)
    else:
        return HttpResponseBadRequest()

    name, content = file_object

    result = FileStorage().save(name, content)

    if request.is_ajax():
        return JsonResponse({'result': 'Ok'})
    else:
        return HttpResponseRedirect(reverse_lazy('files:add_after'))


def add_file_after(request):
    return render(request, 'files/add-after.html')

# def show_file(request, name):
#     """Возвращает страницу с отдельным файлом"""
#     if not name:
#         return Http404
#
#     if request.is_ajax():
#         file_content = FileStorage().get_file_content(name)
#         return JsonResponse(request, {'file': file_content})
#     else:
#         file_url = FileStorage().get_file_url(name)
#         return render(request, 'files/view.html', {'file_url': file_url})
