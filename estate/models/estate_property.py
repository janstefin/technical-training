from odoo import fields, models

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property model"

    name = fields.Char(required=True)
    description = fields.Text()
    date = fields.Date()
    garden_orientation = fields.Selection([("north", "North"), ("south, South"), ("east", "East")])