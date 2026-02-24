# -*- coding: utf-8 -*-
"""REST API controller for the Library Management module.

Exposes a single public endpoint:

    GET /library/books
        Returns a JSON array with every book in the catalogue and its
        current availability status.

Example response:
    [
        {
            "id": 1,
            "name": "Clean Code",
            "author": "Robert C. Martin",
            "published_date": "2008-08-01",
            "is_available": true
        },
        ...
    ]
"""

import json

from odoo import http
from odoo.http import request


class LibraryController(http.Controller):
    """Групує всі ендпоінти до модуля біблотеки library_management"""

    @http.route(
        "/library/books",
        type="http",  # HTTP request
        auth="public",  # Без логіну
        methods=["GET"],
        csrf=False,  # GET requests don't carry a CSRF token
    )
    def get_books(self):
        """Повертає JSON список всіх книг зі статусом.

        Використав sudo() щоб список не залежав від прав користувача

        Returns:
            Response: HTTP 200 with Content-Type: application/json and a
                      JSON-encoded list of book dicts.
        """
        # Забрати всі книги з БД
        books = request.env["library.book"].sudo().search([])

        # Серіалізувати книги в пайтон словник
        # fields.Date пайтон об'єкти; str() конвертує їх до
        # ISO-8601  (YYYY-MM-DD) які є JSON-friendly.
        result = []
        for book in books:
            result.append(
                {
                    "id": book.id,
                    "name": book.name,
                    # Тут треба використати JSON friendly формат для пустих полів
                    "author": book.author or "",
                    "published_date": (
                        str(book.published_date) if book.published_date else None
                    ),
                    "is_available": book.is_available == "true",
                }
            )

        # Будую HTTP відповідь вручну бо type='http' не
        # не серіалізую дані автоматично.
        return request.make_response(
            json.dumps(result, ensure_ascii=False),
            headers=[("Content-Type", "application/json; charset=utf-8")],
        )
