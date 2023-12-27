# Copyright 2024 TINCID (Régis Pirard)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class HrRuleInputTemplate(models.Model):
    _name = "hr.rule.input.template"
    _description = "Salary Rule Input Template"

    name = fields.Char(string="Description", required=True)
    code = fields.Char(
        required=True, help="The code that can be used in the salary rules"
    )
    input_id = fields.Many2one(
        "hr.salary.rule.template", string="Salary Rule Template Input", required=True
    )
    hr_rule_input_ids = fields.One2many(
        comodel_name="hr.rule.input",
        inverse_name="template_id",
        string="Salary Rule Inputs",
    )
