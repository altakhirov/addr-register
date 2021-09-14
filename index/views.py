from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, ListView

from openpyxl import load_workbook

from index.models import FilesToParse
from index.parser import check_first_row
from index.tasks import xlsx_parser


class ParseView(TemplateView):
    template_name = 'parse.html'

    def post(self, request):
        file = request.FILES.get('file')
        with_flats = request.POST.get("with_flats")
        if with_flats == 'y':
            with_flats = True
        elif with_flats == 'n':
            with_flats = False
        else:
            messages.error(request, "Вы не выбрали тип домов!")
            return HttpResponseRedirect(self.request.path_info)
        filename = file.name
        if filename.endswith('.xlsx'):
            FilesToParse.objects.create(
                file=request.FILES.get('file'),
                with_flats=with_flats
            )
            return HttpResponseRedirect('/ru/files')
        else:
            messages.success(request, "Файл должен быть в формате .xlsx!")
        return HttpResponseRedirect(self.request.path_info)


class FileListView(ListView):
    template_name = 'file_list.html'
    queryset = FilesToParse.objects.all().order_by('-pk')
    context_object_name = 'file_list'

    # def get(self, request, *args, **kwargs):
    #     context = self.get_context_data(**kwargs)
    #     return self.render_to_response(context)
    #
    # def get_queryset(self):
    #     return FilesToParse.objects.all().order_by('-pk')


@login_required
def parse_into_db(request, pk):
    file = get_object_or_404(FilesToParse, pk=pk)
    wb_obj = load_workbook(filename=file.file, read_only=True)
    sheet_obj = wb_obj.active
    check = check_first_row(sheet_obj)
    wb_obj.close()
    if check:
        messages.error(request, check)
        return HttpResponseRedirect('/ru/files')
    else:
        xlsx_parser.apply_async((pk,))
        file.in_progress = True
        file.save()
    return HttpResponseRedirect('/ru/files')


@login_required
def delete_file(request, pk):
    file = get_object_or_404(FilesToParse, pk=pk)
    file.delete()
    return HttpResponseRedirect('/ru/files')


class IndexView(TemplateView):
    template_name = 'index.html'
