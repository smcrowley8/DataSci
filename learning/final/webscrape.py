"""Web scarper classes and methods for getting relevant patent data"""
from datetime import date, timedelta
from selenium import webdriver
import time
#set up selenium for global run

SEARCH_SITE = "https://patft.uspto.gov/netahtml/PTO/search-adv.htm" 

def appendDict(d1, d2):
    for k, vals in d2.items():
        d1[k]+=vals 
    return d1

def getPatentData(patentLink, driver):
    results={
        'Inventors':[],
        'Assignee':[],
        'Family_ID':[],
        "AppNum":[],
        'Filed':[],
    }
    
def getResults(baseURL, driver:webdriver):
    results={
        'Inventors':[],
        'Assignee':[],
        'Family_ID':[],
        "AppNum":[],
        'Filed':[],
    }
    patentTable = driver.find_element_by_xpath('/html/body/table/tbody')

    patentLinks = driver.find_elements_by_xpath('/html/body/table/tbody/tr/td/a')
    for patentLink in patentLinks:
        print(f'{patentLink=}')
        patentLink.click()
        time.sleep(2)
        patentInfoTable = driver.find_element_by_xpath('/html/body/table[3]/tbody')
        patentInfoHead = patentInfoTable.find_element_by_xpath('//th')
        patentInfo = patentInfoTable.find_element_by_xpath('//td//b')
        print('info',patentInfo.text)
        print('head',patentInfoHead.text)
        '''for i in range(len(patentInfoHead)):
            if patentInfoHead[i].text in results.keys():
                results[patentInfoHead[i].text].append(patentInfo[i].text)'''
        #results['Inventors'].append(driver.find_element_by_xpath('/html/body/table[3]/tbody/tr[1]/td').text)
        #results['Assignee'].append(driver.find_element_by_xpath('/html/body/table[3]/tbody/tr[2]/td/b').text)
        #results['AppNum'].append(driver.find_element_by_xpath('/html/body/table[3]/tbody/tr[4]/td/b').text)
        #results['Family_ID'].append(driver.find_element_by_xpath('/html/body/table[3]/tbody/tr[3]/td/b').text)
        #results['Filed'].append(driver.find_element_by_xpath('/html/body/table[3]/tbody/tr[5]/td/b').text)
    driver.get(baseURL)
    time.sleep(2)

    nextPageBtn=None
    try:
        nextPageBtn = driver.find_element_by_xpath('/html/body/center[2]/table/tbody/tr/td/a[1]')
        nextPageBtn.click()
        time.sleep(3)
    except(Exception):
        print('next page button not found, more pages for this date search')
        return results 
    nextBaseURL = driver.current_url
    nextResults = getResults(nextBaseURL, driver)
    return appendDict(results, nextResults)

def queryDate(date:str, driver:webdriver):
    
    #searchbox:
        # id = "mytextarea", name="Query"
    #inputBtn:
        # value = "Search", type = "SUBMIT", xpath = "/html/body/center/form/table/tbody/tr[2]/td[2]/input[1]"
    driver.get(SEARCH_SITE)
    time.sleep(2)
    searchInputBox = driver.find_element_by_id("mytextarea")
    searchInputBox.send_keys(date)
    time.sleep(1)
    submitBtn = driver.find_element_by_xpath("/html/body/center/form/table/tbody/tr[2]/td[2]/input[1]")
    submitBtn.click()
    time.sleep(2)
    baseResultUrl = driver.current_url
    return getResults(baseResultUrl, driver)

def buildCSV(startDate:date, endDate:date, filename:str, driver:webdriver):
    """Saves a csv of patent data over given timeframe
    
    Args:
        startDate: start date we want to start scraping patent info from
        endDate: date we want to stop scarping data from
        filename: name of csv file to save patent date to
        
    Returns:
        list of ints of form YYYYMMDD

    """
    with open(filename, "w") as f:
        while startDate<=endDate:
            dateQuery = "APD/"+str(startDate.month)+"/"+str(startDate.day)+"/"+str(startDate.year)
        
            ############# do query in patent search
            queryResults = queryDate(dateQuery, driver)
            ############# save all data from that search in csv, if missing that col gets "NA"
            print(queryResults)
            #move to next date
            startDate+=timedelta(days=1)
    
def main():
    driver = webdriver.Chrome(executable_path='/home/ubuntu/Downloads/engines/chromedriver')

    startDate=date(2015, 12, 25)
    endDate = date(2016,1,1)
    filename="patentData.csv"
    buildCSV(startDate, endDate, filename, driver)

    


if __name__=="__main__":
    main()