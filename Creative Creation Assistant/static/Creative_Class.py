class Creative():
    macros = {
        "campaign_name_macro": {
            "desc": "Campaign Name Macro",
            "key": "##cpn##",
            "value": ""
        },
        "size":
            {
                "desc": "....",
                "key": "##size##",
                "value": ""
            },
        "AdgroupID":
            {
                "desc": "TTD MACRO",
                "key": "%%AdgroupID%%",
                "value": ""
            },
        "Creative_Size":
            {
                "desc": "",
                "key": "",
                "value": "",
                "dynamics": "true"
            }
    }

    def set_campaign_macro_key(self, keywords):
        self.macros["campaign_name_macro"]["key"] = keywords
        return True

    def set_campaign_macro_value(self, keywords):
        self.macros["campaign_name_macro"]["value"] = keywords
        return True

    def other_action(self):
        # ......
        return True

