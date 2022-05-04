from operator import invert
from odoo import fields, models, api, _
from odoo.exceptions import UserError, Warning


class SockMove(models.Model):
    _inherit="mrp.workorder"

    material=fields.One2many(related="production_id.move_raw_ids")

    @api.multi
    def button_start(self):
        vals= super(SockMove, self).button_start()
        for line in self:
            p_sequence= line.sequence -1
            object_order=self.env['mrp.workorder'].search(
                [('production_id', '=', line.production_id.id),('sequence','=',p_sequence)])
            if line.sequence > 1 and object_order.qty_produced < line.qty_producing:
                raise UserError(_('No se han producido unidades suficientes para esta operacion, por favor revise las operaciones anteriores.'))
        for line1 in self:
            for record in line1.material:
                if line1.operation_id == record.operation_id and record.reserved_availability < record.product_uom_qty:
                        raise UserError(_('No hay cantidades reservadas para esta operacion, favor de comprobar la disponibilidad de componentes.'))

        return vals

    @api.multi
    def record_production(self):
        vals= super(SockMove, self).record_production()
        for line in self:
            p_sequence = line.sequence - 1
            object_order = self.env['mrp.workorder'].search(
                [('production_id', '=', line.production_id.id), ('sequence', '=', p_sequence)])
            if line.sequence > 1 and object_order.qty_produced < line.qty_produced:
                raise UserError(_('No se han producido unidades suficientes para esta operacion, por favor revise las operaciones anteriores.'))
        return vals