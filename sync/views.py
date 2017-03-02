from django.shortcuts import render
from models import Tembarun, Tembasteps, Tembavalues


def index(request):
    data = Tembarun.create_view_data()
    steps = data['step']
    values = data['value']

    return render(request, 'index.html', {'steps': steps, 'values': values})
