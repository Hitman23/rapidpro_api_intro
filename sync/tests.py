from django.test import TestCase
from models import Tembarun, Tembasteps, Tembavalues


class Testrun(TestCase):

    def test_get_runs(self):
        tamba_count = Tembarun.get_runs()
        group_count = Tembarun.objects.count()
        self.assertEquals(group_count, tamba_count)
