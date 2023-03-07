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

    def get_excel_file_sheets( self ):
        import pandas as pd
        return pd.read_excel( self.excel_file, sheet_name=None ).keys()

    def select_sheet( self, str ):
        self.selected_sheet = str

    def init_name_seperator( self, str ):
        self.name_seperator = str

    def filter_name( self, filter_list, output_name=1, output_imp_url=1, output_click_url=1, output_device_type=0, output_site_name=0 ):
        '''输入过滤字符串list'''
        import pandas as pd
        import numpy as np
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
        output_pd = pd.iloc[ :, output_col_list ]
        return np.array( output_pd ).tolist()



