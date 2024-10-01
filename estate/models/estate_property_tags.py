from odoo import fields, models

class EstatePropertyTags(models.Model):
    _name = "estate_property.tags"
    _description = "Estate Property Tags"

    name = fields.Char(required=True)
    color = fields.Integer()