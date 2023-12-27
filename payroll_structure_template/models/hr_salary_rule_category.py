# Copyright 2024 TINCID (Régis Pirard)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class HrSalaryRuleCategory(models.Model):

    _inherit = "hr.salary.rule.category"

    _sql_constraints = [
        (
            "template_company_unique",
            "unique(template_id, company_id)",
            "A template category can only be deployed once in a company.",
        ),
    ]

    template_id = fields.Many2one(
        comodel_name="hr.salary.rule.category.template",
        string="Category Template",
        readonly=True,
        ondelete="cascade",
    )
