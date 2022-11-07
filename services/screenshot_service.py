from odoo import models, api
from ..lib.screenshot import screenshot


class ScreenshotService(models.AbstractModel):
    _name = "screenshot.service"
    _description = "ScreenshotService"

    @api.model
    def action_update_screenshot(self, scene_id, screenshot_params):
        scene = self.env["signage.scene"].browse(scene_id)
        scene.static_content = screenshot(screenshot_params)
        return True
