from odoo.tests.common import TransactionCase, tagged


@tagged("-at_install", "post_install")
class TestLoadSalaryStructure(TransactionCase):
    def setUp(self):
        super(TestLoadSalaryStructure, self).setUp()

        self.company1 = self.env["res.company"].create({"name": "Test Company 1"})
        self.env.user.company_ids |= self.company1

        self.structuretemp1 = self.env["hr.payroll.structure.template"].create(
            {
                "name": "Test Template Stucture 1",
                "code": "TS1",
            },
        )

        self.category1 = self.env["hr.salary.rule.category.template"].create(
            {
                "name": "Remunerations",
                "code": "BE_REMUN",
                "note": "Remunerations of all kinds",
            },
        )

        self.ruletemp1 = self.env["hr.salary.rule.template"].create(
            {
                "name": "Salary",
                "category_id": self.category1.id,
                "code": "BE_SALARY",
                "sequence": "100",
                "active": True,
                "appears_on_payslip": True,
                "note": "Monthly salary (wage) defined by the contract",
                "condition_select": "none",
                "amount_select": "code",
                "amount_python_compute": "result = contract.wage",
            },
        )

        self.structuretemp1.rule_ids |= self.ruletemp1

        self.company1.payroll_structure_template_ids |= self.structuretemp1

    def test_load_structure(self):

        # Load structure
        self.company1._load_update_all_salary_structure_company()

        # Check rule
        rule1 = self.env["hr.salary.rule"].search(
            [("company_id", "=", self.company1.id), ("code", "=", "BE_SALARY")]
        )
        self.assertTrue(rule1)
        self.assertEqual(rule1.name, "Salary")
        self.assertEqual(rule1.category_id.name, "Remunerations")
        self.assertEqual(rule1.code, "BE_SALARY")
        self.assertEqual(rule1.sequence, 100)
        self.assertTrue(rule1.active)
        self.assertTrue(rule1.appears_on_payslip),
        self.assertEqual(rule1.note, "Monthly salary (wage) defined by the contract")
        self.assertEqual(rule1.condition_select, "none")
        self.assertEqual(rule1.amount_select, "code")
        self.assertEqual(rule1.amount_python_compute, "result = contract.wage")

        # Check Structure
        struct1 = self.env["hr.payroll.structure"].search(
            [("company_id", "=", self.company1.id), ("code", "=", "TS1")]
        )
        self.assertEqual(struct1.name, "Test Template Stucture 1")
        self.assertIn(rule1.id, struct1.rule_ids.ids)

    def test_update_structure(self):
        # Modify structure, category, 1st rule and add a 2nd rule
        self.structuretemp1.name = "Test Template Stucture 1 (modified)"
        self.category1.name = "Remunerations (modified)"
        self.ruletemp1.name = "Salary (modified)"
        self.ruletemp1.amount_python_compute = "result = contract.wage * 10"
        self.ruletemp2 = self.env["hr.salary.rule.template"].create(
            {
                "name": "Allowance",
                "category_id": self.category1.id,
                "code": "BE_ALLOWANCE",
                "sequence": "110",
                "active": True,
                "appears_on_payslip": True,
                "note": "Some allowance",
                "condition_select": "none",
                "amount_select": "code",
                "amount_python_compute": "result = contract.wage / 100",
            },
        )
        self.structuretemp1.rule_ids |= self.ruletemp2

        # Load structure
        self.company1._load_update_all_salary_structure_company()

        # Check Structure
        struct1 = self.env["hr.payroll.structure"].search(
            [("company_id", "=", self.company1.id), ("code", "=", "TS1")]
        )
        self.assertEqual(struct1.name, "Test Template Stucture 1 (modified)")

        # Check rule 1
        rule1 = self.env["hr.salary.rule"].search(
            [("company_id", "=", self.company1.id), ("code", "=", "BE_SALARY")]
        )
        self.assertTrue(rule1)
        self.assertEqual(rule1.name, "Salary (modified)")
        self.assertEqual(rule1.category_id.name, "Remunerations (modified)")
        self.assertEqual(rule1.code, "BE_SALARY")
        self.assertEqual(rule1.sequence, 100)
        self.assertTrue(rule1.active)
        self.assertTrue(rule1.appears_on_payslip),
        self.assertEqual(rule1.note, "Monthly salary (wage) defined by the contract")
        self.assertEqual(rule1.condition_select, "none")
        self.assertEqual(rule1.amount_select, "code")
        self.assertEqual(rule1.amount_python_compute, "result = contract.wage * 10")
        # Check rule 2
        rule2 = self.env["hr.salary.rule"].search(
            [("company_id", "=", self.company1.id), ("code", "=", "BE_ALLOWANCE")]
        )
        self.assertTrue(rule2)
        self.assertEqual(rule2.name, "Allowance")
        self.assertEqual(rule2.category_id.name, "Remunerations (modified)")
        self.assertEqual(rule2.code, "BE_ALLOWANCE")
        self.assertEqual(rule2.sequence, 110)
        self.assertTrue(rule2.active)
        self.assertTrue(rule2.appears_on_payslip),
        self.assertEqual(rule2.note, "Some allowance")
        self.assertEqual(rule2.condition_select, "none")
        self.assertEqual(rule2.amount_select, "code")
        self.assertEqual(rule2.amount_python_compute, "result = contract.wage / 100")
