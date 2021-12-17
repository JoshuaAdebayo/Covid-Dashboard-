# Covid-Dashboard
In this repository I have made a dashboard that presents covid related data upon a dashboard 

## 1. Download

There are 2 ways this can be done:

1. Clone the git repository and navigate to the directory as shown below via Git Bash

```bash
git clone https://github.com/JoshuaAdebayo/Covid-Dashboard
```

2. Download directly from [https://github.com/JoshuaAdebayo/Covid-Dashboard]
3. (https://github.com/JoshuaAdebayo/Covid-Dashboard)

## 2. Installation

Install the package dependencies using the "required_docs.txt" file as shown below.
This can be done into a virtual environment but is not required:

1. Virtual Environment

Windows:
```bash
pip install -r requirements.txt
```

Mac/Linux:
```bash
pip install -r requirements.txt
```

2. No Virtual Environment

```bash
pip install -r requirements.txt
```

## 3. Navigate to the project directory

## 4. Setup Virtual Environment (This next step is only required if the package dependencies were installed into a virtual environment)

Activate the virtual environment.
To check if it is or has already been activated, (venv) should appear before the console line.

Windows:
```bash
.\venv\Scripts\activate
```

Mac/Linux:
```bash
./venv/bin/activate
```

## 5. Running the flask application

Windows:
```bash
set FLASK_APP=flaskr
flask run
```

Mac/Linux:
```bash
export FLASK_APP=flaskr
flask run
```

## 6. Load webpage

Type in the following URL into the browser to navigate to the webpage: [http://localhost:5000/index] and [http://localhost:5000] / (http://localhost:5000/index), (http://localhost:5000)

## 7. How to use the application

The middle of the dashboard contains information regarding the number of cases in the last 7 days both locally and nationally, the total number of national hospital cases and the total number of national deaths.

The right of the dashboard contains a list of news articles. 
The subject of these news articles will depend on the value in the config file which will be discussed later. 
A news article can be closed by clicking on the x button in the top right corner of its tab. 
Once a certain news article is closed, it will not reappear when the page is refreshed or an update has run (Updates are explained below).

The left of the dashboard contains a list of scheduled updates. 
A scheduled update can be cancelled by clicking on the x button in the top right corner of its tab. 

To schedule one of these updates, in the centre of the dashboard, give the update a title (this is required), the time you want the update to run, whether you want to update the covid data or news or both and whether you want this update to repeat every 24 hours.
Finish by clicking the Submit button.

## 8. Configuration file

The config file is found in the "flaskr/" directory under the name "config.json". 
Editing the values of the parameters in this file will change what is displayed on the dashboard.
Below is a list of all the parameters in each section and what they do.

## "Main details":

"favicon" - specifies the name of the file which contains the favicon. E.g:

```json
"favicon" : "favicon.ico",
```

"Location" - specifies the local location from which the covid data is being fetched from. E.g:

```json
"Location" : "Sheffield",
```

"Location_Type" - specifies the type of location of the local location. E.g:

```json
"Location_Type" : "ltla",
```

"Nation" - specifies the national location from which the covid data is being fetched from. E.g:

```json
"Nation" : "England",
```

"Nation_type" - specifies the type of location of the national location. E.g:

```json
"Nation_Type" : "nation",
```

"Title" - specifies the title displayed at the centre of the dashboard. E.g:

```json
"title" : "Covid Dashboard",
```

"Key" - specifies the apiKey. E.g:

```json
"Key" : "a067b5a85a164a3eaa93431f141c6810",
```

Url" - specifies the url. E.g:

```json
"Url" : "https://newsapi.org/v2/everything",
```

"terms" - specifies the terms that are the subjects of the news articles. E.g:

```json
"terms" : "Covid COVID-19 coronavirus",
```

"Sort" - specifies the order in which the news articles are returned.
This can be changed with values found on [https://newsapi.org/docs/](https://newsapi.org/docs/). E.g:

```json
"Sort" : "publishedAt",
```

"language" - specifies the language the news articles are returned in. E.g:
```json
"language" : "en",
```

## "Logging":

"file" - specifies the location of the log file. E.g:

```json
"file" : "flaskr/logs/logging.log",
```

"format" - specifies the format the logger will output in the log file. E.g:

```json
"format" : "{asctime} {levelname:<8} {message}",
```

"level" - specifies the logging level. E.g:

```json
"level" : 10,
```

"filemode" - specifies the number of days ago you want the articles to come from. E.g:

```json
"filemode" : "w",
```