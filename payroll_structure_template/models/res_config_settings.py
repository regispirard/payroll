# Copyright 2024 TINCID (Régis Pirard)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    payroll_structure_template_ids = fields.Many2many(
        comodel_name="hr.payroll.structure.template",
        string="Payroll Structure Template",
        domain=[("parent_id", "=", False)],
        related="company_id.payroll_structure_template_ids",
        readonly=False,
        help="Select payroll structures template to be loaded",
    )

    def load_update_salary_structure(self):
        for setting in self:
            company = setting.company_id
            company._load_update_salary_structure()
