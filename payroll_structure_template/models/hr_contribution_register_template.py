# Copyright 2024 TINCID (Régis Pirard)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class HrContributionRegisterTemplate(models.Model):
    _name = "hr.contribution.register.template"
    _description = "Contribution Register"

    partner_id = fields.Many2one("res.partner", string="Partner")
    name = fields.Char(required=True)
    note = fields.Text(string="Description")

    hr_contribution_register_ids = fields.One2many(
        comodel_name="hr.contribution.register",
        inverse_name="template_id",
        string="Contribution Registers",
    )
