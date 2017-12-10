# NECTATZScrapper
A pyhton script that uses lxml package and xpath to navigate a page, scrap needed information and write it to either a csv file or a json file

### Description

NECTATZScrapper is a python script written for the Tanzania necta results pages to scrap out subject performance data and gender performance related information. It requests and scraps the page for schools results url list `http://www.necta.go.tz/results/2016/csee/index.htm` and loops through each school url requesting it page and scrapping it i.e `http://www.necta.go.tz/results/2016/csee/results/s0101.htm` 

### Clone the repository
```shell
git clonegit@github.com:CodeForTanzania/NECTATZScrapper.git
```

### Install Packages
```
pip install lxml
pip install requests
```

### To run the scripts
```
python start.py
```
