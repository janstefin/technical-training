from odoo import fields, models

class EstateProprety(models.Model):
    _name = "estate_proprety"
    _description = "estate propret description"

    name = fields.Char()