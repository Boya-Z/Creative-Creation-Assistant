class Result():
    result_according_template = ""
    results_list = []


    def generate_results( self, creative_rules, macros, creative_path ):
        ''' example
        creative_rules = [
            { #第一组选择十个创意的规则
                "name": "##cpn##_HK_Signup_##size##",
                "creative_files": ["160x600.png", "300x50.png", "300x250.png", "300x600.png", "320x50.png",
                                   "320x100.png", "320x480.png", "728x90.png", "1024x768.png", "1200x628.png"],
                "clickthrough_url": "https://www.bybit.com/zh-TW/register?regEmail&medium=paid_displayp&source=TTD&channel=paid_&campaign=HK_##cpn##&term=All_##size##&content=V1&dtpid=1634637492338",
                "landing_page_url": "https://www.bybit.com/"
            },
            { #第二组选择十个创意的规则
                "name": "##cpn##_HK_Rewards_##size##",
                "creative_files": ["160x600.png", "300x50.png", "300x250.png", "300x600.png", "320x50.png",
                                   "320x100.png", "320x480.png", "728x90.png", "1024x768.png", "1200x628.png"],
                "clickthrough_url": "https://www.bybit.com/zh-TW/register?regEmail&medium=paid_displayp&source=TTD&channel=paid_&campaign=HK_##cpn##&term=All_##size##&content=V2_Rewards_Hub&dtpid=1634637232805",
                "landing_page_url": "https://www.bybit.com/"
            },
            {
                "creative_files": ["1 (1).png", "1 (2).png", "1 (3).png"],
                name：  Control_20230213_##creativeFileName##  （第一组）
                Description:  Ecoflow 2023 Control
                Asset File Name:  Control_20230213_##creativeFileName##   (不输入则不需要重命名，保留图片后缀)
                ClickUL:  https://us.ecoflow.com/?utm_source=tzjs&utm_medium=display&utm_campaign=controlled
                landing：  https://us.ecoflow.com/
            }
        ]
        '''

        results = [  ]
        for rule_dict in creative_rules:
            for creative in rule_dict[ "creative_files" ]:
                lines = []
                for macro_obj, macro_dict in macros.items():
                    if macro_dict['dynamic'] == False:
                        name = rule_dict["name"].replace( "{}".format( macro_dict["key"] ), macro_dict["value"] )
                        clickthrough_url = rule_dict["clickthrough_url"].replace( "{}".format(macro_dict["key"]), macro_dict["value"] )
                        landing_page_url = rule_dict["landing_page_ur" \
                                                     "l"].replace( "{}".format(macro_dict["key"]), macro_dict["value"] )
                        Description = rule_dict["Description"].replace( "{}".format(macro_dict["key"]), macro_dict["value"] )
                        Asset_File_Name = rule_dict["Asset_File_Name"].replace( "{}".format(macro_dict["key"]), macro_dict["value"] )
                    else: # 动态宏替换处理
                        if macro_obj == "size":
                            # 读创意文件的size, 存如 size
                            from PIL import Image
                            im = Image.open( "{}\\{}".format( creative_path,creative ) )
                            size = "{}x{}".format( im.size[0], im.size[1] )
                            #size = '160x40'  # example
                            name = name.replace( "{}".format( macro_dict["key"] ), size )
                            clickthrough_url = clickthrough_url.replace( "{}".format( macro_dict["key"] ), size )
                            landing_page_url = landing_page_url.replace( "{}".format( macro_dict["key"] ), size )
                            Description = Description.replace( "{}".format( macro_dict["key"] ), size )
                            Asset_File_Name = Asset_File_Name.replace( "{}".format( macro_dict["key"] ), size )
                        if macro_obj == "creative_file_name":
                            # 读文件名 存入creative_file_name
                            from pathlib import Path
                            creative_file_name = "{}".format(Path(creative).stem)
                            name = name.replace( "{}".format( macro_dict["key"] ), creative_file_name )
                            clickthrough_url = clickthrough_url.replace( "{}".format( macro_dict["key"] ), creative_file_name )
                            landing_page_url = landing_page_url.replace( "{}".format( macro_dict["key"] ), creative_file_name )
                            Description = Description.replace( "{}".format( macro_dict["key"] ), creative_file_name )
                            Asset_File_Name = Asset_File_Name.replace( "{}".format( macro_dict["key"] ), creative_file_name)
                            #加原文件名的后缀
                            import os
                            file_extension = os.path.splitext(creative)[1]
                            Asset_File_Name = "{}{}".format(Asset_File_Name, file_extension)
                            # copy file to export folder, and rename it
                            if Asset_File_Name != creative :
                                import shutil
                                import flask
                                shutil.copy(os.path.join(creative_path, creative), os.path.join(os.path.abspath( "./export" ), creative))
                                os.rename( os.path.join(os.path.abspath( "./export" ), creative), os.path.join(os.path.abspath( "./export" ), Asset_File_Name))
                                # flask.send_file(os.path.join(os.path.abspath( "./export" ), Asset_File_Name))



                lines.append( name ) # name
                lines.append( Description )  # Description
                # lines.append( creative ) # Asset File Name (required)
                lines.append(Asset_File_Name)  # Asset File Name (required)
                lines.append( clickthrough_url )  # Clickthrough URL (required)
                lines.append( landing_page_url ) # Landing Page URL (required)
                lines.append( "" )  # Ad Server
                lines.append( "" )  # Creative Placement ID
                lines.append("")  # Third Party Tracking Tag 1
                lines.append("")  # Third Party Tracking Tag 2
                lines.append("")  # Third Party Tracking Tag 3
                lines.append("")  # Third Party Tracking URL 1
                lines.append("")  # Third Party Tracking URL 2
                lines.append("")  # Third Party Tracking URL 3
                lines.append("")  # Yahoo Offer Type
                lines.append("")  # Flight Start Date
                lines.append("")  # Flight End Date
                lines.append("")  # Flight Time Zone ID
                lines.append("")  # Political Candidate
                lines.append("")  # Mini Program Id
                lines.append("")  # Mini Program Path
                results.append(lines)
        self.results_list = results
        return True

    def export_to_excel( self, path, name ):
        import openpyxl
        from openpyxl.utils import get_column_letter
        workbook = openpyxl.load_workbook('./BulkCreativeImportTemplate.v28.xlsx')

        sheet = workbook.get_sheet_by_name('Hosted Display')
        # 写入正式数据
        for l_index, line in enumerate(self.results_list):
            col = 1
            for col_index, e in enumerate(line):
                sheet.cell(row=2 + l_index, column=col + col_index, value=e)
        result_file = name


        workbook.save( "{}/{}".format( path, result_file ))


        # workbook = openpyxl.Workbook()
        # sheet = workbook.active
        # sheet.title = "Hosted Display"
        # data_title = ["Name (required)","Description", "Asset File Name (required)", "Clickthrough URL (required)", "Landing Page URL (required)", "Ad Server", "Creative Placement ID", "Third Party Tracking Tag 1", "Third Party Tracking Tag 2", "Third Party Tracking Tag 3", "Third Party Tracking URL 1", "Third Party Tracking URL 2", "Third Party Tracking URL 3", "Yahoo Offer Type", "Flight Start Date", "Flight End Date", "Flight Time Zone ID", "Political Candidate", "Mini Program Id", "Mini Program Path" ]
        # col=1
        # for t in data_title:
        #     c = sheet.cell( row=1, column=col, value=t )
        #     collen = len( str(t).encode() )
        #     c.font = openpyxl.styles.Font( bold=True )
        #     letter = get_column_letter( col )
        #     sheet.column_dimensions[letter].width = collen * 1.2
        #     col += 1
        #
        # # 写入正式数据
        # for l_index, line in enumerate( self.results_list ):
        #     col = 1
        #     for col_index, e in enumerate( line ):
        #         sheet.cell( row=2+l_index, column=col+col_index , value=e )
        # result_file = name
        #
        # # 所有行自适应
        #
        #
        # workbook.save( "{}/{}".format( path, result_file ) )
        return result_file



