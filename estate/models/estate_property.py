from odoo import fields, models

class EstateProperty(models.Model):
    _name = "estate_property"
    _description = "Estate Property model"

    name = fields.Char(required=True, default="Unknown")
    state = fields.Selection([("new", "New"), ("offer_received", "Offer Received"), ("sold", "Sold")])
    description = fields.Text()
    postcode = fields.Integer()
    date = fields.Date()
    expected_price = fields.Float(readonly=True, copy=True)
    garden = fields.Boolean()
    bedrooms = fields.Integer()
    garden_orientation = fields.Selection([("south", "South"), ("north", "North")])
    last_seen = fields.Datetime("Last Seen", default=fields.Datetime.now)

