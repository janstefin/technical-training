from odoo import fields, models

class EstatePropertyTypes(models.Model):
    _name = "estate_property.types"
    _description = "Estate Property Types"

    name_type = fields.Char(required=True)