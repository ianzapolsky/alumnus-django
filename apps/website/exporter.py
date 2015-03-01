import csv
import itertools

from django.utils.text import slugify

from alumnus_backend.models import Organization, Member 

import xlrd
import xlwt

class ExcelExporter():
  
    def __init__(self, organization):
        self.org = organization

    def export(self):
        wb = xlwt.Workbook()
        sheet = wb.add_sheet('members')

        # formatting
        headerstyle = xlwt.XFStyle()
        font = xlwt.Font()
        font.bold = True
        font.height = 240
        headerstyle.font = font

        datastyle = xlwt.XFStyle()
        dfont = xlwt.Font()
        dfont.height = 240
        datastyle.font = dfont

        sheet.write(0, 0, 'Email (*Required)', style=headerstyle)
        sheet.write(0, 1, 'First Name (*Required)', style=headerstyle)
        sheet.write(0, 2, 'Last Name (*Required)', style=headerstyle)
        sheet.write(0, 3, 'Gender', style=headerstyle)
        sheet.write(0, 4, 'Grad. Year', style=headerstyle)
        sheet.write(0, 5, 'School', style=headerstyle)
        sheet.write(0, 6, 'Industry', style=headerstyle)
        sheet.write(0, 7, 'Company', style=headerstyle)
        sheet.write(0, 8, 'Current State', style=headerstyle)

        for index, member in enumerate(self.org.get_members()):
          
            sheet.write(index + 1, 0, member.email, style=datastyle)
            sheet.write(index + 1, 1, member.firstname, style=datastyle)
            sheet.write(index + 1, 2, member.lastname, style=datastyle)
            sheet.write(index + 1, 3, member.gender, style=datastyle)
            sheet.write(index + 1, 4, member.graduation_year, style=datastyle)
            sheet.write(index + 1, 5, member.school, style=datastyle)
            sheet.write(index + 1, 6, member.industry, style=datastyle)
            sheet.write(index + 1, 7, member.company, style=datastyle)
            sheet.write(index + 1, 8, member.current_state, style=datastyle)

        return wb
