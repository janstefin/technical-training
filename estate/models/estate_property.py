from odoo import fields, models

class EstateProperty(models.Model):
    _name = "estate_property"
    _description = "Estate Property model"

    name = fields.Char(required=True)
    description = fields.Text()
    date = fields.Date()
    expected_price = fields.Float()
    garden = fields.Boolean()
    bedrooms = fields.Integer()
    garden_orientation = fields.Selection([("south", "South"), ("north", "North")])
