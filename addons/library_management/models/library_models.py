from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Book(models.Model):
    _name = "library.book"
    _description = "Book model"
    name = fields.Char(string="Book Name", required=True)
    author = fields.Char(string="Author")
    published_date = fields.Date(string="Publish Date")
    is_available = fields.Boolean(string="Is Available")


class Rent(models.Model):
    _name = "library.rent"
    _description = "Renting book model"
    partner_id = fields.Many2one("res.partner", string="Partner")
    book_id = fields.Many2one("library.book", string="Book")
    rent_date = fields.Date(string="Rent Date", auto_now_add=True)
    return_date = fields.Date(string="Return Date", blank=True, null=True)


@api.constrains("rent_book_again")
def _check_if_book_returned(self):
    """
    Checking that book can't be rent two times in straight, if it isn't returned
    :param self:
    :return:
    """
    for record in self:
        if not record.return_date:
            raise ValidationError("Book is not returned. You can't rent it now")