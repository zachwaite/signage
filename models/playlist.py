from odoo import models, fields


class SignagePlaylist(models.Model):
    _name = "signage.playlist"
    _description = "SignagePlaylist"

    name = fields.Char()
    active = fields.Boolean(default=True)
    scene_ids = fields.One2many(
        comodel_name="signage.scene",
        inverse_name="playlist_id",
    )
    base_url = fields.Char(
        compute="_compute_base_url",
    )

    def _compute_base_url(self):
        base_url = self.env["ir.config_parameter"].sudo().get_param("web.base.url")
        for record in self:
            record.base_url = f"{base_url}/playlist/{record.id}"
        return True
