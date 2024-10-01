from odoo import fields, models, api, _
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate_property.offer"
    _description = "Estate Property Offer"

    price = fields.Float()
    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")])
    property_id = fields.Many2one("estate_property", required=True)
    partner_id = fields.Many2one("res.partner", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline",
                                inverse="_inverse_date_deadline")

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for estate in self:
            create_date = estate.create_date or fields.Date.today()
            estate.date_deadline = fields.Date.add(create_date,
                                                   days=estate.validity)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property = self.env["estate_property"].browse(vals["property_id"])
            if property.offer_ids:
                min_price = min(property.offer_ids.mapped("price"))
                if (vals["price"] <= min_price):
                    raise UserError(
                        _("The offer must be higer then %s") % min_price)
        return super().create(vals_list)


    def _inverse_date_deadline(self):
        for estate in self:
            create_date = estate.create_date or fields.Date.today()
            estate.validity = (estate.date_deadline - fields.Date.to_date(
                create_date)).days

    def action_accept_offer(self):
        self.status = "accepted"
        for offer in self:
            self.property_id.selling_price = self.price

    def action_refuse_offer(self):
        self.status = "refused"
