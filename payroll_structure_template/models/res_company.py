# Copyright 2024 TINCID (Régis Pirard)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    payroll_structure_template_ids = fields.Many2many(
        comodel_name="hr.payroll.structure.template",
        string="Payroll Structure Template",
        domain=[("parent_id", "=", False)],
        help="Select payroll structures template to be loaded",
    )

    def _load_update_salary_structure(self):
        for company in self:
            for template in company.payroll_structure_template_ids:
                template._load_update_salary_structure(company.id)
