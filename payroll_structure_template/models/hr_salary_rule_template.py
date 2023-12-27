# Copyright 2024 TINCID (Régis Pirard)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class HrSalaryRuleTemplate(models.Model):

    _name = "hr.salary.rule.template"
    _description = "Salary rule template"

    name = fields.Char(
        required=True,
        translate=True,
    )
    code = fields.Char()
    sequence = fields.Integer(
        required=True,
        index=True,
        default=5,
    )
    quantity = fields.Char(
        default="1.0",
    )
    category_id = fields.Many2one(
        comodel_name="hr.salary.rule.category.template",
        string="Category",
    )
    active = fields.Boolean(
        default=True,
    )
    appears_on_payslip = fields.Boolean(
        string="Appears on Payslip",
        default=True,
    )
    parent_rule_id = fields.Many2one(
        comodel_name="hr.salary.rule.template",
        string="Parent Salary Rule",
        index=True,
    )
    condition_select = fields.Selection(
        [
            ("none", "Always True"),
            ("range", "Range"),
            ("python", "Python Expression"),
        ],
        string="Condition Based on",
        required=True,
        default="none",
    )
    condition_range = fields.Char(
        string="Range Based on",
    )
    condition_python = fields.Text(
        string="Python Condition",
        required=True,
        default="""
            # Available variables:
            #-------------------------------
            # payslip: hr.payslip object
            # payslips: object containing payslips (browsable)
            # employee: hr.employee object
            # contract: hr.contract object
            # rules: object containing the rules code (previously computed)
            # categories: object containing the computed salary rule categories
            #    (sum of amount of all rules belonging to that category).
            # worked_days: object containing the computed worked days.
            # inputs: object containing the computed inputs.
            # payroll: object containing miscellaneous values related to payroll
            # current_contract: object with values calculated from the current contract
            # result_rules: object with a dict of qty, rate, amount an total of calculated rules
            # tools: object that contain libraries and tools that can be used in calculations

            # Available compute variables:
            #-------------------------------
            # result: returned value have to be set in the variable 'result'

            # Example:
            #-------------------------------
            # result = worked_days.WORK0 and worked_days.WORK0.number_of_days > 0

            """,
    )
    condition_range_min = fields.Float(
        string="Minimum Range",
    )
    condition_range_max = fields.Float(
        string="Maximum Range",
    )
    amount_select = fields.Selection(
        [
            ("percentage", "Percentage (%)"),
            ("fix", "Fixed Amount"),
            ("code", "Python Code"),
        ],
        string="Amount Type",
        index=True,
        required=True,
    )
    amount_fix = fields.Float(string="Fixed Amount", digits="Payroll")
    amount_percentage = fields.Float(
        string="Percentage (%)",
        digits="Payroll Rate",
    )
    amount_python_compute = fields.Text(
        string="Python Code",
    )
    amount_percentage_base = fields.Char(string="Percentage based on")
    child_ids = fields.One2many(
        comodel_name="hr.salary.rule.template",
        inverse_name="parent_rule_id",
        string="Child Salary Rule Template",
    )
    register_id = fields.Many2one(
        comodel_name="hr.contribution.register.template",
        string="Contribution Register Template",
    )
    input_ids = fields.One2many(
        comodel_name="hr.rule.input.template",
        inverse_name="input_id",
        string="Inputs Template",
    )
    note = fields.Text(string="Description")
    hr_salary_rule_ids = fields.One2many(
        comodel_name="hr.salary.rule",
        inverse_name="template_id",
        string="Salary Rules",
    )
