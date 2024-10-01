from odoo import fields, models, api

class EstatePropertyOffer(models.Model):
    _name = "estate_property.offer"
    _description = "Estate Property Offer"

    price = fields.Float()
    status = fields.Selection([("accepted", "Accepted"), ("refused", "Refused")])
    property_id = fields.Many2one("estate_property", required=True)
    partner_id = fields.Many2one("res.partner", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline")

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for estate in self:
            create_date = estate.create_date or fields.Date.today()
            estate.date_deadline = fields.Date.add(create_date, days=estate.validity)
