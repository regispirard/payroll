To use this module:

#. Add Payroll Structure Template as a dependency in your payroll localization module.

#. Define salary structure templates in the localization module's data files.

Example : 

  <!-- Categories templates -->

  <record id="l10n_country_category1" model="hr.salary.rule.category.template">
    <field name="name">Category1</field>
    <field name="code">Category</field>
    <field name="note">Description of category1</field>
  </record>

  <!-- Salary Rules Template -->

  <record id="l10n_country_rule1" model="hr.salary.rule.template">
    <field name="name">Rule1</field>
    <field name="category_id" ref="l10n_country_category1" />
    <field name="code">RULE1</field>
    <field name="sequence" eval="100" />
    <field name="active">True</field>
    <field name="appears_on_payslip">True</field>
    <field name="note">Description for rule1</field>
    <field name="condition_select">none</field>
    <field name="amount_select">code</field>
    <field name="amount_python_compute">result = contract.wage</field>
  </record>

#. Deploy and customize the templates across your companies as required.
This can be achieved trough Odoo UI, but also trough data files : 

<!-- Salary Structure templates -->

  <record id="structure_l10n_country_struct1" model="hr.payroll.structure.template">
    <field name="code">STRUCT1</field>
    <field name="name">Name of Salary Structure 1</field>
    <field
            name="rule_ids"
            eval="[
            (4, ref('l10n_country_rule1')),
            ]"
        />
  </record>

