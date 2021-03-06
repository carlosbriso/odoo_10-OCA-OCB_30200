# -*- coding: utf-8 -*-
# Copyright 2017-2018 Akretion (http://www.akretion.com)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    fr_chorus_invoice_format = fields.Selection(selection_add=[
        ('xml_cii', 'CII 16B XML'),
        ('pdf_factur-x', 'Factur-X PDF'),
        ])
