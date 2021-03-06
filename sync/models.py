from django.conf import settings
from django.db import models
from temba_client.v2 import TembaClient

client = TembaClient(settings.HOST, settings.KEY)


class Tembarun(models.Model):
    run_id = models.IntegerField(default=0)
    flow_name = models.CharField(max_length=100, null=True)
    responded = models.BooleanField(default=False)
    created_on = models.DateTimeField(null=True)
    modified_on = models.DateTimeField(null=True)

    @classmethod
    def get_runs(cls):
        runs = client.get_runs().all()
        added_runs = 0
        for r in runs:
            if not cls.runid_exists(r):
                runobj = cls.objects.create(run_id=r.id, flow_name=r.flow.name, responded=r.responded,
                                            created_on=r.created_on,
                                            modified_on=r.modified_on)
                Tembavalues.create_values(values=r.values, runid=runobj)
                Tembasteps.create_steps(path=r.path, runid=runobj)
                added_runs += 1
        return added_runs

    @classmethod
    def runid_exists(cls, r):
        return cls.objects.filter(run_id=r.id).exists()

    @classmethod
    def create_view_data(cls):
        runs = Tembarun.objects.all()
        complete_array_step = []
        complete_array_value = []
        for r in runs:
            steps = create_list(Tembasteps, r)
            complete_array_step.append(steps)
            values = create_list(Tembavalues, r)
            complete_array_value.append(values)

        return {'step': complete_array_step, 'value': complete_array_value}

    def __unicode__(self):
        return str(self.run_id)


class Tembaflows(models.Model):
    uuid = models.CharField(max_length=16)
    name = models.CharField(max_length=100)
    created_on = models.DateTimeField()
    runs_c = models.IntegerField(default=0)
    runs_i = models.IntegerField(default=0)
    runs_e = models.IntegerField(default=0)
    run_id = models.ForeignKey(Tembarun, null=True)

    @classmethod
    def get_flows(cls):
        flows = client.get_flows().all()
        for f in flows:
            cls.objects.create(uuid=f.uuid, name=f.name, created_on=f.created_on, runs_c=f.runs.completed,
                               runs_i=f.runs.interrupted, runs_e=f.runs.expired)


class Tembacontacts(models.Model):
    uuid = models.CharField(max_length=16)
    name = models.CharField(max_length=100, null=True)
    urn = models.CharField(max_length=100, null=True)

    @classmethod
    def get_contacts(cls):
        contacts = client.get_contacts().all()
        for c in contacts:
            cls.objects.create(uuid=c.uuid, name=c.name, urn=c.urn)


class Tembasteps(models.Model):
    node = models.CharField(max_length=100)
    time = models.DateTimeField()
    run_id = models.ForeignKey(Tembarun, null=True)

    @classmethod
    def create_steps(cls, path, runid):
        for p in path:
            cls.objects.create(node=p.node, time=p.time, run_id=runid)

    def __str__(self):
        return self.node


class Tembavalues(models.Model):
    value = models.CharField(max_length=20)
    run_id = models.ForeignKey(Tembarun, null=True)

    @classmethod
    def create_values(cls, values, runid):
        for v in values:
            cls.objects.create(value=v, run_id=runid)

    def __str__(self):
        return self.value


def create_list(obj, r):
    intermediate_array_step = []
    passed_object = obj.objects.filter(run_id=r)
    for o in passed_object:
        intermediate_array_step.append(o)
    return intermediate_array_step
