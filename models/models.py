# -*- coding: utf-8 -*-


import binascii
import tempfile

import certifi
import urllib3
import base64
import csv
import io
import re
import xlrd

from odoo import models, fields, api
from odoo.exceptions import Warning, UserError

class import_mdl(models.Model):
    _name = 'import_mdl.import_mdl'

    file = fields.Binary('File to import', required=True)
    file_type = fields.Selection([('csv', 'CSV'), ('xls', 'XLS')], string="File Type", default='csv')

    res_model = fields.Selection([('explo.explo','Explo'), ('invst.invest','Invest')],string='Model')



    def import_file(self):
        table = 'NULL'
        importable_fields={
            'champs1': 'code', 
            'champs2': 'ne pas import', 
            'champs3': 'montant',
            'champs4':'ne pas import',
            'champs5':'ne pas import'
            }
        list_col=[]
        for i in importable_fields:
            if(importable_fields[i]!='ne pas import'):
                list_col.append(importable_fields[i])
        list_col.extend(['create_uid','create_date', 'write_uid','write_date'])
        All_col=[]
        for i in importable_fields:
            All_col.append(importable_fields[i])


        if self.res_model == 'explo.explo':
            table = 'explo_explo'
        if self.res_model == 'invest.invest':
            table = 'invest_invest'
        if self.file_type == 'csv':

            try:
                file = base64.b64decode(self.file)
                data = io.StringIO(file.decode("utf-8"))
                data.seek(0)
                file_reader = []
                csv_reader = csv.reader(data, delimiter=',')
                file_reader.extend(csv_reader)

            except:
                raise Warning(_("File is not Valid!"))

            fields = list(map(str, file_reader[0]))
            for fr in range(len(file_reader)):
                line = list(map(str, file_reader[fr]))
                vals = dict(zip(list_col, line))
                if vals:
                    if fr == 0:
                        continue
                    else:
                        if line[2] == '' or check_value(line[2])==False :
                            line[2] = '0.0'
                        if "'" in line[1] :
                            line[1] = line[1].replace("'","_")
                        for i in range(0,len(All_col)):
                            if All_col[i]=="ne pas import":
                                continue
                            else:
                                vals.update({All_col[i]:line[i]})
                        vals.update({'create_uid': self.env.user.id,
                                    'create_date': self.create_date,
                                    'write_uid': self.env.user.id,
                                    'write_date': self.write_date,
                                })
                        tuple1=()
                        tuple2=()
                        cnt=0
                        for i in list_col:
                            tuple1=tuple1+(i,)
                            cnt+=1
                            tuple2=tuple2+(vals[i],)
                        col="%s" %(tuple1,) 
                        col=col.replace("'","")
                        valeur="%s" %(tuple2,) 
                        if(cnt==1): 
                            col=col.replace(",","")
                            valeur=valeur.replace(",","").replace("\"","'")

                        self.env.cr.execute("insert into "+table + col +"values"+valeur)
                        self.env.cr.commit()  
      
        elif self.file_type == 'xls':
            try:
                fp = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
                fp.write(binascii.a2b_base64(self.file))
                fp.seek(0)
                vals = {}
                workbook = xlrd.open_workbook(fp.name)
                sheet = workbook.sheet_by_index(0)

            except:
                raise Warning(_("File not Valid"))
            fields = map(lambda row: row.value.encode('utf-8'), sheet.row(0))


            for row_no in range(sheet.nrows):
                val = {}
                if row_no <= 0:
                    continue
                else:

                    line = list(
                        map(lambda row: isinstance(row.value, bytes) and row.value.encode('utf-8') or str(row.value),
                            sheet.row(row_no)))
                    if line[2] == '' or check_value(line[2])==False :
                        line[2] = '0.0'
                    if "'" in line[1] :
                        line[1] = line[1].replace("'","_")
                    
                    for i in range(0,len(All_col)):
                        if All_col[i]=="ne pas import":
                            continue
                        else:
                            vals.update({All_col[i]:line[i]})
                    vals.update({'create_uid': self.env.user.id,
                                'create_date': self.create_date,
                                'write_uid': self.env.user.id,
                                'write_date': self.write_date,
                            })
                    tuple1=()
                    tuple2=()
                    cnt=0
                    for i in list_col:
                        tuple1=tuple1+(i,)
                        cnt+=1
                        tuple2=tuple2+(vals[i],)
                    col="%s" %(tuple1,) 
                    col=col.replace("'","")
                    valeur="%s" %(tuple2,) 
                    if(cnt==1): 
                        col=col.replace(",","")
                        valeur=valeur.replace(",","").replace("\"","'")
                    self.env.cr.execute("insert into "+table + col +"values"+valeur)
                    self.env.cr.commit()             
        else:
            raise UserError(_("Please select xls or csv format!"))

def check_value(s):
    try:
        float(s)
        return True
    except ValueError:
        return False



