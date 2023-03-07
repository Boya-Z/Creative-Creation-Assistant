class Miaozhen_Tracking():
    def __init__( self, file ):
        self.excel_file = file
        self.site_name_col= "C",
        self.site_name_col_index = 2,
        self.device_type_col = "D",
        self.device_type_col_index = 3,
        self.tracking_name_col = "E",
        self.tracking_name_col_index = 4,
        self.imp_url_col = "F",
        self.imp_url_col_index = 5,
        self.click_url_col = "G",
        self.click_url_col_index = 6

    def get_sheets( self ):
        import pandas as pd
        return pd.read_excel( self.excel_file, sheet_name=None ).keys()

    def select_sheet( self, str ):
        self.selected_sheet = str

    def init_name_seperator( self, str ):
        self.name_seperator = str

    def generate_filter_pd( self, filter_list=[], output_name=1, output_imp_url=1, output_click_url=1, output_device_type=1, output_site_name=1 ):
        '''输入过滤字符串list, 输出list记录集，每条记录字段顺序默认为： site_name, device_type, tracking_name, imp_url, click_url'''
        import pandas as pd

        pd.read_excel( self.excel_file, sheet_name=self.selected_sheet )
        output_col_list = []
        if output_site_name == 1:
            output_col_list.append( self.site_name_col_index )
        if output_device_type == 1:
            output_col_list.append( self.device_type_col_index )
        if output_name == 1:
            output_col_list.append( self.tracking_name_col_index )
        if output_imp_url == 1:
            output_col_list.append( self.imp_url_col_index )
        if output_click_url == 1:
            output_col_list.append( self.click_url_col_index )
        self.filtered_pd = pd.iloc[ :, output_col_list ]

    def get_list_from_filter_pd(self):
        import numpy as np
        return np.array( self.filtered_pd ).tolist()

    def get_tracking_name_struct_set( self ):
        import pandas as pd
        import numpy as np
        result = {
            'site_name': [],
            'device_type': [],
            'tracking_name': [],
            'imp_url': [],
            'click_url': []
        }
        if self.filtered_pd.empty:
            return {"error": "no self.filtered_pd. You should execute class.get_list_from_filter_pd() first."}
        name_lists = np.array( self.filtered_pd.iloc[ :, 2 ] ).tolist()
        for name in name_lists:
            elements = name.split( self.name_seperator )
            result['site_name'].append( elements[0] )
            result['device_type'].append( elements[1] )
            result['tracking_name'].append( elements[2] )
            result['imp_url'].append( elements[3] )
            result['click_url'].append( elements[4] )
        for key,value in result.items():
            result[key] = set( value )
        return result




