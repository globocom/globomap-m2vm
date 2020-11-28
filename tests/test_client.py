from unittest import TestCase, mock
from m2vm.client import GmapClient


class ClientTest(TestCase):

    def setUp(self):
        self.gmap_client = GmapClient()

