# Copyright 2024 TINCID (Régis Pirard)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class HrContributionRegister(models.Model):
    _inherit = "hr.contribution.register"

    _sql_constraints = [
        (
            "template_company_unique",
            "unique(template_id, company_id)",
            "A template contribution register can only be deployed once in a company.",
        ),
    ]

    template_id = fields.Many2one(
        comodel_name="hr.contribution.register.template",
        string="Contribution Register Template",
        readonly=True,
        ondelete="cascade",
    )
