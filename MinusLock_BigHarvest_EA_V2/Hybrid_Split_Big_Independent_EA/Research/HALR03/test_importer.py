from datetime import timezone
import importlib
from io import StringIO
import unittest

q=importlib.import_module("07_CSV_IMPORTER")


class DataTests(unittest.TestCase):
    def test_mt5_separators_and_quality(self):
        s=StringIO("<DATE>;<TIME>;<BID>;<ASK>;<LAST>;<VOLUME>;<FLAGS>\n"
                   "2024.01.01;14:00:00.000;1,10000;1,10025;0;0;2\n"
                   "2024.01.01;14:00:00.000;1,10000;1,10025;0;0;2\n"
                   "2024.01.01;14:00:01.000;1,10050;1,10040;0;0;2\n"
                   "2024.01.01;13:59:59.000;1,10000;1,10005;0;0;2\n"
                   "2024.01.01;14:00:03.000;1,100001;1,10010;0;0;2\n")
        a,ticks=q.inspect(s,timezone.utc,separator=";")
        self.assertEqual((a["duplicate_record"],a["time_reversal"],a["crossed"],a["off_tick_size"]),
                         (1,1,1,1))
        self.assertEqual(ticks[0][2:],(110000,110025))

    def test_last_cannot_replace_bid_ask(self):
        with self.assertRaises(ValueError):
            q.inspect(StringIO("<DATE>,<TIME>,<LAST>\n"),timezone.utc)
