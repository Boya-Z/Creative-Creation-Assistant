# Creative-Creation-Assistant
 
What Is The Business Problem The App Is Solving?

During the campaign creative setup, clients would often provide a list of creative files and websites. Account managers would need to bulk import creatives by filling out the template spreadsheet. The spreadsheet needs to include the following columns:

Names: usually contain information such as campaign name, file size, advertiser name, and campaign regions which need to change for each line
Asset File Name: same file name might appear several times for the same creatives
Clickthrough URL & Clickthrough URL:  many short character fields need to be replaced several times

This manual typing process is often complex, involves too many "copy and paste" commands, and can take hours if many creative files and long website URLs are involved.




Is there a specific region or market this applies to?




What Are Case Studies Where This Provided Value

One sentence summary of impact of the logic being developed per case study is recommended

Who Are The Primary Stakeholders?

App Developers: 

Tony Zhang Boya Zeng boya.zeng@thetradedesk.com




Non-App Developers:

Insert the names of the non-app developers




Who are the reviewers?

Parking Lot Attendants

Anyone within @parking-lot-attendents







Describe The App Design

Describe how the app works, including any/all technologies or packages used

Use python to run on a website (server), upload files from the local directory, and download the result files to a local directory.

Language: HTML, CSS, Python, Javascript, 

import flask,os
from flask import Flask, render_template, request
from PIL import Image
Font Awesome Kit for icon in web page

Input

 creative files(usually pictures)
 campaign name, name format, clickthrough page URL format, landing page URL format

Output:

creative bulk import spreadsheet in template excel format 




The app interface:

Click 'Campaign Name': set up the campaign name by typing in

Click "View All Macros": view the macros we can use/already saved

Click 'Creative File'→Click 'Choose file' to choose creative files→

Click 'save' will save the file and direct you to set the rules→

Check the file you wish to display in the spreadsheet, fill in the creative name, and URL of the landing page and click_through page.→

Click 'Add Settings' to view what would be shown in the spreadsheet →

Click 'Download Results' to get the auto-filled spreadsheet→

Click the lower left downloaded file to view the spreadsheet

Click 'Enable Editing'→save the file →

ready to upload the file!




upload the spreadsheet together with the creative files.







Next Step:

link to internal API: search campaign name by its campaign ID through "Campaign Name" on the left side menu

What Data is Used In Creating The Insights

From Advertiser or Agency：

creative files， landing page URL, and Click Through URL which need to upload to Solimar

From Internal：

API to search campaign name by its ID




What Data Is Created From The App? (If Any)

Are any derivative data sets created? If so where, what columns are saved, and what is the data retention?




Does The App Directly Access External Data Sources?

Yes 

	

No 



 
	
 







Who Will Have Access To The App/Who Are the Primary Customers?

TTD Account Managers










What Criteria Should We Use To Determine Whether To Deprecate The App Or Move To a Full Feature?

Factors to consider: (1) Usage frequency (Business Impact， multiple users at the same time)  (2) User experience (More Integration/Automation) （3）If integration with Solimar is needed
