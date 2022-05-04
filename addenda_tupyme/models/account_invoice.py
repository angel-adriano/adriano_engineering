# -*- coding: utf-8 -*-

from odoo import fields, models, api 
#import odoo.addons.decimal_precision as dp
import os
import io
import logging
_logger = logging.getLogger(__name__)
from lxml import etree
from dateutil.parser import parse

data = """ <cfdi:Addenda>
<detallista:detallista xmlns:detallista="http://xml.tupyme.xyz/schema">
<detallista:orderIdentification>
<detallista:referenceIdentification type="">"%s"</detallista:referenceIdentification>
"""

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    #codigo_envio = fields.Many2one('addenda.chrysler.envio', string='Dirección de envío')
    #orden_compra = fields.Char(string='Orden de compra')
    #requicision_liberacion = fields.Char(string='Requisición de liberación')
    tupyme_addenda = fields.Boolean(string='Addenda', default=False)
    tupyme_agregado = fields.Boolean(string='Addenda agregada', default=False, readonly=True)
    text_addenda = fields.Char(string="Orden de compra:")

    @api.multi
    def add_addenda_tupyme(self):
        self.addenda_tupyme()
        return True

    @api.multi
    def addenda_tupyme(self):
        #tfd_namespace = {'tfd': 'http://www.sat.gob.mx/TimbreFiscalDigital'}
        for invoice in self:
            if invoice.xml_invoice_link and os.path.exists(invoice.xml_invoice_link):
                try:
                    new_data = data%(self.text_addenda)
                  
                    #secuencia = ""
                    #for line in self.invoice_line_ids: 
                    #    secuencia +="""
            #<part unidaDeMedida="%s" precioUnitario="%s" montoDeLinea="%s" cantidad="%s">
            #    <references releaseRequisicion="%s" ordenCompra="%s" ammendment="%s"/>
            #</part>"""%(line.product_id.uom_id.name, line.price_unit, line.price_subtotal, line.quantity, self.requicision_liberacion, self.orden_compra, line.line_item)
                    
                    new_data2 = """
                    </detallista:orderIdentification>
                    </detallista:detallista>
 </cfdi:Addenda>
</cfdi:Comprobante>
                    """

                    filedata = ''
                    # Read in the file
                    with io.open(invoice.xml_invoice_link, 'r', encoding='utf-8') as f:
                        filedata = f.read()
                    
                    # Replace the target string    
                    filedata = filedata.replace('</cfdi:Comprobante>', new_data)
                    #filedata2 = secuencia
                    filedata3 = new_data2
                    # Write the file out again
                    with io.open(invoice.xml_invoice_link, 'w', encoding='utf-8') as f:
                        f.write(filedata)
                        #f.write(filedata2)
                        f.write(filedata3)
                        invoice.tupyme_agregado = True
#                     f = open(invoice.xml_invoice_link,'a+')
#                     f.write(new_data)
#                     f.close()
                except Exception as e:
                    _logger.error(str(e))
                    pass