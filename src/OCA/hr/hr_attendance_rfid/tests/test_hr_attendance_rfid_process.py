# -*- coding: utf-8 -*-
# Copyright 2018 Eficent Business and IT Consulting Services, S.L.
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo.tests.common import TransactionCase


class TestHrAttendance(TransactionCase):

    def setUp(self):
        super(TestHrAttendance, self).setUp()
        self.employee_model = self.env['hr.employee']
        self.test_employee = self.browse_ref('hr.employee_al')
        self.rfid_card_code = '5b3f5'
        self.test_employee.rfid_card_code = self.rfid_card_code

    def test_valid_employee(self):
        """Valid employee"""
        res = self.employee_model.register_attendance(
            self.rfid_card_code)
        self.assertTrue('action' in res and res['action'] == 'check_in')
        self.assertTrue('logged' in res and res['logged'])
        self.assertTrue(
            'rfid_card_code' in res and
            res['rfid_card_code'] == self.rfid_card_code)
        res = self.employee_model.register_attendance(
            self.rfid_card_code)
        self.assertTrue('action' in res and res['action'] == 'check_out')
        self.assertTrue('logged' in res and res['logged'])

    def test_invalid_code(self):
        """Invalid employee"""
        invalid_code = '029238d'
        res = self.employee_model.register_attendance(invalid_code)
        self.assertTrue('action' in res and res['action'] == 'FALSE')
        self.assertTrue('logged' in res and not res['logged'])
        self.assertTrue(
            'rfid_card_code' in res and
            res['rfid_card_code'] == invalid_code)
