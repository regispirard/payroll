# Copyright 2024 TINCID (Régis Pirard)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, fields, models
from odoo.exceptions import UserError


class HrPayrollStructureTemplate(models.Model):

    _name = "hr.payroll.structure.template"
    _description = "Payroll structure template"

    name = fields.Char(required=True)
    code = fields.Char(string="Reference", required=True)
    note = fields.Text(string="Description")
    parent_id = fields.Many2one(
        comodel_name="hr.payroll.structure.template", string="Parent"
    )
    children_ids = fields.One2many(
        comodel_name="hr.payroll.structure.template",
        inverse_name="parent_id",
        string="Children",
    )
    rule_ids = fields.Many2many(
        comodel_name="hr.salary.rule.template",
        relation="hr_structure_salary_rule_template_rel",
        column1="struct_template_id",
        column2="rule_template_id",
        string="Salary Rules Templates",
    )
    payroll_structure_ids = fields.One2many(
        comodel_name="hr.payroll.structure",
        inverse_name="template_id",
        string="Salary Structures",
    )

    def _check_if_master_template_structure(self):
        # Verifies the template structure is a master structure
        if self.parent_id:
            raise UserError(_("Can only load main salary structure"))
        return

    def _get_structure_from_template_structure(self, template_structure, company_id):
        payroll_structure = template_structure.payroll_structure_ids.filtered_domain(
            [
                ("company_id", "=", company_id),
            ],
        )
        return payroll_structure

    def _get_all_template_structures(self):
        # List all template payroll structures linked to a master structure
        all_template_structures = self
        childrens = self.children_ids

        while childrens:
            all_template_structures += childrens
            new_childrens = self.env["hr.payroll.structure.template"]
            for child in childrens:
                new_childrens += child.children_ids
            childrens = new_childrens
        return all_template_structures.sorted(lambda g: g.id)

    def _get_all_template_rules(self, all_template_structures):
        # List all template rules linked to payroll structures
        all_template_rules = self.env["hr.salary.rule.template"]
        for structure in all_template_structures:
            for rule in structure.rule_ids:
                if rule not in all_template_rules:
                    all_template_rules += structure.rule_ids
        return all_template_rules.sorted(lambda g: g.id)

    def _get_all_template_categories(self, all_template_rules):
        # List all categories linked to payroll structures
        all_template_categories = self.env["hr.salary.rule.category.template"]
        for rule in all_template_rules:
            if rule.category_id not in all_template_categories:
                all_template_categories += rule.category_id
        return all_template_categories.sorted(lambda g: g.id)

    def _get_all_registers(self, all_template_rules):
        # List all contribution registers
        all_template_registers = self.env["hr.contribution.register.template"]
        for rule in all_template_rules:
            if rule.register_id not in all_template_registers:
                all_template_registers += rule.register_id
        return all_template_registers.sorted(lambda g: g.id)

    def _get_all_rule_inputs(self, all_template_rules):
        # List all inputs
        all_template_inputs = self.env["hr.rule.input.template"]
        for rule in all_template_rules:
            for rule_input in rule.input_ids:
                if rule_input not in all_template_inputs:
                    all_template_inputs += input
        return all_template_inputs.sorted(lambda g: g.id)

    def _create_structure_from_templates(self, all_template_structures, company_id):
        # Create or update payroll structures
        for template_structure in all_template_structures:

            # check if structure already exists for this company
            payroll_structure = (
                template_structure._get_structure_from_template_structure(
                    template_structure, company_id
                )
            )

            # Find parent record if any
            if template_structure.parent_id:
                parent_id = (
                    template_structure.parent_id.payroll_structure_ids.filtered_domain(
                        [
                            ("company_id", "=", company_id),
                        ]
                    ).id
                )
                if not parent_id:
                    raise UserError(_("Cannot find parent salary structure"))
            else:
                parent_id = False

            structure_data = {
                "name": template_structure.name,
                "code": template_structure.code,
                "note": template_structure.note,
                "template_id": template_structure.id,
                "parent_id": parent_id,
                "company_id": company_id,
            }

            # create or update salary structure
            if not payroll_structure:
                payroll_structure.create(structure_data)
            else:
                payroll_structure.write(structure_data)

    def _create_categories_from_templates(self, all_template_categories, company_id):
        # Create or update categories
        for template_category in all_template_categories:

            # check if category already exists for this company
            category = template_category.hr_salary_rule_category_ids.filtered_domain(
                [
                    ("company_id", "=", company_id),
                ],
            )

            # Find parent record if any
            if template_category.parent_id:
                category_ids = template_category.parent_id.hr_salary_rule_category_ids
                parent_id = category_ids.filtered_domain(
                    [
                        ("company_id", "=", company_id),
                    ]
                ).id
                if not parent_id:
                    raise UserError(_("Cannot find parent category"))
            else:
                parent_id = False

            category_data = {
                "name": template_category.name,
                "code": template_category.code,
                "note": template_category.note,
                "template_id": template_category.id,
                "parent_id": parent_id,
                "company_id": company_id,
            }

            # create or update category
            if not category:
                category.create(category_data)
            else:
                category.write(category_data)

    def _create_rules_from_templates(self, all_template_rules, company_id):
        # Create or update rules
        for template_rule in all_template_rules:

            # check if rule already exists for this company
            rule = template_rule.hr_salary_rule_ids.filtered_domain(
                [
                    ("company_id", "=", company_id),
                ],
            )

            # Find category
            if template_rule.category_id:
                category_ids = template_rule.category_id.hr_salary_rule_category_ids
                category_id = category_ids.filtered_domain(
                    [
                        ("company_id", "=", company_id),
                    ]
                ).id
                if not category_id:
                    raise UserError(_("Cannot find rule category"))
            else:
                category_id = False

            # Find parent record if any
            if template_rule.parent_rule_id:
                parent_rule_id = (
                    template_rule.parent_rule_id.hr_salary_rule_ids.filtered_domain(
                        [
                            ("company_id", "=", company_id),
                        ]
                    ).id
                )
                if not parent_rule_id:
                    raise UserError(_("Cannot find parent rule"))
            else:
                parent_rule_id = False

            # Find structures linked to the rule (M2M)
            template_structures = self.search([("rule_ids", "=", template_rule.id)])

            rule_data = {
                "name": template_rule.name,
                "code": template_rule.code,
                "sequence": template_rule.sequence,
                "quantity": template_rule.quantity,
                "category_id": category_id,
                "active": template_rule.active,
                "appears_on_payslip": template_rule.appears_on_payslip,
                "parent_rule_id": parent_rule_id,
                "condition_select": template_rule.condition_select,
                "condition_range": template_rule.condition_range,
                "condition_python": template_rule.condition_python,
                "condition_range_min": template_rule.condition_range_min,
                "condition_range_max": template_rule.condition_range_max,
                "amount_select": template_rule.amount_select,
                "amount_fix": template_rule.amount_fix,
                "amount_percentage": template_rule.amount_percentage,
                "amount_python_compute": template_rule.amount_python_compute,
                "amount_percentage_base": template_rule.amount_percentage_base,
                "note": template_rule.note,
                "template_id": template_rule.id,
                "company_id": company_id,
            }

            # create or update rule
            if not rule:
                # create
                rule = rule.create(rule_data)
            else:
                rule.write(rule_data)

                # link rule with structure (M2M)
                for template_structure in template_structures:
                    structure = (
                        template_structure._get_structure_from_template_structure(
                            template_structure, company_id
                        )
                    )
                    structure.rule_ids = rule

    # Create or update contribution registers
    def _create_registers_from_templates(self, all_template_registers, company_id):
        for template_register in all_template_registers:

            # check if register already exists for this company
            register = template_register.hr_contribution_register_ids.filtered_domain(
                [
                    ("company_id", "=", company_id),
                ],
            )

            register_data = {
                "partner_id": template_register.partner_id,
                "name": template_register.name,
                "note": template_register.note,
                "template_id": template_register.id,
                "company_id": company_id,
            }

            # create or update registers
            if not register:
                register.create(register_data)
            else:
                register.write(register_data)

    def _create_inputs_from_templates(self, all_template_inputs, company_id):
        # Create or update rule imputs
        for template_input in all_template_inputs:

            # check if input already exists for this company
            rule_input = template_input.hr_rule_input_ids

            # Find rule linked to input
            if template_input.input_id:
                input_rule_id = (
                    template_input.input_id.hr_salary_rule_ids.filtered_domain(
                        [
                            ("company_id", "=", company_id),
                        ]
                    ).id
                )
                if not input_rule_id:
                    raise UserError(_("Cannot find rule for input"))
            else:
                input_rule_id = False

            input_data = {
                "name": template_input.name,
                "code": template_input.code,
                "input_id": input_rule_id,
                "template_id": template_input.id,
            }

            # create or update inputs
            if not rule_input:
                rule_input.create(input_data)
            else:
                rule_input.write(input_data)

    def _load_update_salary_structure(self, company_id):

        for template_structure in self:

            template_structure._check_if_master_template_structure()

            all_template_structures = template_structure._get_all_template_structures()
            template_structure._create_structure_from_templates(
                all_template_structures, company_id
            )

            all_template_rules = template_structure._get_all_template_rules(
                all_template_structures
            )
            all_template_categories = template_structure._get_all_template_categories(
                all_template_rules
            )
            template_structure._create_categories_from_templates(
                all_template_categories, company_id
            )

            all_template_registers = template_structure._get_all_registers(
                all_template_rules
            )
            template_structure._create_registers_from_templates(
                all_template_registers, company_id
            )

            all_template_inputs = template_structure._get_all_rule_inputs(
                all_template_rules
            )
            template_structure._create_inputs_from_templates(
                all_template_inputs, company_id
            )

            template_structure._create_rules_from_templates(
                all_template_rules, company_id
            )
