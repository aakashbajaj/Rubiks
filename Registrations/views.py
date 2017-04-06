from django.shortcuts import render
from django.views.generic import CreateView
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required

from models import *

import csv
import xlsxwriter, StringIO
from time import strftime, gmtime
# Create your views here.

@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(CreateView):
	model = Participant
	fields = ['name', 'idno', 'phone', 'can_solve', 'institute', 'psrn', 'dept']
	template_name = 'index.html'
	success_url = '.'
	def get_context_data(self, *args, **kwargs):
		context = super(RegisterView, self).get_context_data(*args, **kwargs)
		context["number"] = Participant.objects.all().count() + 2000
		return context
	def get(self, request, *args, **kwargs):
		if request.GET.get('count', False):
			return JsonResponse({'count' : Participant.objects.all().count() + 2000}) 
		return super(RegisterView, self).get(request, *args, **kwargs)
	def post(self, request, *args, **kwargs):
		if request.POST['institute'] == "BITS" and Participant.objects.filter(idno=request.POST['idno'], institute="BITS"):
			return JsonResponse({'error' : 1})
		else:
			res = super(RegisterView, self).post(request, *args, **kwargs)
			return JsonResponse({'success' : 1})

@staff_member_required
def ParticipantExcel(request, **kwargs):
	entries = Participant.objects.filter(id__gte=1435).order_by('idno')
	output = StringIO.StringIO()
	workbook = xlsxwriter.Workbook(output)
	worksheet = workbook.add_worksheet('new-spreadsheet')
	date_format = workbook.add_format({'num_format': 'mmmm d yyyy'})
	worksheet.write(0, 0, "Generated:")
	generated = strftime("%d-%m-%Y %H:%M:%S UTC", gmtime())
	worksheet.write(0, 1, generated)

	worksheet.write(1, 0, "ID NO")
	worksheet.write(1, 1, "Name")
	worksheet.write(1, 2, "Institute")
	worksheet.write(1, 3, "Phone")
	worksheet.write(1, 4, "Can Solve?")

	for i, p in enumerate(entries):
		worksheet.write(i+2, 0, p.idno)
		worksheet.write(i+2, 1, p.name)
		worksheet.write(i+2, 2, p.institute)
		worksheet.write(i+2, 3, p.phone)
		worksheet.write(i+2, 4, p.can_solve)

	workbook.close()
	filename = 'Participants.xlsx'
	output.seek(0)
	response = HttpResponse(output.read(), content_type="application/ms-excel")
	response['Content-Disposition'] = 'attachment; filename=%s' % filename
	return response

@staff_member_required
def HostelExcel(request, hostel):
	entries = BITSians.objects.filter(hostel__iexact=hostel).order_by('room')
	output = StringIO.StringIO()
	writer = csv.writer(output)
	writer.writerow(["Mame", "ID No.", "Hostel", "Room", "Registered"])
	for b in entries:
		writer.writerow([b.name, b.idno, b.hostel, b.room, b.registered])
	filename = 'Participants.csv'
	output.seek(0)
	response = HttpResponse(output.read(), content_type="application/ms-excel")
	response['Content-Disposition'] = 'attachment; filename=%s' % filename
	return response
