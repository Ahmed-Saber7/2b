# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    letter_guarantee_id = fields.Many2one(comodel_name="letter.guarantee", string="Letters Of Guarantee",
                                          required=False, )
