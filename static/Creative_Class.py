class Creative():
    macros = {
        "campaign_name": {
            "desc": "Campaign Name Macro",
            "key": "##cpn##",
            "value": "default_campaign_name",
            "dynamic": False
        },
        "size":{
            "desc": "Creative Size",
            "key": "##size##",
            "value": "",
            "dynamic": True
        },
        "TTD AdgroupID":{
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

