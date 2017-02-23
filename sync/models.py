from django.conf import settings
from django.db import models
from temba_client.v2 import TembaClient

client = TembaClient(settings.HOST, settings.KEY)


class Tembarun(models.Model):
    run_id = models.IntegerField(default=0)
    responded = models.BooleanField(default=False)
    created_on = models.DateTimeField(null=True)
    modified_on = models.DateTimeField(null=True)

    @classmethod
    def get_runs(cls):
        runs = client.get_runs().all()
        number_of_runs = 0
        for r in runs:
            if not cls.runid_exists(r):
                cls.objects.create(run_id=r.id, responded=r.responded, created_on=r.created_on,
                                   modified_on=r.modified_on)
                k = Tembarun.objects.get(run_id=r.id)
                Tembavalues.get_values(values=r.values, runid=k)
                Tembasteps.get_steps(path=r.path, runid=k)
                number_of_runs += 1
        return number_of_runs

    @classmethod
    def runid_exists(cls, r):
        return cls.objects.filter(run_id=r.id).exists()

    def __unicode__(self):
        return self.run_id


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
    def get_steps(cls, path, runid):
        for p in path:
            cls.objects.create(node=p.node, time=p.time, run_id=runid)

    def __str__(self):
        return self.node


class Tembavalues(models.Model):
    value = models.CharField(max_length=20)
    run_id = models.ForeignKey(Tembarun, null=True)

    @classmethod
    def get_values(cls, values, runid):
        for v in values:
            cls.objects.create(value=v, run_id=runid)

    def __str__(self):
        return self.value
