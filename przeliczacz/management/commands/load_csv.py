from django.core.management.base import BaseCommand, CommandError
from przeliczacz.models import Product
import re


class Command(BaseCommand):
    help = 'Load custom products from a CSV file.'
    path = './przeliczacz.csv'

    def handle(self, *args, **options):

        try:
            file = open(self.path)
        except IOError as e:
            raise CommandError("I/O error({0}): {1}".format(e.errno, e.strerror))

        lines = file.readlines()

        for line in lines:
            line_segments = line.split(",")
            if len(line_segments) >= 5:
                name = line_segments[1]
                if name:
                    ww = line_segments[2]
                    wbt = line_segments[3]
                    if ww and wbt:
                        cal = line_segments[4]
                        try:
                            ww = float(ww)
                            wbt = float(wbt)
                        except ValueError:
                            continue
                        try:
                            cal = float(cal)
                        except ValueError:
                            cal = None

                        i = Product()
                        i.ww = ww
                        i.wbt = wbt
                        i.name = name
                        i.cal = cal
                        m = re.search(r'[\d.]+ *g', name)
                        try:
                            unit_weight = float(m.group().split('g')[0])
                            i.unit_weight = unit_weight
                        except:
                            pass
                        i.save()