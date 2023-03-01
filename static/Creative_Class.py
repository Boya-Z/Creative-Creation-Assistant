class Creative():
    macros = {
        "campaign_name": {
            "desc": "Campaign Name Macro",
            "key": "##cpn##",
            "value": "default_campaign_name",
            "dynamic": False
        },
        "creative_file_name":{
            "desc": "the Original Name of Creative File",
            "key": "##cfn##",
            "value": "*depend on uploaded creative files",
            "dynamic": True
        },
        "Creative_size": {
            "desc": "Creative Size, i.e. 300x250",
            "key": "##cs##",
            "value": "*depend on uploaded creative files",
            "dynamic": True
        },
        "TTD AdgroupID": {
            "desc": "Macro in TTD",
            "key": "%%AdGroupID%%",
            "value": "",
            "dynamic": True
        },
        "TTD CampaignID": {
            "desc": "Macro in TTD",
            "key": "%%CampaignID%%",
            "value": "",
            "dynamic": True
        }
    }

    def set_campaign_macro_key(self, keywords):
        self.macros["campaign_name"]["key"] = keywords
        return True

    def set_campaign_macro_value(self, keywords):
        self.macros["campaign_name"]["value"] = keywords
        return True

    def get_size(self, file ):
        from PIL import Image
        im = Image.open( file )
        return im.size

    def get_file_name(self, filepath ):
        import os
        from pathlib import Path
        # name = os.path.basename(filepath)
        name = Path(filepath).stem
        return name

    def get_file_full_name(self, filepath ):
        from pathlib import Path
        name= Path(filepath).stem
        fullname=Path(filepath).name


