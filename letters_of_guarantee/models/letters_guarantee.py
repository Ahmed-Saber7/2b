# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class LettersOfGuarantee(models.Model):
    _name = 'letter.guarantee'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    state = fields.Selection([
        ('draft', 'Draft'),
        ('to_be_approved', 'To Be Approved'),
        ('approve', 'Approve'),
        ('reject', 'Reject'),
        ('cancel', 'Cancel')], required=True, default='draft')

    name = fields.Char(string="Name", required=False, default="Draft")
    bank = fields.Char(string="Bank", required=False, )
    letter_guarantee_date = fields.Date(string="Letter Guarantee Date", required=False, default=fields.Date.today())
    letter_guarantee_number_old = fields.Char(string="Letter Guarantee Old Num.", required=False, )
    letter_guarantee_number_new = fields.Char(string="Letter Guarantee New Num.", required=False, )
    letter_guarantee_type = fields.Selection(string="Letter Guarantee Type",
                                             selection=[('elementary', 'Elementary'), ('final', 'Final'),
                                                        ('advance_payment', 'Advance Payment'), ], required=False, )
    organization_id = fields.Many2one(comodel_name="res.partner", string="Organization", required=False, )
    status = fields.Selection(string="Status", selection=[('running', 'Running'), ('finished', 'Finished'), ],
                              required=False, )
    department_id = fields.Many2one(comodel_name="hr.department", string="Department", required=False, )
    expiry_date = fields.Date(string="Expiry Date", required=False, )
    letter_guarantee_value = fields.Float(string="Letter Guarantee Value", required=False, )
    marge = fields.Float(string="Marge", required=False, )
    marge_value = fields.Float(string="", required=False, compute="get_marge_value")
    current_user = fields.Many2one('res.users', 'Current User', default=lambda self: self.env.user)

    # WorkFlow
    def submit_for_approval(self):
        self.state = 'to_be_approved'

    def cancel(self):
        self.state = 'cancel'

    def reset_to_draft(self):
        self.state = 'draft'

    def approve(self):
        self.state = 'approve'

    def reject(self):
        self.state = 'reject'

    # CREATE Sequence
    @api.model
    def create(self, vals):
        vals['name'] = (self.env['ir.sequence'].next_by_code('letter.guarantee')) or 'New'
        return super(LettersOfGuarantee, self).create(vals)

    # func to get marge value
    @api.depends('letter_guarantee_value', 'marge')
    def get_marge_value(self):
        for rec in self:
            if rec.letter_guarantee_value and rec.marge:
                rec.marge_value = rec.letter_guarantee_value * rec.marge / 100
            else:
                rec.marge_value = 0.0

    # func to prevent delete a Letter which is not in draft or cancelled state
    def unlink(self):
        for rec in self:
            if rec.state not in ('draft', 'cancel'):
                raise UserError(
                    'You cannot delete a Letter which is not in draft or cancelled state')
        return super(LettersOfGuarantee, self).unlink()
