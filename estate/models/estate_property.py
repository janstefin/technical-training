from odoo import _, fields, models, api, Command
from odoo.tools.float_utils import float_is_zero, float_compare
from odoo.exceptions import UserError, ValidationError


class EstateProperty(models.Model):
    _name = "estate_property"
    _description = "Estate Property model"

    def action_sell_property(self):
        vals_list=[]
        for property in self:
            vals = {
                "partner_id": property.buyer_id.id,
                "move_type": "out_invoice",
                "journal_id": 1,
                "invoice_line_ids":[
                    Command.create({
                        "name": property.name,
                        "quantity": 1,
                        "price_unit": 0.06*property.selling_price
                    }),
                    Command.create({
                        "name": "Administration Fees",
                        "quantity": 1,
                        "price_unit": 100
                    })
                ]
            }
            vals_list.append(vals)
        self.env["account.move"].create(vals_list)
        return super().action_sell_property()

    name = fields.Char(required=True)

    state = fields.Selection(
        [("new", "New"), ("offer_received", "Offer Received"),
         ("sold", "Sold"), ("canceled", "Canceled"),
         ("offer_accepted", "Offer accepted")])
    description = fields.Text()
    postcode = fields.Integer()
    date = fields.Date()
    expected_price = fields.Float()
    best_offer = fields.Float()
    selling_price = fields.Float()

    living_area = fields.Float()
    facades = fields.Integer()
    garden_area = fields.Float()
    total_area = fields.Float(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price")

    garden = fields.Boolean()
    bedrooms = fields.Integer()
    garden_orientation = fields.Selection(
        [("south", "South"), ("north", "North")])
    last_seen = fields.Datetime("Last Seen", default=fields.Datetime.now)

    property_type_id = fields.Many2one("estate_property.types")
    tag_ids = fields.Many2many("estate_property.tags")
    salesperson_id = fields.Many2one("res.users",
                                     default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", copy=False)
    offer_ids = fields.One2many("estate_property.offer", "property_id")

    _sql_constraints = [
        ("unique_name", "UNIQUE(name)", "The name should be unique!"),
        ("check_selling_price", "CHECK(selling_price >= 0)",
         "The selling price must be positive")
    ]

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        for property in self:
            if (not float_is_zero(property.selling_price,
                                  precision_rounding=0.01) and float_compare(
                property.selling_price, 0.9 * property.expected_price,
                precision_rounding=0.01) < 0):
                raise ValidationError(
                    _("The selling price should not be lower then 90% of the "
                      "expected price"))

    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.garden_area + property.living_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for property in self:
            if property.offer_ids:
                property.best_price = max(property.offer_ids.mapped("price"))
            else:
                property.best_price = 0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = self.garden_orientation = False

    @api.ondelete(at_uninstall=False)
    def _unlink_if_new_canceled(self):
        for property in self:
            if property.state in ("new", "canceled"):
                raise UserError(_("Only new or canceled property can be "
                                  "deleted"))




    def action_sell_property(self):
        for property in self:
            if property.state == "canceled":
                raise UserError(_("Canceled properties cannot be sold"))
            property.state = "sold"

    def action_cancel_property(self):
        self.state = "canceled"
