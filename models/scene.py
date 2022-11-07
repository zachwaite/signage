from odoo import models, fields
from odoo.tools.safe_eval import safe_eval


class SignageScene(models.Model):
    _name = "signage.scene"
    _description = "SignageScene"

    name = fields.Char(copy=False)
    sequence = fields.Integer()
    active = fields.Boolean(default=True)
    playlist_id = fields.Many2one(
        comodel_name="signage.playlist",
        required=True,
    )
    qweb_view_id = fields.Many2one(
        comodel_name="ir.ui.view",
        required=True,
        default=lambda self: self._default_qweb_view_id(),
    )
    duration_seconds = fields.Integer(default=30)
    url = fields.Char(compute="_compute_url")
    next_url = fields.Char(compute="_compute_next_url")

    # static vs data driven
    type = fields.Selection(
        [
            ("static", "Static"),
            ("data", "Data Driven"),
        ],
        default="static",
        required=True,
    )
    static_content = fields.Image(max_width=1000, max_height=600)
    data_model = fields.Char()
    data_model_domain = fields.Char(default="[]")

    def _default_qweb_view_id(self):
        return self.sudo().env.ref("signage.sceneview_indexed_static").id

    def _compute_url(self):
        for record in self:
            record.url = f"{record.playlist_id.base_url}/{record.id}"
        return True

    def _compute_next_url(self):
        for record in self:
            scene_ids_list = record.playlist_id.scene_ids.ids
            this_index = scene_ids_list.index(record.id)
            try:
                next_id = scene_ids_list[this_index + 1]
            except IndexError:
                next_id = scene_ids_list[0]
            record.next_url = f"{record.playlist_id.base_url}/{next_id}"
        return True

    def get_data_records(self):
        self.ensure_one()
        if self.data_model:
            return (
                self.env[self.data_model]
                .sudo()
                .search(safe_eval(self.data_model_domain))
            )
        else:
            return False


class IndexedSignageScene(models.Model):
    _inherit = "signage.scene"
    _description = "IndexedSignageScene"

    header_icon = fields.Image()
    header_title = fields.Char()
    index_icon = fields.Image()
    footer_msg = fields.Char()
