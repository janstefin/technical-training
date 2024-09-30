from odoo import fields, models

class EstateProperty(models.Model):
    _name = "estate_property"
    _description = "Estate Property model"

    name = fields.Char(required=True)
    state = fields.Selection([("new", "New"), ("offer_received", "Offer Received"), ("sold", "Sold")])
    description = fields.Text()
    postcode = fields.Integer()
    date = fields.Date()
    expected_price = fields.Float(readonly=True, copy=False)
    garden = fields.Boolean()
    bedrooms = fields.Integer()
    garden_orientation = fields.Selection([("south", "South"), ("north", "North")])
    last_seen = fields.Datetime("Last Seen", default=fields.Datetime.now)
    salesperson_id = fields.Many2one("res.users", default = lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", copy=False)
    offer_ids = fields.One2many("estate.property.offer", "property_id")

