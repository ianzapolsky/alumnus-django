import csv
import itertools

from django.utils.text import slugify

from alumnus_backend.models import Organization, Member 

import xlrd
from xlrd.sheet import ctype_text


class ExcelParser():
  
    def __init__(self, f):
        self.f = f 
        self.wb = xlrd.open_workbook(self.f.name, file_contents=self.f.read())
        self.sheet = self.wb.sheet_by_index(0)

    def parse(self, organization):
        for r in range(1, self.sheet.nrows):
            row = self.sheet.row(r)
  
            # Check that Email, First name, and Last name are present
            if row[0].value == '' or row[1].value == '' or row[2].value == '':
                continue

            m = Member(email=row[0].value, firstname=row[1].value, lastname=row[2].value, organization=organization)

            if row[3].value != '':
                m.gender = row[3].value
            if row[4].value != '':
                m.graduation_year = int(row[4].value)
            if row[5].value != '':
                m.school = row[5].value
            if row[6].value != '':
                m.industry = row[6].value
            if row[7].value != '':
                m.company = row[7].value
            if row[8].value != '':
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

    def validate(self):
        row = self.sheet.row(0)
        if row[0].value != 'Email (*Required)':
            return False 
        if row[1].value != 'First name (*Required)':
            return False 
        if row[2].value != 'Last name (*Required)':
            return False 
        if row[3].value != 'Gender':
            return False 
        if row[4].value != 'Grad. Year':
            return False 
        if row[5].value != 'School':
            return False 
        if row[6].value != 'Industry':
            return False 
        if row[7].value != 'Company':
            return False 
        if row[8].value != 'Current State':
            return False 
        return True

