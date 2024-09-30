from odoo import fields, models

class EstatePropertyOffer(models.Model):
    _name = "estate_property.offer"
    _description = "Estate Property Offer"

    price = fields.Float()
    status = fields.Selection([("accepted", "Accepted"), ("refused", "Refused")])
    property_id = fields.Many2one("estate_property", required=True)
    partner_id = fields.Many2one("res.partner", required=True)
