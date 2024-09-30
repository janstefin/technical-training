from odoo import fields, models

class EstateProperty(models.Model):
    _name = "estate_property"
    _description = "Estate Property model"

    name = fields.Char(required=True)
    state = fields.Selection([("new", "New"), ("offer_received", "Offer Received"), ("sold", "Sold")])
    description = fields.Text()
    postcode = fields.Integer()
    date = fields.Date()
    expected_price = fields.Float()
    best_offer = fields.Float()
    selling_price = fields.Float()

    living_area = fields.Float()
    facades = fields.Integer()
    garden_area = fields.Float()
    total_area=fields.Float()


    garden = fields.Boolean()
    bedrooms = fields.Integer()
    garden_orientation = fields.Selection([("south", "South"), ("north", "North")])
    last_seen = fields.Datetime("Last Seen", default=fields.Datetime.now)

    property_type_id = fields.Many2one("estate_property.types")
    tag_ids = fields.Many2many("estate_property.tags")
    salesperson_id = fields.Many2one("res.users", default = lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", copy=False)
    offer_ids = fields.One2many("estate_property.offer", "property_id")

