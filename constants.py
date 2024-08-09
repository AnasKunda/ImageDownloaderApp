import re
from PIL import Image


# Dict of all common filters.
# The Player Name filter fetches values from a view. Rest all have pre defined values.
# The filter_field_name is the column in Dashboard used to filter values.
    
filter_dict = {
    "Player Name": {
        "get_values_from_view_id": "6b5e8a50-4e87-42c8-8a19-0cd0419f1e97",
        "field_name_in_source_view": "Player 1 Name",
        "filter_field_name": "PlayerName",
        "is_required": True,
        "has_default": True
    },
    "Surface": {
        "values": ["Clay","Grass","Hard"],
        "is_required": False,
        "filter_field_name": "surface",
        "has_default": False
    },
    "Opponent Hand": {
        "values": ["Left", "Right"],
        "is_required": False,
        "filter_field_name": "opponent_handedness",
        "has_default": False
    },
    "Year From": {
        "values": ["2020","2021","2022","2023","2024"],
        "is_required": False,
        "filter_field_name": "event_year_param",
        "has_default": False
    }
}

 
# Dict of all view-specific filters.

iteration_filter_dict = {
    "Shot Selection": {
        "values":["Stroke - Include VolleyOverheads","Backhand","Backhand Drive Volley","Backhand Overhead","Backhand Volley","Forehand","Forehand Drive Volley","Forehand Overhead","Forehand Volley","Serve","UNKNOWN","UNKNOWN Drive Volley","UNKNOWN Overhead","UNKNOWN Volley"]
    },
    "Is Inside Baseline": {
        "values":["TRUE","FALSE"]
    },
    "Forehand hit from Backhand Corner": {
        "values":["True","False"]
    },
    "Service Side": {
        "values":["Advantage","Deuce"]
    },
    "Which Serve": {
        "values":["First Serve","Second Serve"]
    },
    "Hit from Mid section?": {
        "values":["TRUE","FALSE"]
    },
    "Stroke": {
        "values":["Backhand","Forehand","Serve"]
    },
    "Zones": {
        "values":["Zone 1","Zone 2","Zone 3","Zone 4","Zone 5",]
    }
}

class TableauView:
    ''' 
        There is a TableauView object for each view. If a newly added view does not have an associated TableauView
        object, then refer to technical document to see how to create a TableauView object.
        
        Attributes:
        no_of_images: Number of images to download per iteration. This number must match with the number of crop coordinates.
        crop_coords: crop coordinates in the format: (left top x, left top y, bottom right x, bottom right y) in pixels.
        preprocess: One view requires some preprocessing before downloading. A portion of image must be covered with plain white color.
        img2: The image with which preprocessing should be done. Generally it is a plain white image to cover a portion.
        paste_coords: The coordinate location where the img2 should be pasted on top of the original image.
        iteration_filters: view-specific filter that a view has.
        exclude_common_filters: to exclude a common filter
    '''
    def __init__(self, no_of_images, crop_coords, **kwargs):
        self.no_of_images = no_of_images
        self.crop_coords = crop_coords
        self.preprocess = kwargs.get('preprocess', None)
        self.img2 = kwargs.get('img2',None)
        self.paste_coords = kwargs.get('paste_coordinate', None)
        self.iteration_filters = kwargs.get('iteration_filters', None)
        self.exclude_common_filters = kwargs.get('exclude_common_filters', None)
        
serve_view_obj = TableauView(
    no_of_images=3,
    crop_coords=[(0,0,774,766),(0,766,1006,886),(773,7,1022,696)]
)

s_1_r_1_obj = TableauView(
    no_of_images=2,
    crop_coords=[(0,0,626,571),(951,0,1167,276)]
)

serve_view_heat_map_obj = TableauView(
    no_of_images=3,
    crop_coords=[(0,0,773,741),(0,750,1023,899),(774,0,1023,741)]
)

return_view_obj = TableauView(
    no_of_images=3,
    crop_coords=[(0,0,774,746),(0,746,1006,886),(773,7,1022,696)]
)

return_view_v2_obj = TableauView(
    no_of_images=2,
    crop_coords=[(0,0,772,900),(773,0,1022,900)]
)

return_view_heat_map_obj = TableauView(
    no_of_images=3,
    crop_coords=[(0,0,772,772),(0,773,772,899),(772,0,1024,772)]
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
    crop_coords=[(0, 52, 1467, 825), (0, 0, 1468, 52)],
    iteration_filters = {"Hit from Mid section?":"Hit from Mid section?",\
                        "Zones":"Zones"}
)

ground_stroke_with_kpi_card_2_obj = TableauView(
    no_of_images=2,
    crop_coords=[(0, 52, 1468, 826), (0, 0, 1468, 52)],
    iteration_filters = {"Stroke":"stroke",\
                        "Is Inside Baseline":"Is Inside Baseline?",\
                        "Forehand hit from Backhand Corner":"Forehand hit from Backhand Corner"},
    exclude_common_filters = ["surface"]
)

winners_and_errors_heatmap_obj = TableauView(
    no_of_images=2,
    crop_coords=[(0, 52, 1468, 826), (0, 0, 1468, 52)],
    iteration_filters = {"Shot Selection":"Stroke - Include VolleyOverheads"}
)

serve_plus_1_obj = TableauView(
    no_of_images=2,
    crop_coords=[(0, 0, 781, 899), (781, 0, 1023, 899)],
    iteration_filters = {"Service Side":"court_side", "Which Serve":"WhichServe"}
)

serve_plus_1_heatmap_obj = TableauView(
    no_of_images=4,
    crop_coords=[(0,0,784,567),(0,568,784,615),(0,616,836,900),(785,0,1025,684)]
)

return_plus_1_obj = TableauView(
    no_of_images=2,
    crop_coords=[(0, 0, 779, 899), (779, 0, 1023, 899)],
    iteration_filters = {"Which Serve":"WhichServe"}
)

game_scenarios_obj = TableauView(
    no_of_images=2,
    crop_coords=[(0, 0, 885, 826), (885, 0, 1170, 826)]
)

stroke_speed_and_spin_obj = TableauView(
    no_of_images=2,
    crop_coords=[(0, 82, 1368, 702),(0, 0, 1368, 82)]
)

ppc_npc_obj = TableauView(
    no_of_images=2,
    crop_coords=[(0,70,1500,754),(0,0,1500,70)]
)

fh_backhand_detailed_tables_obj = TableauView(
    no_of_images=2,
    crop_coords=[(0,60,1468,826),(0,0,1468,60)],
    exclude_common_filters = ["surface", "opponent_handedness"]
)

when_opponent_at_the_end_obj = TableauView(
    no_of_images=2,
    crop_coords=[(0,0,829,800),(830,0,1000,800)]
)

vs_slice_obj = TableauView(
    no_of_images=2,
    crop_coords=[(0,0,768,707),(769,0,1000,202)]
)

fluctuation_global_obj = TableauView(
    no_of_images=1,
    crop_coords=[(0,0,1500,1040)]
)

cizr_fluctuations_obj = TableauView(
    no_of_images=2,
    crop_coords=[(0,120,1468,959),(1238,0,1468,120)]
)

cizr_opp_fluctuations_obj = TableauView(
    no_of_images=2,
    crop_coords=[(0,126,1466,902),(1256,0,1466,126)]
)

tour_averages_obj = TableauView(
    no_of_images=2,
    crop_coords=[(0,70,400,1126),(0,0,150,70)]
)

# x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=

class RegexDict(dict):
    ''' 
        A dictionary like class that takes a regular expression as an input.
        The regular expression matches with a specific view name and returns the corresponding TableauView object.
    '''
    def __init__(self):
        super(RegexDict, self).__init__()
        
    def __getitem__(self, item):
        for k,v in self.items():
            if re.match(k, item):
                return v
        return None
    
    def get(self, item, default):
        for k,v in self.items():
            if re.match(k, item):
                return v
        return default

# note the regular expressions and the corresponding TableauView object
view_name_patterns = RegexDict()
view_name_patterns[r"(?i)serve view \(first"]  = serve_view_obj
view_name_patterns[r"(?i)serve view \(second"]  = serve_view_obj
view_name_patterns[r"(?i)serve view \(heat map\)"] = serve_view_heat_map_obj
view_name_patterns[r"(?i)serve view heatmap\(with tour avgs\)"] = serve_view_heat_map_obj
view_name_patterns[r"(?i)serve view"]  = serve_view_obj
view_name_patterns[r"(?i)return view \(heat map\)"] = return_view_heat_map_obj
view_name_patterns[r"(?i)return view \(v[2,3]\).*"] = return_view_v2_obj
view_name_patterns[r"(?i)return view"] = return_view_obj
view_name_patterns[r"(?i)ground stroke full court view"] = ground_stroke_view_obj
view_name_patterns[r"(?i)ground stroke heat map view \(.*"] = ground_stroke_view_obj
view_name_patterns[r"(?i)ground strokes with shot type bar chart.*"] = ground_stroke_bar_chart_obj
view_name_patterns[r"(?i)ground stroke with kpi cards \(2\).*"] = ground_stroke_with_kpi_card_2_obj
view_name_patterns[r"(?i)ground stroke with kpi cards v3.*"] = ground_stroke_with_kpi_card_2_obj
view_name_patterns[r"(?i)ground stroke with kpi cards.*"] = ground_stroke_with_kpi_card_obj
view_name_patterns[r"(?i)winners and errors heatmap.*"] = winners_and_errors_heatmap_obj
view_name_patterns[r"(?i)serve \+1 \(heat map\)"] = serve_plus_1_obj
view_name_patterns[r"(?i)serve \+1.*"] = serve_plus_1_obj
view_name_patterns[r"(?i)return \+1.*"] = return_plus_1_obj
view_name_patterns[r"(?i)game scenarios.*"] = game_scenarios_obj
view_name_patterns[r"(?i)stroke speed & spin over time.*"] = stroke_speed_and_spin_obj
view_name_patterns[r"(?i)ppc-npc.*"] = ppc_npc_obj
view_name_patterns[r"(?i)fh and backhand detailed tables.*"] = fh_backhand_detailed_tables_obj
view_name_patterns[r"(?i)[s,r]\+1 based on.*"] = s_1_r_1_obj
view_name_patterns[r"(?i)when opponent at.*"] = when_opponent_at_the_end_obj
view_name_patterns[r"(?i)vs slice.*"] = vs_slice_obj
view_name_patterns[r"(?i)fluctuations global.*"] = fluctuation_global_obj
view_name_patterns[r"(?i)cizr fluctuations.*"] = cizr_fluctuations_obj
view_name_patterns[r"(?i)cizr opp fluctuations.*"] = cizr_opp_fluctuations_obj
view_name_patterns[r"(?i)tour averages by rankings.*"] = tour_averages_obj