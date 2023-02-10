class FileImport():
    custom_rules = [
        # {  # 第一组选择十个创意的规则
        #     "name": "##cpn##_HK_Signup_##size##",
        #     "creative_files": ["160x600.png", "300x50.png", "300x250.png", "300x600.png", "320x50.png",
        #                        "320x100.png", "320x480.png", "728x90.png", "1024x768.png", "1200x628.png"],
        #     "clickthrough_url": "https://www.bybit.com/zh-TW/register?regEmail&medium=paid_displayp&source=TTD&channel=paid_&campaign=HK_##cpn##&term=All_##size##&content=V1&dtpid=1634637492338",
        #     "landing_page_url": "https://www.bybit.com/"
        # }
        # },
        # {  # 第二组选择十个创意的规则
        #     "name": "##cpn##_HK_Rewards_##size##",
        #     "creative_files": ["160x600.png", "300x50.png", "300x250.png", "300x600.png", "320x50.png",
        #                        "320x100.png", "320x480.png", "728x90.png", "1024x768.png", "1200x628.png"],
        #     "clickthrough_url": "https://www.bybit.com/zh-TW/register?regEmail&medium=paid_displayp&source=TTD&channel=paid_&campaign=HK_##cpn##&term=All_##size##&content=V2_Rewards_Hub&dtpid=1634637232805",
        #     "landing_page_url": "https://www.bybit.com/"
        # }
    ]

    def clean_rules(self):
        self.custom_rules.clear()
        return True

    def add_rules(self, name, files, click, landing):
        rule ={  # 第一组选择十个创意的规则
            "name": name,
            "creative_files": files,
            "clickthrough_url": click,
            "landing_page_url": landing
        }
        self.custom_rules.append(rule)
        return True
