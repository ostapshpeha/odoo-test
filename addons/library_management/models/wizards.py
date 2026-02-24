from odoo import models, fields, api


class RentWizard(models.TransientModel):
    _name = "library.rent.wizard"
    partner_id = fields.Many2one("res.partner", string="Partner")

    def action_create(self):
        self.env["library.rent"].create(
            {"partner_id": self.partner_id.id, "is_available": False}
        )
