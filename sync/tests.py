from django.test import TestCase
from datetime import datetime
from models import Tembarun, Tembasteps, Tembavalues


class TestRun(TestCase):

    def test_get_runs(self):
        group_count = Tembarun.objects.count()
        tamba_count = Tembarun.get_runs()

        self.assertEquals(Tembarun.objects.count(), group_count + tamba_count)

    def test_run_exists(self):
            class G(object):
                def __init__(self, run_id=None, flow_name=None, responded=None, created_on=None, modified_on=None):
                    self.id = run_id
                    self.flow_name = flow_name
                    self.responded = responded
                    self.created_on = created_on
                    self.modified_on = modified_on

            rapidpro_mock_run = G(run_id=100, flow_name='pmct', responded=True)
            self.assertEquals(Tembarun.runid_exists(rapidpro_mock_run), False)
            Tembarun.objects.create(run_id=100, flow_name='pmct', responded=True)
            self.assertEquals(Tembarun.runid_exists(rapidpro_mock_run), True)


# from django.test import TestCase
# from sync.models import Group, Run
#
#
# class TestGroup(TestCase):
#     def test_add_groups(self):
#         group_count = Group.objects.count()
#         added_groups = Group.add_groups()
#         self.assertEquals(Group.objects.count(), group_count + added_groups)
#
#     def test_group_exists(self):
#         class G(object):
#             def __init__(self, name=None, uuid=None, query=None, count=None):
#                 self.name = name
#                 self.uuid = uuid
#                 self.query = query
#                 self.count = count
#
#         rapidpro_mock_group = G(name='Test Group', uuid='random number', query=None, count=4)
#         self.assertEquals(Group.group_exists(rapidpro_mock_group), False)
#         Group.objects.create(name='Test Group', uuid='random number', query=None, count=4)
#         self.assertEquals(Group.group_exists(rapidpro_mock_group), True)
#
#
# class TestRun(TestCase):
#     def test_add_runs(self):
#         run_count = Run.objects.count()
#         added_runs = Run.add_runs()
# self.assertEquals(Run.objects.count(), run_count + added_runs)