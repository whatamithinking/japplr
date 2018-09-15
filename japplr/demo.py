
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
    ,global_filters={ 'type':'full_time','posteddaysago':7 }
)
j.login()
j.run( quantity_per_search=10, schedule_every_mins=15 )