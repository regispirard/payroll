# Copyright 2024 TINCID (Régis Pirard)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class HrSalaryRuleCategoryTemplate(models.Model):

    _name = "hr.salary.rule.category.template"
    _description = "Salary rule category template"

    name = fields.Char(
        required=True,
        translate=True,
    )
    code = fields.Char(
        required=True,
    )
    parent_id = fields.Many2one(
        comodel_name="hr.salary.rule.category.template",
        string="Parent",
    )
    children_ids = fields.One2many(
        comodel_name="hr.salary.rule.category.template",
        inverse_name="parent_id",
        string="Children",
    )
    note = fields.Text(string="Description")
    hr_salary_rule_category_ids = fields.One2many(
        comodel_name="hr.salary.rule.category",
        inverse_name="template_id",
        string="Salary Categories",
    )
