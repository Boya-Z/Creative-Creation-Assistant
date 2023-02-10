from flask import Flask, render_template, request, send_file, make_response
from datetime import timedelta
import requests, json, socket, os
import time, re
import static.Creative_Class as classCreative
import static.FileImport as fileimport

app = Flask(__name__, template_folder='templates', static_folder='static')
app.add_template_filter(enumerate)


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
    return render_template('CampaignName.html',
                           campaign_name_macro=classCreative.Creative.macros["campaign_name_macro"])


@app.route('/CampaignNameSetting', methods=['POST'])
def CampaignNameSetting():
    campaignName = request.form.get("campaign_name")
    campaignMacroKey = request.form.get("campaign_macro_key")
    creative = classCreative.Creative()
    creative.set_campaign_macro_key(campaignMacroKey)
    creative.set_campaign_macro_value(campaignName)
    # 如果有历史记录数据，则将其值传入exsiting_data一起返回界面
    return render_template('index.html')


@app.route('/viewMacros')
def viewMacros():
    print(classCreative.Creative.macros)
    return render_template('viewMacros.html', macros=classCreative.Creative.macros)


@app.route('/chooseFile')
def chooseFile():
    return render_template('chooseFile.html')


# 多个文件上传时候的代码：
@app.route('/fileUpload', methods=["POST"])
def fileUpload():
    context = {}
    context['uploaded_number'] = len(request.files)
    upload_files = request.files.getlist('file')
    for upload_file in upload_files:
        upload_path = os.path.join('upload', upload_file.filename)
        upload_file.save(upload_path)
    # print(upload_files)
    # return 'file uploaded successfully'

    return render_template("fileSuccess.html", name=upload_files)


# @app.route('/fileUpload', methods=['POST'])
# def fileUpload():
# for data in request.files:
#     f = request.files['file']
#     f.save(os.path.abspath("./upload{}".format(f.filename)))

# uploaded_file = request.files.getlist('file')
# for uploaded_file in request.files.getlist('file'):
#     if uploaded_file.filename != '':
#         uploaded_file.save(uploaded_file.filename)
# return render_template('index.html')

@app.route('/fileSuccess')
def fileSuccess():
    return render_template('fileSuccess.html')


@app.route('/CreativeSetting')
def CreativeSetting():
    from os import listdir
    files = []
    for x in os.listdir(os.path.abspath("./upload")):
        files.append(x)

    return render_template('CreativeSetting.html', files=files)


@app.route('/rules', methods=['POST'])
def rules():
    Name = request.form.get("campaign_name")
    clickthrough = request.form.get("clickthrough")
    landing_page = request.form.get("landing_page")

    files = request.form.get("creative_files")
    print(files)
    custom_rules = fileimport.FileImport()
    custom_rules.add_rules(Name, files, clickthrough, landing_page)
    print(custom_rules.custom_rules)
    # creative = classCreative.Creative()
    # fileimport.set_campaign_macro_key(clickthrough)
    # fileimport.set_campaign_macro_value(landing_page)
    # 如果有历史记录数据，则将其值传入exsiting_data一起返回界面
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
    # app.run(host='127.0.0.1', port='80')
