import csv
import itertools

from django.utils.text import slugify

from alumnus_backend.models import Organization, Member 

import xlrd
from xlrd.sheet import ctype_text


class ExcelParser():
  
    def __init__(self, f, organization):
        self.f = f 
        self.organization = organization
        self.wb = xlrd.open_workbook(self.f.name, file_contents=self.f.read())
        self.sheet = self.wb.sheet_by_index(0)

    def parse(self):
        for r in range(1, self.sheet.nrows):
            row = self.sheet.row(r)
            m = Member(email=row[0].value, firstname=row[1].value, lastname=row[2].value, organization=self.organization)

            if 3 < len(row):
                m.gender = row[3].value
            if 4 < len(row):
                m.graduation_year = int(row[4].value)
            if 5 < len(row):
                m.school = row[5].value
            if 6 < len(row):
                m.industry = row[6].value
            if 7 < len(row):
                m.company = row[7].value
            if 8 < len(row):
                m.current_state = row[8].value

            # set slug
            max_length = Member._meta.get_field('slug').max_length
            m.slug = orig = slugify(m.__unicode__())[:max_length]
            for x in itertools.count(1):
                if not Member.objects.filter(slug=m.slug).exists():
                    break
                # Truncate the original slug dynamically. Minus 1 for the hyphen.
                m.slug = "%s-%d" % (orig[:max_length - len(str(x)) - 1], x)

            m.save() 
