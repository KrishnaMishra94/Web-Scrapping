import pandas as pd 
from selenium import webdriver 
import re  ## FOR PERFORMING TEXT CLEANING
import datetime 
from dateutil.relativedelta import relativedelta ## FOR FINDING TIME DIFFERENCE

job_lists   = pd.DataFrame(columns=['JOB CATEGORY','JOB TITLE','JOB TYPE','JOB LOCATION','EXPERIENCE REQUIRED','POSTING TIME'])

################################## SESSION CREATION ########################################
driver      = webdriver.Chrome() ## USING CHROME DRIVER
url         = "https://techolution.app.param.ai/jobs/"  ## URL TO CRAWL
driver.get(url)

div_parent_nodes    = driver.find_elements_by_css_selector("div.ui.segments")
i=0
for div_parent in div_parent_nodes:        
    job_category    = div_parent.find_element_by_css_selector("div.ui.segment").text    
    div_nodes       = div_parent.find_elements_by_css_selector("div.ui.segment.job_list_card")
    
    for div in div_nodes:
        job_title   = div.find_element_by_tag_name('h3').text
                
        span_nodes  = div.find_elements_by_tag_name('span')
        
        details = []
        for span in span_nodes:        
            if(re.search('^\W+$',span.text)):
                continue
            else:
                txt = re.sub('\W+$','',span.text)
                details.append(txt)
                
        job_lists.loc[i,'JOB TITLE']            = job_title
        job_lists.loc[i,'JOB CATEGORY']         = job_category                
        job_lists.loc[i,'JOB TYPE']             = details[0]
        job_lists.loc[i,'JOB LOCATION']         = details[1]
        job_lists.loc[i,'EXPERIENCE REQUIRED']  = details[2]
        job_lists.loc[i,'POSTING TIME']         = details[3]
        i+=1
driver.quit()
#############################################################################################

################################### HANDLING TIME COMPONENT ################################
def text_to_date(df,old_column,new_column):    
    for i in range(len(job_lists)):        
        time = df.loc[i,old_column].split()[:2]
        count , unit = time[0],time[1]
        
        if( (count == 'a') or (count == 'an')):
            count = 1
        count = int(count)
           
        if(re.search('month',unit)):
            time = datetime.datetime.strptime('12/01/18 11:59:59', '%m/%d/%y %H:%M:%S') - relativedelta(months=count)
        elif(re.search('year',unit)):
            time = datetime.datetime.strptime('12/01/18 11:59:59', '%m/%d/%y %H:%M:%S') - relativedelta(years=count)
        elif(re.search('day',unit)):
            time = datetime.datetime.strptime('12/01/18 11:59:59', '%m/%d/%y %H:%M:%S') - relativedelta(days=count)
        elif(re.search('hour',unit)):
            time = datetime.datetime.strptime('12/01/18 11:59:59', '%m/%d/%y %H:%M:%S') - relativedelta(hours=count)
        elif(re.search('minute',unit)):
            time = datetime.datetime.strptime('12/01/18 11:59:59', '%m/%d/%y %H:%M:%S') - relativedelta(minutes=count)
        elif(re.search('second',unit)):
            time = datetime.datetime.strptime('12/01/18 11:59:59', '%m/%d/%y %H:%M:%S') - relativedelta(seconds=count)              
            
        df.loc[i,new_column] = time


###### CALLING FUNCTION ########
text_to_date(job_lists,'POSTING TIME','DUMMY POSTED DATE')    


#############################################################################################


################################# DATA SAVING TO CSV ########################################
job_lists.sort_values(by='DUMMY POSTED DATE',inplace=True)
job_lists = job_lists.loc[:,job_lists.columns != 'DUMMY POSTED DATE']
job_lists.to_csv('Techolution_Job_Postings.csv',index=False)
#############################################################################################

