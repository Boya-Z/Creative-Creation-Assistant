import flask
from flask import Flask, render_template, request
from datetime import timedelta
import requests, json, socket
import os
import static.Creative_Class as classCreative
import static.Result_Class as classResult


app = Flask(__name__, template_folder='templates', static_folder='static' )
app.add_template_filter( enumerate )
# app.add_template_filter( items )

creative_rules = []
# 访问主界面，打开后包括了一级功能入口，比如campaignName设置入口，Hosted类创意设置入口，NamingConversion设置入口，生成CreativeTemplate功能按钮，辅助功能入口等
@app.route('/')
def index():
    # 经验建议：
    # 可以根据用户输入的user.name存储项目临时文件 或者 根据用户的IP地址存储项目临时文件，便于二次访问时候获取上次的历史记录
    # 如果有历史记录数据，则将其值传入exsiting_data一起返回界面
    return render_template('index.html',exsiting_data = dict())

@app.route('/CampaignName')
def CampaignName():
    # 如果有历史记录数据，则将其值传入exsiting_data一起返回界面
    return render_template('CampaignName.html', campaign_name_macro=classCreative.Creative.macros["campaign_name"] )


@app.route('/CampaignNameSetting', methods=['POST'] )
def CampaignNameSetting(  ):
    campaignName = request.form.get("campaign_name")
    creative = classCreative.Creative()
    creative.set_campaign_macro_value( campaignName )
    # 如果有历史记录数据，则将其值传入exsiting_data一起返回界面
    return render_template('index.html')

@app.route( '/viewMacros' )
def viewMacros():
    print(classCreative.Creative.macros)
    return render_template('viewMacros.html', macros=classCreative.Creative.macros )

@app.route( '/chooseFile' )
def chooseFile():
    return render_template('chooseFile.html')

@app.route( '/fileUpload', methods=["POST"] )
def fileupload():
    from PIL import Image
    # im = Image.open(file)
    # return im.size
    context = {}
    file_list = []
    context['uploaded_number'] = len( request.files )
    upload_files = request.files.getlist('files')
    for upload_file in upload_files:
        temp = []
        upload_path = os.path.join( 'upload', upload_file.filename )
        # 存储文件size
        upload_file.save( upload_path )
        size = Image.open(upload_path).size
        temp.append( upload_file.filename )
        temp.append( size[0] )
        temp.append( size[1] )
        file_list.append( temp )
    return render_template('CreativeSetting.html', file_list=file_list, macros=classCreative.Creative.macros )

@app.route('/sumbitted')
def get_sumbitted():
    return render_template('submitted.html', creative_rules=creative_rules )

@app.route('/add_rules', methods=['POST'] )
def add_rules():
    creative_rules.append(
                {
                    "creative_files": request.form.get( 'files' ).split(","),
                    "name": request.form.get('creative_name_rule'),
                    "clickthrough_url": request.form.get('clickthrough_rule'),
                    "landing_page_url": request.form.get('landing_page_rule')
                }
            )
    return render_template('submitted.html', creative_rules=creative_rules )

@app.route('/output')
def exportXlsx():
    creative_upload_path = os.path.abspath( "./upload" )
    '''
    creative_rules = [
        {  # 第一组选择十个创意的规则
            "name": "##cpn##_HK_Signup_##size##",
            "creative_files": ["1 (1).png", "1 (2).png", "1 (3).png"],
            "clickthrough_url": "https://www.bybit.com/zh-TW/register?regEmail&medium=paid_displayp&source=TTD&channel=paid_&campaign=HK_##cpn##&term=All_##size##&content=V1&dtpid=1634637492338",
            "landing_page_url": "https://www.bybit.com/"
        },
        {  # 第二组选择十个创意的规则
            "name": "##cpn##_HK_Rewards_##size##",
            "creative_files": ["1 (1).png", "1 (2).png", "1 (3).png"],
            "clickthrough_url": "https://www.bybit.com/zh-TW/register?regEmail&medium=paid_displayp&source=TTD&channel=paid_&campaign=HK_##cpn##&term=All_##size##&content=V2_Rewards_Hub&dtpid=1634637232805",
            "landing_page_url": "https://www.bybit.com/"
        }
    ]
    '''

    resultObj = classResult.Result()
    resultObj.generate_results( creative_rules=creative_rules, macros=classCreative.Creative.macros, creative_path=creative_upload_path )
    result_file_name = resultObj.export_to_excel( path=os.path.abspath( "./export" ), name="result.xlsx" )
    basedir = os.path.abspath( os.path.dirname(__file__) )
    file_path = os.path.join( basedir, "export", result_file_name )
    return flask.send_file(file_path)


if __name__ == '__main__':
    app.run( host='0.0.0.0', port='27804' )
    #app.run(host='127.0.0.1', port='80')
