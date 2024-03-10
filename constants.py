import re
from PIL import Image

# Dict of all possible filters
filter_dict = {
    "Player Name": {
        "get_values_from_view_id": "6b5e8a50-4e87-42c8-8a19-0cd0419f1e97",
        "field_name_in_source_view": "Player 1 Name",
        "filter_field_name": "PlayerName",
        "is_required": True
    }
}

    # "Select Surface": {
    #     "values": ["All","Clay","Grass","Hard"],
    #     "filter_field_name": "surface",
    #     "is_required": False
    # }

class TableauView:
    def __init__(self, no_of_images, crop_coords, **kwargs):
        self.no_of_images = no_of_images
        self.crop_coords = crop_coords
        self.preprocess = kwargs.get('preprocess', None)
        self.img2 = kwargs.get('img2',None)
        self.paste_coords = kwargs.get('paste_coordinate', None)
        
serve_view_obj = TableauView(
    no_of_images=3,
    crop_coords=[(0,0,774,746),(0,746,1006,886),(773,7,1022,696)]
)

return_view_obj = TableauView(
    no_of_images=3,
    crop_coords=[(0,0,774,746),(0,746,1006,886),(773,7,1022,696)]
)

ground_stroke_view_obj = TableauView(
    no_of_images=2,
    crop_coords=[(0,0,782,898),(782,0,1023,898)]
)

ground_stroke_bar_chart_obj = TableauView(
    no_of_images=1,
    crop_coords=[(0,0,1022,898)],
    preprocess = 'paste',
    img2 = Image.new(mode="RGBA", size=(251,236), color="white"),
    paste_coordinate = (771,0)
)

ground_stroke_with_kpi_card_obj = TableauView(
    no_of_images=2,
    crop_coords=[(0, 52, 1467, 825), (677, 0, 1467, 52)]
)

ground_stroke_with_kpi_card_2_obj = TableauView(
    no_of_images=2,
    crop_coords=[(0, 52, 1468, 826), (0, 0, 1468, 52)]
)

winners_and_errors_heatmap_obj = TableauView(
    no_of_images=2,
    crop_coords=[(0, 52, 1468, 826), (0, 0, 1468, 52)]
)

serve_plus_1_obj = TableauView(
    no_of_images=2,
    crop_coords=[(0, 0, 781, 899), (781, 0, 1023, 899)]
)

return_plus_1_obj = TableauView(
    no_of_images=2,
    crop_coords=[(0, 0, 779, 899), (779, 0, 1023, 899)]
)

game_scenarios_obj = TableauView(
    no_of_images=2,
    crop_coords=[(0, 0, 885, 826), (885, 0, 1170, 826)]
)

stroke_speed_and_spin_obj = TableauView(
    no_of_images=2,
    crop_coords=[(0, 82, 1368, 702),(0, 0, 1368, 82)]
)

# 0, 82, 1368, 702

# x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=

class RegexDict(dict):
    def __init__(self):
        super(RegexDict, self).__init__()
        
    def __getitem__(self, item):
        for k,v in self.items():
            if re.match(k, item):
                return v
        return None

view_name_patterns = RegexDict()
view_name_patterns[r"(?i)serve view"]  = serve_view_obj
view_name_patterns[r"(?i)serve heat map view"] = serve_view_obj
view_name_patterns[r"(?i)return view"] = return_view_obj
view_name_patterns[r"(?i)return view \(heat map\)"] = return_view_obj
view_name_patterns[r"(?i)ground stroke full court view"] = ground_stroke_view_obj
view_name_patterns[r"(?i)ground stroke heat map view \(.*"] = ground_stroke_view_obj
view_name_patterns[r"(?i)ground strokes with shot type bar chart.*"] = ground_stroke_bar_chart_obj
view_name_patterns[r"(?i)ground stroke with kpi cards"] = ground_stroke_with_kpi_card_obj
view_name_patterns[r"(?i)ground stroke with kpi cards \(2\)"] = ground_stroke_with_kpi_card_2_obj
view_name_patterns[r"(?i)winners and errors heatmap.*"] = winners_and_errors_heatmap_obj
view_name_patterns[r"(?i)serve \+1.*"] = serve_plus_1_obj
view_name_patterns[r"(?i)return \+1.*"] = return_plus_1_obj
view_name_patterns[r"(?i)game scenarios.*"] = game_scenarios_obj
view_name_patterns[r"(?i)stroke speed & spin over time.*"] = stroke_speed_and_spin_obj