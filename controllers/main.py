import pytz
import datetime
from odoo import http
from odoo.http import request
from odoo.tools.safe_eval import safe_eval


class SignageController(http.Controller):
    @http.route("/signage", auth="public")
    def signage_playlist_index(self):
        playlists = request.env["signage.playlist"].sudo().search([])
        header_icon = request.env.company.logo
        header_title = "Available Playlists"
        return request.render(
            "signage.playlist_index",
            {
                "playlists": playlists,
                "header_icon": header_icon,
                "header_title": header_title,
            },
        )

    @http.route("/playlist/<int:playlist_id>", auth="public")
    def signage_playlist_init(self, playlist_id):
        """Redirect to the first scene in the playlist"""
        playlist = request.env["signage.playlist"].sudo().browse(playlist_id)
        return request.redirect(playlist.scene_ids[0].url)

    @http.route("/playlist/<int:playlist_id>/<int:scene_id>", auth="public")
    def signage_playlist_scene(self, playlist_id, scene_id):
        """Navigate to a specific scene
        This will:
        - get the template
        - get the duration
        - get the next url
        - get the records that fill the template

        The template layout will load some js to set a timer to go to
        the next page once this one has shown for the duration.
        """
        scene = (
            request.env["signage.scene"]
            .sudo()
            .search([("playlist_id", "=", playlist_id), ("id", "=", scene_id)])
        )
        user_tz = pytz.timezone(request.env.user.tz)
        localtime = datetime.datetime.now(user_tz)
        return scene.qweb_view_id._render(
            {
                "localtime": localtime,
                "scene": scene,
                "data_records": scene.get_data_records(),
                "duration_seconds": scene.duration_seconds,
                "next_url": scene.next_url,
            },
        )
