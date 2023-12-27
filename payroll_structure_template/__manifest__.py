# Copyright 2024 TINCID (Régis Pirard)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Payroll Structure Template",
    "author": "TINCID (Régis PIRARD), Odoo Community Association (OCA)",
    "summary": """
        Simplify the deployment and maintenance of standardized payroll structures
        across multiple companies and databases. Payroll Structure Template is an
        CA Payroll extension that enables you to create, maintain, and deploy
        standardized payroll structures for any company.
        With multi-company support, it ensures that only relevant companies apply
        the localization-specific payroll rules. Ideal for adapting quickly to
        legislative changes while preserving compliance.
    """,
    "website": "https://github.com/OCA/payroll",
    "category": "Payroll",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "depends": [
        "payroll",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/res_config_settings_views.xml",
    ],
    "application": False,
}
