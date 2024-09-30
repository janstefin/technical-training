from odoo import fields, models

class EstatePropertyTags(models.Model):
    _name = "estate_property.tags"
    _description = "Estate Property Tags"

    name_tag = fields.Char(required=True)