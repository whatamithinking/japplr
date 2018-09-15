

<p align="center">
<img src="https://github.com/ConnorSMaynes/japplr/blob/master/japplr/logo.png" alt="Japplr Auto Job Applier">
</p>

Automatically apply to jobs.

## Pitch

```
Looking for a job?
What if you could be 
	Everywhere at once? 
	In every job database on the planet? 
	On every recruiter's desk?
	In every company's HR department?
Japplr makes being an omnipresent terrifying job applying daemon possible with a just few lines of code.
Welcome to your future, 
	Welcome...
		To...
			Japplr
```

## Attributes

- `accounts` : Dictionary of each site name and an instance of that API
    ```python
    accounts = {
      'ziprecruiter'  :   {
        'email'     :   EMAIL
        ,'password' :   PASSWORD
        ,'enabled'  :   True
      }
      ,'monster'  :   {
        'email'     :   EMAIL
        ,'password' :   PASSWORD
        ,'enabled'  :   True
      }
    }
    ```
- `global_filters` : Global filters to apply to all searches. These can be overridden by local filters in a search.
  ```python
  { 
    'type'          : 'full_time'
    ,'posteddaysago': 7
    ,'salary'       : 100000
  }  
  ```
- `searches` : List of dictionaries. Each dictionary contains a set of filters to apply to that specific search. Local filters override global filters
  ```python
  my_searches = [
    { 'keywords' : 'python programmer' }
    ,{ 'keywords' : 'sql programmer' }
    ,{ 'keywords' : 'SCADA programmer' }
  ]
  ```
  
## Methods

- `login` : Login to each of your enabled accounts.
  - `accounts` : Dictionary of accounts. Use Enabled key to enable/disable different accounts, so they are used/ignored in `run`
- `run` : Run `Japplr`, applying to jobs on all job boards
  - `quantity_per_search` : Max number of jobs to apply to per schedule of run
  - `schedule_every_mins` : How many minutes to wait before running through all searches all for all enabled accounts.
  - `give_up_on_search_secs` : How many seconds to wait for a search to finish before giving up. Default is 0, which automatically calculates a number of seconds to wait before giving up. If -1, then will not give up until we run out of pages in the search results.

## Installation

```bash
pip install git+git://github.com/ConnorSMaynes/japplr
```

## Usage

NOTES: 
- Replace EMAIL and PASSWORD with your own.
- You should setup filters in your email to filter out the "resume received" emails you get every time you apply to something, the "unfortunately" emails every time you get a rejection, and the "interview" emails for when you get an email.

```python
from japplr import Japplr

my_searches = [
	{ 'keywords' : 'automation engineer' }
	,{ 'keywords' : 'test automation engineer' }
	,{ 'keywords' : 'electrical engineer' }
	,{ 'keywords' : 'integration engineer' }
	,{ 'keywords' : 'automation developer' }
	,{ 'keywords' : 'python developer' }
	,{ 'keywords' : 'inductive automation ignition' }
	,{ 'keywords' : 'python programmer' }
	,{ 'keywords' : 'database developer' }
	,{ 'keywords' : 'sql programmer' }
	,{ 'keywords' : 'dev ops' }
	,{ 'keywords' : 'SCADA programmer' }
	,{ 'keywords' : 'HMI programmer' }
]

accounts = {
	'ziprecruiter'  :   {
		'email'     :   EMAIL
		,'password' :   PASSWORD
		,'enabled'  :   True
	}
	,'monster'  :   {
		'email'     :   EMAIL
		,'password' :   PASSWORD
		,'enabled'  :   True
	}
}

j = Japplr(
    accounts=accounts
    ,searches=my_searches
    ,global_filters={ 'type':'full_time','posteddaysago':7, 'salary':100000 }
)
j.login()
j.run( quantity_per_search=10, schedule_every_mins=15 )
```

## Similar Projects

This project was inspired by others:
- [ziprecruiter](https://github.com/ConnorSMaynes/ziprecruiter)
- [monster](https://github.com/ConnorSMaynes/monster)

## License

Copyright © 2018, [ConnorSMaynes](https://github.com/ConnorSMaynes). Released under the [MIT](https://github.com/ConnorSMaynes/japplr/blob/master/LICENSE.txt).
