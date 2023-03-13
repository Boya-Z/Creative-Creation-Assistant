class Miaozhen_Tracking:
    def __init__( self, file ):
        self.pd = ''
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
        self.pd = pd.read_excel( self.excel_file, sheet_name=None )
        return self.pd.keys()

    def select_sheet( self, str ):
        self.selected_sheet = str

    def init_name_seperator( self, str ):
        self.name_seperator = str

    def generate_filter_pd( self, output_name=1, output_imp_url=1, output_click_url=1, output_device_type=1, output_site_name=1 ):
        '''输入过滤字符串list, 输出list记录集，每条记录字段顺序默认为： site_name, device_type, tracking_name, imp_url, click_url'''
        import pandas as pd
        self.pd = pd.read_excel( self.excel_file, sheet_name=self.selected_sheet )
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
        self.filtered_pd = self.pd.iloc[ :, 2:7 ]


    def get_list_from_filter_pd(self):
        import numpy as np
        return np.array( self.filtered_pd ).tolist()

    def fixed_name_list( self ):
        import numpy as np
        fixed_name_list = []
        fixed_name_struct_list = []
        if self.filtered_pd.empty:
            print( "Error: no self.filtered_pd. You should execute class.get_list_from_filter_pd() first." )
            quit()
        name_lists = np.array(self.filtered_pd.iloc[:, 2]).tolist()
        fix_seperator = self.name_seperator.strip()
        fix_seperators = [' {}'.format(fix_seperator), '{} '.format(fix_seperator)]
        for name in name_lists:
            name_splited = []
            # 修复秒针代码中可能错误的把" - "写成了" -" 或 "- "
            for f in fix_seperators:
                name = name.replace( f , self.name_seperator )
            temp_split = name.split( self.name_seperator )
            for e in temp_split:
                name_splited.append( e.strip() )
            fixed_name_list.append( self.name_seperator.join( name_splited ) )

            for i,e in enumerate( name_splited ):
                #temp_list.append( e )
                try:
                    fixed_name_struct_list[i].append( e )
                except Exception:
                    fixed_name_struct_list.append([])
                    fixed_name_struct_list[i].append( e )
        return fixed_name_list, fixed_name_struct_list



    def get_tracking_name_struct_set( self, common_market=[], common_site=[] ):
        import pandas as pd
        import numpy as np
        import re
        temp_list = []
        unique_name_structs = []
        size_list = []

        (fixed_name_list, fixed_name_struct_list) = self.fixed_name_list( )

        '''
        if self.filtered_pd.empty:
            print( "Error: no self.filtered_pd. You should execute class.get_list_from_filter_pd() first." )
            return {"error": "no self.filtered_pd. You should execute class.get_list_from_filter_pd() first."}
        name_lists = np.array( self.filtered_pd.iloc[ :, 2 ] ).tolist()
        fix_seperator = self.name_seperator.strip()
        fix_seperators = [" {}".format(fix_seperator), "{} ".format(fix_seperator)]

        for name in name_lists:
            # 修复秒针代码中可能错误的把" - "写成了" -" 或 "- "
            for f in fix_seperators:
                name = name.replace( f , self.name_seperator )
            name_split = name.split( self.name_seperator )
        '''

        for name in fixed_name_list:
            size_list.append( self.get_size_from_str( name ) )

        '''
        for name_split in fixed_name_struct_list:
            for i, e in enumerate( name_split ):
                try:
                    temp_list[i].append(e.strip())
                except Exception:
                    temp_list.append([])
                    temp_list[i].append(e.strip())
        '''
        '''
        for i, fields in enumerate( fixed_name_struct_list ):
            temp_set = set( fields )
            if len( temp_set ) < items_limited:
                unique_name_structs.append( temp_set )
        '''

        market_list = []
        for index, name_structs in enumerate( fixed_name_struct_list ):
            # fixed_name_struct_list = [[ 'Hormel', 'Hormel', 'Hormel' ],['Beef Jerky', 'Beef Jerky', 'Beef Jerky' ],[ ..... ]]

            if len( list( set(name_structs).intersection( common_market ) ) ) > 0:
                market_list = fixed_name_struct_list[index]

        return fixed_name_list, fixed_name_struct_list, set(size_list), set(market_list)

    def get_size_from_str( self, str ):
        import re
        result = ''
        re_split = re.split(r'([0-9]{2,}x[0-9]{2,})', str)
        if re_split[1] != "":
            result = re_split[1]
        return result


    def set_pd_value(self, col, data_list ):
        self.filtered_pd.iloc[:, col ] = data_list
        return True


