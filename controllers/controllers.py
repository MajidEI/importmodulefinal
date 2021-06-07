# -*- coding: utf-8 -*-
from odoo import http

# class ImportMdl(http.Controller):
#     @http.route('/import_mdl/import_mdl/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/import_mdl/import_mdl/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('import_mdl.listing', {
#             'root': '/import_mdl/import_mdl',
#             'objects': http.request.env['import_mdl.import_mdl'].search([]),
#         })

#     @http.route('/import_mdl/import_mdl/objects/<model("import_mdl.import_mdl"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('import_mdl.object', {
#             'object': obj
#         })