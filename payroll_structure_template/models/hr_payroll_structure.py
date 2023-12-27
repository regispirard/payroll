# Copyright 2024 TINCID (Régis Pirard)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class HrPayrollStructure(models.Model):

    _inherit = "hr.payroll.structure"
    _description = "Payroll structure template"

    _sql_constraints = [
        (
            "template_company_unique",
            "unique(template_id, company_id)",
            "A payroll template can only be deployed once in a company.",
        ),
    ]

    template_id = fields.Many2one(
        comodel_name="hr.payroll.structure.template",
        string="Salary Structure Template",
        readonly=True,
        ondelete="cascade",
    )
