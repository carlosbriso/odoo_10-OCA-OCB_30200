# -*- coding: utf-8 -*-
################################################################
#    License, author and contributors information in:          #
#    __openerp__.py file at the root folder of this module.    #
################################################################

from openerp import models, api
import logging
_logger = logging.getLogger(__name__)


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.model
    def _prepare_picking(self):
        vals = super(PurchaseOrder, self)._prepare_picking()
        vals.update({
            'client_order_ref': self.partner_ref,
            'currency_id': self.currency_id.id if self.currency_id else False,
            'payment_term_id': self.payment_term_id.id
            if self.payment_term_id else False,
            'fiscal_position_id': self.fiscal_position_id.id
            if self.fiscal_position_id else False,
            'amount_untaxed': self.amount_untaxed,
            'amount_tax': self.amount_tax,
            'amount_total': self.amount_total,
        })
        return vals


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    @api.multi
    def _prepare_stock_moves(self, picking):
        """ Prepare the stock moves data for one order line. This function
        returns a list of dictionary ready to be used in stock.move's create()
        """
        res = super(PurchaseOrderLine, self)._prepare_stock_moves(picking)
        self.ensure_one()
        for tmp in res:
            if tmp.get('purchase_line_id', False) == self.id:
                tmp.update({
                    'move_price_unit': self.price_unit,
                    'price_subtotal': self.price_subtotal,
                    'tax_id': [(4, tax.id) for tax in self.taxes_id],
                })
        return res
