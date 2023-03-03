from zipfile import ZIP_DEFLATED
import flask
from flask import Flask, render_template, request, session, Response
from datetime import timedelta
import requests, json, socket
import os, stat, filetype, zipfile
import static.Creative_Class as classCreative
import static.Result_Class as classResult
import win32com.client as win32
import pythoncom
campaignName = ""
#basedir = os.path.abspath( os.path.dirname(__file__) )
#se_upload_path = os.path.join( basedir, "upload", campaignName )
#se_export_path = os.path.join( basedir, "export", campaignName )

app = Flask(__name__, template_folder='templates', static_folder='static' )
app.add_template_filter( enumerate )
# app.add_template_filter( items )

# 访问主界面，打开后包括了一级功能入口，比如campaignName设置入口，Hosted类创意设置入口，NamingConversion设置入口，生成CreativeTemplate功能按钮，辅助功能入口等
@app.route('/')
def index():
    # 经验建议：
    # 可以根据用户输入的user.name存储项目临时文件 或者 根据用户的IP地址存储项目临时文件，便于二次访问时候获取上次的历史记录
    # 如果有历史记录数据，则将其值传入exsiting_data一起返回界面
    return render_template('index.html',exsiting_data = dict() )

@app.route('/CampaignName')
def CampaignName():
    # 如果有历史记录数据，则将其值传入exsiting_data一起返回界面
    if 'campaignName' not in session.keys():
        session['campaignName'] = ""
    # 初始化创意设置规则
    if 'creative_rules' not in session.keys():
        session['creative_rules'] = []
    campaign_macro_dict = classCreative.Creative()
    campaign_macro_dict.set_campaign_macro_value( session["campaignName"] )
    return render_template( 'CampaignName.html', campaign_name_macro=campaign_macro_dict.macros['campaign_name'] )


@app.route('/CampaignNameSetting', methods=['POST'] )
def CampaignNameSetting(  ):
    session['campaignName'] = request.form.get("campaign_name")
    if not os.path.exists("./export/{}/".format( session['campaignName'] ) ):
        os.makedirs( "./export/{}/".format( session['campaignName'] ) )
        os.chmod( "./export/{}/".format( session['campaignName'] ) , stat.S_IRWXO )
    if not os.path.exists("./upload/{}/".format( session['campaignName'] ) ):
        os.makedirs("./upload/{}/".format(session['campaignName']))
        os.chmod("./upload/{}/".format(session['campaignName']), stat.S_IRWXO )
    session['export_path'] = "./export/{}/".format(session['campaignName'])
    session['upload_path'] = "./upload/{}/".format(session['campaignName'])
    #creative = classCreative.Creative()
    #creative.set_campaign_macro_value( campaignName )
    # 如果有历史记录数据，则将其值传入exsiting_data一起返回界面
    return render_template( 'chooseFile.html' )

@app.route( '/viewMacros' )
def viewMacros():
    campaign_macro_dict = classCreative.Creative()
    campaign_macro_dict.set_campaign_macro_value(session["campaignName"])
    return render_template('viewMacros.html', macros=campaign_macro_dict.macros )

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
    upload_path = session['upload_path']
    '''
    if not os.path.exists("./export/{}/".format( classCreative.Creative.macros["campaign_name"]["value"]) ):
        os.makedirs("./export/{}/".format( classCreative.Creative.macros["campaign_name"]["value"]) )
    '''
    context['uploaded_number'] = len( request.files )
    upload_files = request.files.getlist('files')
    '''
    if not os.path.exists( "./upload/{}/".format( classCreative.Creative.macros["campaign_name"]["value"] ) ):
        os.makedirs( "./upload/{}/".format( classCreative.Creative.macros["campaign_name"]["value"] ) )
    upload_campaign_path = "./upload/{}/".format( classCreative.Creative.macros["campaign_name"]["value"] )
    '''
    #upload_campaign_path = "./upload/{}/".format( campaignName )
    for upload_file in upload_files:
        temp = []
        upload_file_path = os.path.join( upload_path, upload_file.filename )
        # 存储文件size
        upload_file.save( upload_file_path )
        size = Image.open( upload_file_path ).size
        kind = filetype.guess( upload_file_path )
        temp.append( upload_file.filename )
        temp.append( size[0] )
        temp.append( size[1] )
        temp.append( kind.extension )
        temp.append( kind.mime )
        file_list.append( temp )
    creative_class = classCreative.Creative()
    creative_class.set_campaign_macro_value( session['campaignName'] )
    session['creative_macros'] = creative_class.macros
    return render_template('CreativeSetting.html', file_list=file_list, macros=session['creative_macros'] )

@app.route( '/sumbitted' )
def get_sumbitted():
    return render_template( 'submitted.html', creative_rules=session['creative_rules'] )

@app.route( '/add_rules', methods=['POST'] )
def add_rules():
    if os.path.exists( "{}rules.tmp".format( session['upload_path'] ) ):
        with open( "{}rules.tmp".format( session['upload_path'] ) ) as fo:
            rules_list = json.load( fo )
    else:
        rules_list = []
    session['rules_file'] = "{}rules.tmp".format( session['upload_path'] )
    rules_list.append(
        {
            "creative_files": request.form.get( 'files' ).split(","),
            "name": request.form.get('creative_name_rule'),
            "Description": request.form.get('Description_rule'),
            "Asset_File_Name": request.form.get('Asset_File_Name_rule'),
            "clickthrough_url": request.form.get('clickthrough_rule'),
            "landing_page_url": request.form.get('landing_page_rule')
        }
    )
    with open( "{}rules.tmp".format( session['upload_path'] ), "w" ) as fo:
        json.dump( rules_list, fo )
    return render_template('submitted.html', creative_rules=rules_list )

@app.route('/output')
def exportXlsx():
    #creative_upload_path = os.path.abspath( se_upload_path )
    #result_export_path = os.path.abspath( se_export_path )
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
    resultObj = classResult.Result()
    # session['rules_file']
    with open( session['rules_file'] , 'r' ) as fo:
        creative_rules = json.load( fo )
    resultObj.generate_results( creative_rules=creative_rules, macros=session['creative_macros'], creative_path=session['upload_path'], export_path=session['export_path'] )
    result_file_name = resultObj.export_to_excel( path=session['export_path'], name="{}_BulkCreativeImport_Result_v28.xlsx".format( session['campaignName']) )
    file_path = os.path.join( session['export_path'], result_file_name )
    return flask.send_file(file_path)

@app.route( '/empty' )
def empty():
    # clean creative_rules list
    session['creative_rules'].clear()
    # 清空 export folder
    directory = os.path.abspath( session['export_path'] )
    for f in os.listdir(directory):
        os.remove(os.path.join(directory, f))
    # 清空 upload folder
    directory = os.path.abspath(session['upload_path'])
    for f in os.listdir(directory):
        os.remove(os.path.join(directory, f))
    return render_template( 'chooseFile.html' )

@app.route( '/delete_last_rule' )
def delete_last_rule():
    # delete the last rule of creative_rules list
    session['creative_rules'].pop(-1)

    return render_template( 'chooseFile.html' )

@app.route('/download_zip')
def download():
    exportXlsx()
    from flask import send_file
    from glob import glob
    from io import BytesIO
    from zipfile import ZipFile

    stream = BytesIO()
    with ZipFile(stream, 'w') as zf:
        for root, subdirs, files in os.walk( session['export_path'] ):
            for filename in files:
                zf.write( os.path.join( root, filename ) )
    stream.seek(0)

    return send_file(
        stream,
        as_attachment=True,
        download_name='{}_BulkCreativeImport_Result.zip'.format( session['campaignName'] )
    )
app.secret_key = 'tz.Feb.2023'

if __name__ == '__main__':
    app.run( host='0.0.0.0', port='27804' )
    #app.run(host='127.0.0.1', port='80')
