from django.shortcuts import render
from models import Tembarun, Tembasteps, Tembavalues


def index(request):
    runs = Tembarun.objects.all()
    ir_step = []
    ir_value = []
    ic_step = []
    ic_value = []
    for r in runs:
        steps = Tembasteps.objects.filter(run_id=r)
        for s in steps:
            ir_step.append(s)
            ic_step.append(ir_step)
            ir_step = []
        values = Tembavalues.objects.filter(run_id=r)
        for v in values:
            ir_value.append(v)
            ic_value.append(ir_value)
            ir_value = []

    return render(request, 'index.html', {'steps': ic_step, 'values': ic_value})
