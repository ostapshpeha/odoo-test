# -*- coding: utf-8 -*-
from odoo import models, fields


class RentWizard(models.TransientModel):
    """Transient (wizard) model за видачу книги читачеві.

    Записи TransientModel є тимчасовими: Odoo автоматично видаляє їх
    після настроюваного періоду (за замовчуванням 24 години).  Вони ідеально підходять для
    багатокрокові діалоги або форми, які збирають дані перед виконанням
    дії, бо вони не засоряють базу даних у довгостроковій перспективі.

    Правила:
        1. Бібліотекар відкриває запис книги та клацає «Опублікувати книгу».
        2. Odoo створює порожній RentWizard із попередньо заповненим book_id
           (передається через context['default_book_id'] у Book.action_open_rent_wizard).
        3. Бібліотекар обирає читача (partner_id) і натискає «Підтвердити».
        4. action_confirm() створює запис library.rent і позначає
           книгу як недоступна.
    """

    _name = "library.rent.wizard"
    _description = "Rent Book Wizard"

    # Книга яку орендують
    book_id = fields.Many2one(
        comodel_name="library.book",
        string="Book",
        required=True,
    )

    # Читач
    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Reader",
        required=True,
    )

    def action_confirm(self):
        """Створити запис оренди і позначити книгу як неактивна.

        Кроки:
            1. Валідація, що лише один візард в обробці
               (ensure_one raises an error if called on a multi-record set).
            2. Створити library.rent запис який привязую читача до книги.
               rent_date автозаповнення.
            3. Позначити is_available = False
            4. Повернути 'перезавантажену' дію клієнта, то ж форма зміниться
               і кнопка 'Publish book' зникне
        Returns:
            dict: Odoo client action that reloads the current view.
        """
        # Валідація що цей метод викликається на один запис а не сет записів
        self.ensure_one()

        # Крок 1 створити запис
        self.env["library.rent"].create(
            {
                "book_id": self.book_id.id,
                "partner_id": self.partner_id.id,
            }
        )

        # Крок 2 : Позначити книгу недоступною
        self.book_id.write({"is_available": "false"})

        # Крок 3: Явно відкрити форму книги, щоб клієнт отримав свіжі дані з БД.
        # (reload не завжди спрацьовує при поверненні з модального діалогу)
        return {
            "type": "ir.actions.act_window",
            "res_model": "library.book",
            "res_id": self.book_id.id,
            "view_mode": "form",
            "views": [(False, "form")],
            "target": "current",
        }
