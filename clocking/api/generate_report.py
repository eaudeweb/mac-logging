from datetime import timedelta
import xlsxwriter

from instance.settings import REPORT_DIR, REPORT_FILE


def generate_report(entries):
    workbook = xlsxwriter.Workbook(REPORT_DIR + REPORT_FILE)
    bold = workbook.add_format({'bold': 1})
    worksheets = []
    for entry in entries:
        day = entry['day'].strftime('%B_%d_%Y')
        worksheet = workbook.add_worksheet(name=day)
        worksheet.write('A1', 'Name', bold)
        worksheet.write('B1', 'Device', bold)
        worksheet.write('C1', 'Time In', bold)
        worksheet.write('D1', 'Time Out', bold)
        worksheets.append(worksheet)
    date_format = workbook.add_format({'num_format': 'hh:mm'})
    i = 0
    for entry in entries:
        row = 1
        col = 0
        for entry_by_day in entry['entries_by_day']:
            name = entry_by_day.mac.person.first_name + ' ' + entry_by_day.mac.person.last_name
            device = entry_by_day.mac.device.value
            start_date = entry_by_day.startdate
            end_date = entry_by_day.startdate + timedelta(hours=8)
            worksheets[i].write_string(row, col, name)
            worksheets[i].write_string(row, col + 1, device)
            worksheets[i].write_datetime(row, col + 2, start_date, date_format)
            worksheets[i].write_datetime(row, col + 3, end_date, date_format)
            row += 1
        worksheets[i].set_column('A:A', 20)
        worksheets[i].set_column('B:B', 15)
        worksheets[i].set_column('C:C', 15)
        worksheets[i].set_column('D:D', 15)
        i += 1

    workbook.close()
