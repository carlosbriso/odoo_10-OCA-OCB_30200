# -*- coding: utf-8 -*-
# Copyright (C) 2009  Renato Lima - Akretion
# Copyright (C) 2011  Vinicius Dittgen - PROGE, Leonardo Santagada - PROGE
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import time
import base64
from openerp import models, fields, api, _
from openerp.exceptions import Warning as UserError


class L10nBrAccountNfeExportInvoice(models.TransientModel):
    """ Export fiscal eletronic file from invoice"""
    _name = 'l10n_br_account_product.nfe_export_invoice'
    _description = 'Export eletronic invoice for Emissor de NFe SEFAZ SP'

    def _default_file_type(self):
        company_id = self.env['res.company']._company_default_get(
            'l10n_br_account_product.nfe_export_invoice')
        return self.env['res.company'].browse(company_id).file_type

    def _default_nfe_environment(self):
        company_id = self.env['res.company']._company_default_get(
            'l10n_br_account_product.nfe_export_invoice')
        return self.env['res.company'].browse(company_id).nfe_environment

    def _default_export_folder(self):
        company_id = self.env['res.company']._company_default_get(
            'l10n_br_account_product.nfe_export_invoice')
        return self.env['res.company'].browse(company_id).export_folder

    def _default_sign_xml(self):
        company_id = self.env['res.company']._company_default_get(
            'l10n_br_account_product.nfe_export_invoice')
        return self.env['res.company'].browse(company_id).sign_xml

    name = fields.Char('Nome', size=255)
    file = fields.Binary('Arquivo', readonly=True)
    file_type = fields.Selection(
        selection=[
            (u'xml', 'XML'),
            (u'txt', ' TXT')
        ],
        string='Tipo do Arquivo',
        default=_default_file_type)
    state = fields.Selection(
        selection=[
            ('init', 'init'),
            ('done', 'done')
        ],
        string='state',
        readonly=True,
        default='init')
    nfe_environment = fields.Selection(
        selection=[
            ('1', u'Produ????o'),
            ('2', u'Homologa????o')
        ],
        string='Ambiente',
        default=_default_nfe_environment)
    sign_xml = fields.Boolean(
        string='Assinar XML',
        default=_default_sign_xml)
    nfe_export_result = fields.One2many(
        comodel_name='l10n_br_account_product.nfe_export_invoice_result',
        inverse_name='wizard_id',
        string='NFe Export Result')
    export_folder = fields.Boolean(
        string=u'Salvar na Pasta de Exporta????o',
        default=_default_export_folder)

    @api.multi
    def nfe_export(self):
        for data in self:
            active_ids = self._context.get('active_ids', [])

            if not active_ids:
                err_msg = (u'N??o existe nenhum documento fiscal para ser'
                           u' exportado!')
            export_inv_ids = []
            export_inv_numbers = []
            company_ids = []
            err_msg = ''

            for inv in self.env['account.invoice'].browse(active_ids):
                if inv.state not in ('sefaz_export'):
                    err_msg += (u"O Documento Fiscal %s n??o esta definida para"
                                u" ser exporta????o "
                                u"para a SEFAZ.\n") % inv.internal_number
                elif not inv.issuer == '0':
                    err_msg += (u"O Documento Fiscal %s ?? do tipo externa e "
                                u"n??o pode ser exportada para a "
                                u"receita.\n") % inv.internal_number
                else:
                    inv.write({
                        'nfe_export_date': False,
                        'nfe_access_key': False,
                        'nfe_status': False,
                        'nfe_date': False
                    })

                    message = "O Documento Fiscal %s foi \
                        exportado." % inv.internal_number
                    inv.log(message)
                    export_inv_ids.append(inv.id)
                    company_ids.append(inv.company_id.id)

                export_inv_numbers.append(inv.internal_number)

            if len(set(company_ids)) > 1:
                err_msg += (u'N??o ?? permitido exportar Documentos Fiscais de '
                            u'mais de uma empresa, por favor selecione '
                            u'Documentos Fiscais da mesma empresa.')

            if export_inv_ids:
                if len(export_inv_numbers) > 1:
                    name = 'nfes%s-%s.%s' % (
                        time.strftime('%d-%m-%Y'),
                        self.env['ir.sequence'].get('nfe.export'),
                        data.file_type)
                else:
                    name = 'nfe%s.%s' % (export_inv_numbers[0],
                                         data.file_type)

                mod_serializer = __import__(
                    ('openerp.addons.l10n_br_account_product'
                     '.sped.nfe.serializer.') +
                    data.file_type, globals(), locals(), data.file_type)

                func = getattr(mod_serializer, 'nfe_export')

                str_nfe_version = inv.nfe_version

                nfes = func(self._cr, self._uid, export_inv_ids,
                            data.nfe_environment, str_nfe_version,
                            self._context)

                for nfe in nfes:
                    nfe_file = nfe['nfe'].encode('utf8')

                data.write({
                    'file': base64.b64encode(nfe_file),
                    'state': 'done',
                    'name': name,
                })

            if err_msg:
                raise UserError(_('Error!'), _("'%s'") % _(err_msg, ))

            view_rec = self.env['ir.model.data'].get_object_reference(
                'l10n_br_account_product',
                'l10n_br_account_product_nfe_export_invoice_form')
            view_id = view_rec and view_rec[1] or False

            return {
                'view_type': 'form',
                'view_id': [view_id],
                'view_mode': 'form',
                'res_model': 'l10n_br_account_product.nfe_export_invoice',
                'res_id': data.id,
                'type': 'ir.actions.act_window',
                'target': 'new',
                'context': data.env.context,
            }


class L10nBrAccountNfeExportInvoiceResult(models.TransientModel):
    _name = 'l10n_br_account_product.nfe_export_invoice_result'

    wizard_id = fields.Many2one(
        comodel_name='l10n_br_account_product.nfe_export_invoice',
        string='Wizard ID',
        ondelete='cascade', select=True)
    document = fields.Char(string='Documento', size=255)
    status = fields.Selection(
        selection=[
            ('success', 'Sucesso'),
            ('error', 'Erro')
        ],
        string='Status')
    message = fields.Char(string='Mensagem', size=255)
