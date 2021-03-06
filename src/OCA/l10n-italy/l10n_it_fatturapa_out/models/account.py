# -*- coding: utf-8 -*-
# Copyright 2014 Davide Corio
# Copyright 2016 Lorenzo Battistini - Agile Business Group
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models
from odoo.exceptions import UserError
from odoo.tools.translate import _


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    fatturapa_attachment_out_id = fields.Many2one(
        'fatturapa.attachment.out', 'FatturaPA Export File',
        readonly=True)

    def preventive_checks(self):
        for line in self.invoice_line_ids:
            if '\n' in line.name:
                raise UserError(_(
                    "Invoice line [%s] must not contain new line character"
                ) % line.name)
