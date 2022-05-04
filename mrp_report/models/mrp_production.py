
from odoo import fields, models, _
from odoo.exceptions import UserError


class MrpReport(models.TransientModel):
    _name = "mrp.report"
    

    start = fields.Datetime(
        string="Fecha inicial"
    )
    end = fields.Datetime(
        string="Fecha final"
    )
   
    start1 = fields.Datetime(
        string="Fecha inicial"
    )
    end1 = fields.Datetime(
        string="Fecha final"
    )
    

   
  
 

    def generate(self):
        report = self.env.ref("mrp_report.mrp_summary_report")
        if self.start and self.end and (self.start1 or self.end1):
            raise UserError('Datos de seleccion erroneos')
        elif self.start1 and self.end1 and (self.start or self.end):
            raise UserError('Datos de seleccion erroneos')
        return report.report_action(self)

    def get_mrp_records(self):
        if self.start and self.end and not self.start1==True and not self.end1==True:
            obj = self.env["mrp.production"].search(
                [
                    
                    ("date_planned_start", ">=", self.start),
                    ("date_planned_start", "<=", self.end),
                    
                ]
            )
        elif self.start1 and self.end1 and not self.start==True and not self.end==True:
            obj= self.env["mrp.production"].search(
                [
                    ("date_planned_finished", ">=", self.start1),
                    ("date_planned_finished", "<=", self.end1),
                    
                ]
            )

        elif not self.start1==True and not self.end1==True and not self.start==True and not self.end==True:
            obj= self.env["mrp.production"].search(
                [
        
                    
                ]
            )
        
            


        return obj



