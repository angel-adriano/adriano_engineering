# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################
from re import sub
from logging import getLogger

from odoo import api,models


class Feed(models.Model):
	_inherit = 'wk.feed'


	def match_invoice_partner(self,partner_id):
		# NOTE: ambos objs (partner_id, self) tienen rfc como property
		address_lines = [
			(partner_id.street, self.invoice_street),
			(partner_id.street2, self.invoice_street2),
			(partner_id.zip, self.invoice_zip),
			(partner_id.city, self.invoice_city),
			(partner_id.state_id.code, self.invoice_state_id),
			(partner_id.country_id.code, self.invoice_country_id),
		]
		for local_address, remote_address in address_lines:
			if not self.match_address(local_address, remote_address):
				return False
		return True

	def match_shipping_partner(self,partner_id):
		address_lines = [
			(partner_id.street, self.shipping_street),
			(partner_id.street2, self.shipping_street2),
			(partner_id.zip, self.shipping_zip),
			(partner_id.city, self.shipping_city),
			(partner_id.state_id.code, self.shipping_state_id),
			(partner_id.country_id.code, self.shipping_country_id),
		]
		for local_address, remote_address in address_lines:
			if not self.match_address(local_address, remote_address):
				return False
		return True

	def match_address(self, local_address, remote_address):
		if local_address:
			local_address = sub(r'\s+', '', local_address).lower()
		else:
			local_address = ''
		if remote_address:
			remote_address = sub(r'\s+', '', remote_address).lower()
		else:
			remote_address = ''
		return local_address==remote_address

	@api.model
	def create_partner_invoice_id(self,partner_id,channel_id,invoice_partner_id=None):
		# NOTE: funcion llamada en lugar de feeds.create_partner_invoice_id
		if self.channel != 'shopify':
			return super().create_partner_invoice_id(partner_id,channel_id,invoice_partner_id)
		store_id = invoice_partner_id
		invoice_partner_id = partner_id.child_ids.filtered(lambda x: self.match_invoice_partner(x))
		if invoice_partner_id:
			invoice_partner_id = invoice_partner_id[0]
			invoice_partner_id.type = 'invoice'
		else:
			if store_id is False:
				raise Exception('Invoice address data missing')
			self.env['import.operation'].create(
				{'channel_id':channel_id.id}
			).import_with_filter(
				object      = 'res.partner',
				filter_type = 'id',
				object_id   = store_id,
			)
			if not channel_id.auto_evaluate_feed:
				self.env['partner.feed'].search(
					[
						('state','=','draft'),
						'|',
						('store_id','=',store_id),
						('parent_id','=',store_id)
					],
				).with_context(get_mapping_ids=True).import_items()
			invoice_partner_id = partner_id.child_ids.filtered(lambda x: self.match_invoice_partner(x))
			# NOTE: aqui se cambia el delivery por invoice
			# NOTE: filtra los id's creados y si uno hace match con la direccion de billing (shopi)
			# 		quiere decir que esa direccion debe ser invoice (odoo)
			if invoice_partner_id:
				invoice_partner_id = invoice_partner_id[0]
				invoice_partner_id.type = 'invoice'
			else:
				_error = ('Neither can find order invoice address match in '
						  'local partner, nor in remote customer.\n')
				_error += "\tstore_info(channel={}, customer_id={}) ".format(channel_id.channel,store_id)
				if partner_id:
					_error += "res.partner(id={}, name='{}')".format(partner_id.id,partner_id.name)
				raise Exception(_error)
		return invoice_partner_id

	@api.model
	def create_partner_shipping_id(self,partner_id,channel_id,shipping_partner_id=None):
		# NOTE: funcion llamada en lugar de feeds.create_partner_invoice_id
		if self.channel != 'shopify':
			return super().create_partner_shipping_id(partner_id,channel_id,shipping_partner_id)
		store_id = shipping_partner_id
		shipping_partner_id = partner_id.child_ids.filtered(lambda x: self.match_shipping_partner(x))
		if shipping_partner_id:
			shipping_partner_id = shipping_partner_id[0]
			shipping_partner_id.type = 'delivery'
		else:
			if store_id is False:
				raise Exception('Invoice address data missing')
			self.env['import.operation'].create(
				{'channel_id':channel_id.id}
			).import_with_filter(
				object      = 'res.partner',
				filter_type = 'id',
				object_id   = store_id,
			)
			if not channel_id.auto_evaluate_feed:
				self.env['partner.feed'].search(
					[
						('state','=','draft'),
						'|',
						('store_id','=',store_id),
						('parent_id','=',store_id)
					],
				).with_context(get_mapping_ids=True).import_items()
			shipping_partner_id = partner_id.child_ids.filtered(lambda x: self.match_shipping_partner(x))
			if shipping_partner_id:
				shipping_partner_id = shipping_partner_id[0]
				shipping_partner_id.type = 'delivery'
			else:
				_error = ('Neither can find order shipping address match in '
						  'local partner, nor in remote customer.\n')
				_error += "\tstore_info(channel={}, customer_id={}) ".format(channel_id.channel,store_id)
				if partner_id:
					_error += "res.partner(id={}, name='{}')".format(partner_id.id,partner_id.name)
				raise Exception(_error)
		return shipping_partner_id
