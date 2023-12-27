# Copyright 2024 TINCID (Régis Pirard)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class HrRuleInput(models.Model):
    _inherit = "hr.rule.input"

    _sql_constraints = [
        (
            "template_unique",
            "unique(template_id)",
            "A template rule can only be deployed once in a company.",
        ),
    ]

    template_id = fields.Many2one(
        comodel_name="hr.rule.input.template",
        string="Rule Input Template",
        readonly=True,
        ondelete="cascade",
    )
