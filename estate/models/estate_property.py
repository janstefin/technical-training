from odoo import fields, models

class EstateProperty(models.Model):
    _name = "estate_property"
    _description = "Estate Property model"

    name = fields.Char(required=True)
    description = fields.Text()
    date = fields.Date()
