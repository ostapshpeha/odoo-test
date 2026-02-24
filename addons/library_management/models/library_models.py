# coding: utf-8
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Book(models.Model):
    """Репрезентація однієї книги в каталозі.

    Кожна книга має два стани:
        - available (is_available=True)  — можна орендувати
        - unavailable (is_available=False) — не можна орендувати
    """

    _name = "library.book"
    _description = "Library Book"

    name = fields.Char(string="Book Name", required=True)

    # Опціонально, тому що старі книги можуть мати невідомих авторів
    author = fields.Char(string="Author")

    # Офіційна дата публікації
    published_date = fields.Date(string="Publication Date")

    # Прапорець - доступність
    # По замовчуванню - True, як тільки книгу додають на стелаж
    is_available = fields.Boolean(string="Is Available", default=True)

    def action_open_rent_wizard(self):
        """Відкриваємо візарда 'RentBook' в діалоговому вікні.

        Візард автозаповнює всі поля книги, то ж бібліотекар лише вибирає орендаря.

        Returns:
            dict: An Odoo action descriptor that opens library.rent.wizard
                  in a modal dialog ('target': 'new').
        """
        return {
            "name": "Publish book",  # Назва діалогового вікна
            "type": "ir.actions.act_window",
            "res_model": "library.rent.wizard",
            "view_mode": "form",
            "target": "new",  # Вікдрити як popup/modal
            # Авто заповнення візардом ід книги, то ж бібліотекарю не треба шукати,
            # чи вона відкрита до оренди.
            "context": {"default_book_id": self.id},
        }


class Rent(models.Model):
    """Репрезентація однієї оренди, орендар - книга.

    Правила:
        - rent_date автоматично виставляється на сьогоднішню дату.
        - return_date заповнюється коли книга повернута; до цього поле порожнє (False/None),
        сигнал що оренда активна.
        - Книга не може бути орендована двома клієнтами зразу
    """

    _name = "library.rent"
    _description = "Book Rental"

    # Орендар
    # Many2one to res.partner — це вбудована модель клієнта в Odoo
    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Reader",
        required=True,
    )

    # Книга для оренди
    book_id = fields.Many2one(
        comodel_name="library.book",
        string="Book",
        required=True,
    )

    # Дата старту оренди
    # default=fields.Date.today автоматично ставить сьогоднішню дату коли створено запис
    rent_date = fields.Date(
        string="Rent Date",
        default=fields.Date.today,
        readonly=True,
    )

    # Кінець оренди
    # Залишити порожньою (False) поки книга не повернута.
    return_date = fields.Date(string="Return Date")

    # --- Constraints ---

    @api.constrains("book_id", "return_date")
    def _check_book_not_already_rented(self):
        """Запобігає повторній оренді книги яка вже орендована.

        Це обмеження виконується щоразу, коли book_id або return_date змінюються.
        Він шукає інші *активні* оренди (return_date пуста)
        за ту саму книгу.  Якщо такі існують, це викликає ValidationError,
        яке Odoo відображає як зручне повідомлення про помилку.
        """
        for record in self:
            conflicting_rents = self.env["library.rent"].search(
                [
                    ("book_id", "=", record.book_id.id),
                    ("return_date", "=", False),  # досі активна (not returned)
                    ("id", "!=", record.id),  # виключити поточний запис
                ]
            )

            if conflicting_rents:
                raise ValidationError(
                    f"The book '{record.book_id.name}' is already rented out "
                    "and has not been returned yet. "
                    "Please wait until it is returned before renting it again."
                )
