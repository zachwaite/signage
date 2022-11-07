{
    "name": "Odoo Digital Signage",
    "summary": """Digital Signage""",
    "category": "Uncategorized",
    "version": "15.0.0.1",
    "author": "Waite Perspectives, LLC - Zach Waite",
    "license": "OPL-1",
    "depends": [
        "web",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/playlist_views.xml",
        "views/scene_views.xml",
        "views/menuitems.xml",
        "views/signage_layout_templates.xml",
        "views/signage_playlist_index_templates.xml",
        "views/indexed_signage_scene_templates.xml",
    ],
    "demo": [],
    "assets": {
        "web.assets_frontend": [
            "signage/static/src/scss/*",
        ],
    },
}
