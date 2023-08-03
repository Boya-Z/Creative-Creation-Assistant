from zipfile import ZIP_DEFLATED
import flask
from flask import Flask, render_template, request, session, Response
# from datetime import timedelta
import requests, json, socket
import os, stat, filetype, zipfile
import static.Creative_Class as classCreative
import static.Result_Class as classResult
# import tkinter as tk
# from tkinter import ttk
import static.Miaozhen_Tracking_Class as miaozhen
import static.Common_Class as commonClass

import webview

NORM_FONT = ("Verdana", 10)


campaignName = ""
# basedir = os.path.abspath( os.path.dirname(__file__) )
# se_upload_path = os.path.join( basedir, "upload", campaignName )
# se_export_path = os.path.join( basedir, "export", campaignName )

app = Flask(__name__, template_folder='templates', static_folder='static')
app.add_template_filter(enumerate)
app.add_template_filter(len, name='len')
window = webview.create_window('Creative Bulk Import Assistant',app)

# app.add_template_filter( items )

# 访问主界面，打开后包括了一级功能入口，比如campaignName设置入口，Hosted类创意设置入口，NamingConversion设置入口，生成CreativeTemplate功能按钮，辅助功能入口等
@app.route('/')
def index():
    # 经验建议：
    # 可以根据用户输入的user.name存储项目临时文件 或者 根据用户的IP地址存储项目临时文件，便于二次访问时候获取上次的历史记录
    # 如果有历史记录数据，则将其值传入exsiting_data一起返回界面
    return render_template('index.html', exsiting_data=dict())


@app.route('/CampaignName')
def CampaignName():
    # 如果有历史记录数据，则将其值传入exsiting_data一起返回界面
    if 'campaignName' not in session.keys():
        session['campaignName'] = ""
    # 初始化创意设置规则
    if 'creative_rules' not in session.keys():
        session['creative_rules'] = []
    campaign_macro_dict = classCreative.Creative()
    campaign_macro_dict.set_campaign_macro_value(session["campaignName"])
    return render_template('CampaignName.html', campaign_name_macro=campaign_macro_dict.macros['campaign_name'])


@app.route('/CampaignNameSetting', methods=['POST'])
def CampaignNameSetting():
    session['campaignName'] = request.form.get("campaign_name")
    if not os.path.exists("./export/{}/".format(session['campaignName'])):
        os.makedirs("./export/{}/".format(session['campaignName']))
        os.chmod("./export/{}/".format(session['campaignName']), stat.S_IRWXO)
    if not os.path.exists("./upload/{}/".format(session['campaignName'])):
        os.makedirs("./upload/{}/".format(session['campaignName']))
        os.chmod("./upload/{}/".format(session['campaignName']), stat.S_IRWXO)
    session['export_path'] = "./export/{}/".format(session['campaignName'])
    session['upload_path'] = "./upload/{}/".format(session['campaignName'])
    # creative = classCreative.Creative()
    # creative.set_campaign_macro_value( campaignName )
    # 如果有历史记录数据，则将其值传入exsiting_data一起返回界面
    return render_template('chooseFile.html')


@app.route('/viewMacros')
def viewMacros():
    campaign_macro_dict = classCreative.Creative()
    campaign_macro_dict.set_campaign_macro_value(session["campaignName"])
    return render_template('viewMacros.html', macros=campaign_macro_dict.macros)


@app.route('/chooseFile')
def chooseFile():
    return render_template('chooseFile.html')


@app.route('/fileUpload', methods=["POST"])
def fileupload():
    from PIL import Image
    import cv2
    # im = Image.open(file)
    # return im.size
    context = {}
    file_list = []
    upload_path = session['upload_path']
    context['uploaded_number'] = len(request.files)
    upload_files = request.files.getlist('files')
    # upload_files = request.form.get('all_files')
    # print(request.form.get('all_files'))
    # print(request.files.getlist('all_files'))
    # print(upload_files)
    for upload_file in upload_files:
        temp = []
        upload_file_path = os.path.join(upload_path, upload_file.filename)
        # 存储文件size
        upload_file.save(upload_file_path)
        kind = filetype.guess(upload_file_path)
        if kind.mime.split('/')[0] == 'image':
            size = Image.open(upload_file_path).size
            temp.append(upload_file.filename)
            temp.append(size[0])
            temp.append(size[1])
            temp.append(kind.extension)
            temp.append(kind.mime)
            file_list.append(temp)
        elif kind.mime.split('/')[0] == 'video':
            vid = cv2.VideoCapture(upload_file_path)
            height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
            width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)
            temp.append(upload_file.filename)
            temp.append(int(height))
            temp.append(int(width))
            temp.append(kind.extension)
            temp.append(kind.mime)
            file_list.append(temp)
        else:
            temp.append(upload_file.filename)
            temp.append('N')
            temp.append('N')
            temp.append(kind.extension)
            temp.append(kind.mime)
            file_list.append(temp)
    creative_class = classCreative.Creative()
    creative_class.set_campaign_macro_value(session['campaignName'])
    session['creative_macros'] = creative_class.macros
    return render_template('CreativeSetting.html', file_list=file_list, macros=session['creative_macros']
                           , creative_type=['Hosted Display','Hosted Native','Hosted Video'
                                            ,'Hosted Audio','Hosted Flash','Hosted HTML5','Third Party Display'
                                            ,'Third Party Video', 'Third Party Audio'])


@app.route('/skip_creative_upload', methods=["POST"])
def skip_creative_upload():
    session['skip_creative_upload'] = '1'
    creative_class = classCreative.Creative()
    creative_class.set_campaign_macro_value(session['campaignName'])
    session['creative_macros'] = creative_class.macros
    return render_template('CreativeSetting.html', file_list=[], macros=session['creative_macros'])


@app.route('/miaozhenfileUpload', methods=["POST"])
def miaozhenfileUpload():
    session['skip_creative_upload'] = "1"
    upload_path = session['upload_path']
    upload_file = request.files.getlist('upload_outside_file')[0]
    upload_file_path = os.path.join(upload_path, upload_file.filename)
    upload_file.save(upload_file_path)
    session['upload_file_path'] = upload_file_path
    miaozhen_obj = miaozhen.Miaozhen_Tracking(upload_file_path)
    sheets = miaozhen_obj.get_sheets()
    return render_template('please select excel sheet.html', sheets=sheets)


@app.route('/selected_excel_sheet', methods=["POST"])
def selected_excel_sheet():
    if session['skip_creative_upload'] == "1":
        selected_sheet_name = request.form.get("selected_radio")
        session['selected_sheet_name'] = selected_sheet_name

        # 开始解析秒针的监测文件内容
        miaozhen_obj = miaozhen.Miaozhen_Tracking(session['upload_file_path'])
        miaozhen_obj.select_sheet(selected_sheet_name)
        miaozhen_obj.init_name_seperator(request.form["name_sep"])
        session["name_sep"] = request.form["name_sep"]
        miaozhen_obj.generate_filter_pd()
        common = commonClass.Common()
        (fixed_name_lists, filtered_name_struct_list, suspact_size_list,
         suspact_market_list) = miaozhen_obj.get_tracking_name_struct_set(
            common.market, common.site)

        # 替换掉 秒针dataframes中的那么字段
        miaozhen_obj.set_pd_value(col=2, data_list=fixed_name_lists)
        miaozhen_file_content_lists = miaozhen_obj.get_list_from_filter_pd()

        # 将修复的fixed_name写进export项目目录中
        session['miaozhen_content_tmp'] = '{}miaozhen_file_content.tmp'.format(session["export_path"])
        with open(session['miaozhen_content_tmp'], "w", encoding='utf-8') as fw:
            json.dump(miaozhen_file_content_lists, fw)

        '''
        filtered_name_struct_list.format:
        [
            ['Hormel'], 
            ['Beef Jerky'], 
            ['Splash', 'Native Display', 'Display', 'Mobile Video'], 
            ['RTB', 'iQIyi', 'Youku', 'Tencent'], 
            ['Jingdong', 'Tianmao', 'Dingdong', 'Pupu'], 
            ['GZ', 'SZ', 'BJ', 'SH'], 
            ['600x300', 'Office 1080x2280', '960x540', 'Office_960x540', '640x360', '300x200', 'Office 1125x2436', '640x100', 'Office 720x1280', 'Camping_960x540', 'Office_1280x720', 'Office 640x960', '1280x720', '640x320', '960x640', 'Office 360x644', '480x320', 'Camping_1280x720', '1000x560'], 
        ]
        
        recommand_size_list.format:
        ['1280x720', '640x960', '1080x2280', '960x540', '720x1280', '1125x2436', '360x644']
        '''

        # recognise site
        recommand_site_list = []
        candidate_site_list = []
        for index, filtered_name_struct in enumerate(filtered_name_struct_list):
            recognised_sizes = list(set(filtered_name_struct).intersection(common.site))
            if len(recognised_sizes) > 0:
                recommand_site_list += recognised_sizes  # 精准记录site name
                candidate_site_list += filtered_name_struct_list[index]  # 记录疑似含有site name的列
        return render_template('init creative name.html',
                               # name_struct_list = filtered_name_struct_list,
                               recommand_size_list=suspact_size_list,
                               recommand_site_list=set(recommand_site_list),
                               candidate_site_list=set(candidate_site_list),
                               recommand_market_list=suspact_market_list,
                               sheet_name=selected_sheet_name,
                               display_item_num=5)


@app.route('/select_creative_name', methods=["POST"])
def select_creative_name():
    name_conversion_form = {}
    if 'recommand_site' in request.form.keys():
        name_conversion_form["recommand_site_list"] = request.form['recommand_site_list'].split(',')
        name_conversion_form["candidate_site_list"] = request.form['candidate_site_list'].split(',')
    if 'recommand_market' in request.form.keys():
        name_conversion_form["recommand_market_list"] = request.form['recommand_market_list'].split(',')
    if 'recommand_size' in request.form.keys():
        name_conversion_form["recommand_size_list"] = request.form['recommand_size_list'].split(',')

    r = generate_results_from_miaozhen_file(name_conversion_from=name_conversion_form)
    return flask.send_file(r)


def generate_results_from_miaozhen_file(name_conversion_from):
    '''
    输入参数 name_conversion_from 的格式：
    {
        "recommand_site_list"=[],
        "candidate_site_list"=[],
        "recommand_market_list"=[],
        "recommand_size_list"=[]
    }
    '''

    # with open( session[ 'miaozhen_content_tmp' ], "r", encoding='utf-8') as fr:

    result_obj = classResult.MiaozhenResult()
    with open(session['miaozhen_content_tmp'], "r", encoding='utf-8') as fr:
        outside_data_set = json.load(fr)
    result_file_name = result_obj.save_results_from_miaozhen_set(outside_data_set=outside_data_set,
                                                                 export_path=session['export_path'],
                                                                 result_file="{}_BulkCreativeImport_Result_v28.xlsx".format(
                                                                     session['campaignName']),
                                                                 name_conversion_from=name_conversion_from,
                                                                 name_sep=session['name_sep'])

    file_path = os.path.join(session['export_path'], result_file_name)
    return file_path


@app.route('/sumbitted')
def get_sumbitted():
    return render_template('submitted.html', creative_rules=session['creative_rules'])


@app.route('/add_rules', methods=['POST'])
def add_rules():

    if os.path.exists("{}rules.tmp".format(session['upload_path'])):
        with open("{}rules.tmp".format(session['upload_path'])) as fo:
            rules_list = json.load(fo)
    else:
        rules_list = []

    session['rules_file'] = "{}rules.tmp".format(session['upload_path'])
    # if len(request.form.get('Ag_list').split(",")) > 0 and session['Adgroup'] != request.form.get('Ag_list').split(","):
    #     session['Adgroup'] = request.form.get('Ag_list').split(",")
    #     return render_template('submitted.html', creative_rules=rules_list)

    # creative_type=['Hosted Display','Hosted Native','Hosted Video','Hosted Audio']
    # types = request.form.get('creative_type')
    # print(str(types))
    # print(request.form.get('files').split(","))
    if request.form['add_rule'] == 'Change Type':
    # if "not submit form" in request.form:
        pass
    elif request.form['add_rule'] == 'Add Rule':
        rules_list.append(
            {
                "creative_type":request.form.get('creative_type'),
                "creative_files": request.form.get('files').split(";"),
                "name": request.form.get('creative_name_rule'),
                "Description": request.form.get('Description_rule'),
                "Asset_File_Name": request.form.get('Asset_File_Name_rule'),
                "clickthrough_url": request.form.get('clickthrough_rule'),
                "landing_page_url": request.form.get('landing_page_rule'),
                "Impression_Tracking_url": request.form.get('Impression_Tracking_url'),
                "Native_Short_Title": request.form.get('Native_Short_Title'),
                "Native_Long_Title": request.form.get('Native_Long_Title'),
                "Native_Short_Description": request.form.get('Native_Short_Description'),
                "Native_Long_Description": request.form.get('Native_Long_Description'),
                "Sponsor": request.form.get('Sponsor'),
                "Click_Tracking_Parameter": request.form.get('Click_Tracking_Parameter'),
                "Width": request.form.get('Width'),
                "Height": request.form.get('Height'),
                "AdTag": request.form.get('AdTag'),
                "VAST_XML_URL": request.form.get('VAST_XML_URL'),
                "Adgroup_name": request.form.get('Ag_list').split(",")
            }
        )
    # print(rules_list)
    with open("{}rules.tmp".format(session['upload_path']), "w") as fo:
        json.dump(rules_list, fo)
    return render_template('submitted.html', creative_rules=rules_list)

# @app.route('/creative_type', methods=['GET'])
# def dropdown():
#     creative_type=['video','display']
#     return render_template('submitted.html', creative_type=creative_type)

@app.route('/delete_last_rule', methods=['POST'])
def delete_last_rule():
    # delete the last rule of creative_rules list
    if os.path.exists("{}rules.tmp".format(session['upload_path'])):
        with open("{}rules.tmp".format(session['upload_path'])) as fo:
            rules_list = json.load(fo)
        # else:

    # else:
    #     rules_list = []
    session['rules_file'] = "{}rules.tmp".format(session['upload_path'])
    # rules_list.append(
    #     {
    #         "creative_files": request.form.get( 'files' ).split(","),
    #         "name": request.form.get('creative_name_rule'),
    #         "Description": request.form.get('Description_rule'),
    #         "Asset_File_Name": request.form.get('Asset_File_Name_rule'),
    #         "clickthrough_url": request.form.get('clickthrough_rule'),
    #         "landing_page_url": request.form.get('landing_page_rule')
    #     }
    # )
    if len(rules_list) > 0:
        rules_list.pop(-1)
    with open("{}rules.tmp".format(session['upload_path']), "w") as fo:
        json.dump(rules_list, fo)

    # session['creative_rules'].pop(-1)
    return render_template('submitted.html', creative_rules=rules_list)


@app.route('/output')
def exportXlsx():
    # creative_upload_path = os.path.abspath( se_upload_path )
    # result_export_path = os.path.abspath( se_export_path )
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
    with open(session['rules_file'], 'r') as fo:
        creative_rules = json.load(fo)
    resultObj.generate_results(creative_rules=creative_rules, macros=session['creative_macros'],
                               creative_path=session['upload_path'], export_path=session['export_path'])
    result_file_name = resultObj.export_to_excel(
        path=session['export_path'],
        name="{}_BulkCreativeImport_Result_v30.xlsx".format(session['campaignName'])
    )
    file_path = os.path.join(session['export_path'], result_file_name)
    return flask.send_file(file_path)


@app.route('/empty')
def empty():
    # clean creative_rules list
    session['creative_rules'].clear()
    # 清空 export folder
    directory = os.path.abspath(session['export_path'])
    for f in os.listdir(directory):
        os.remove(os.path.join(directory, f))
    # 清空 upload folder
    directory = os.path.abspath(session['upload_path'])
    for f in os.listdir(directory):
        os.remove(os.path.join(directory, f))
    return render_template('chooseFile.html')


@app.route('/download_zip')
def download():
    exportXlsx()
    from flask import send_file
    from glob import glob
    from io import BytesIO
    from zipfile import ZipFile

    stream = BytesIO()
    with ZipFile(stream, 'w') as zf:
        for root, subdirs, files in os.walk(session['export_path']):
            for filename in files:
                zf.write(os.path.join(root, filename))
    stream.seek(0)

    return send_file(
        stream,
        as_attachment=True,
        download_name='{}_BulkCreativeImport_Result.zip'.format(session['campaignName'])
    )


@app.route('/creative_upload/', methods=['POST'])
def creative_upload():
    return render_template('creative_upload.html')


app.secret_key = 'tz.Feb.2023'
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port='27804')
    app.run(host='127.0.0.1', port='80')
    # webview.start()
