
from ziprecruiter import ZipRecruiter
from monster import Monster
from tqdm import trange, tqdm
import schedule, time, traceback
import threading

SITES = {
	'ziprecruiter'	:	ZipRecruiter
	,'monster'		:	Monster
}

class Japplr():
	__api_throttle_secs = 3

	def __init__( self, accounts={}, searches=[], **global_filters ):
		''' Login to each enabled and supported job board account in the accounts dict.

		Args:
			accounts (dict,optional): Dictionary of each job board account in the following format.
				accounts = {
					'ziprecruiter': { 'email':Z_EMAIL, 'password':Z_PASSWORD, 'enabled':True }
					,'monster': { 'email':M_EMAIL, 'password':M_PASSWORD, 'enabled':True }
					,...
				}
				Unsupported accounts included in this dictionary will be ignored.
			searches (list): List of dictionaries, where each dictionary contains a different
				set of filter criteria.
			global_filters (dict): Dictionary of global filters to apply to all searches. If a
				search contains that filter already, the search's filter will be used instead
				of the global filter.

		Returns:
			Nothing
		'''
		self.__logged_in = False
		self.accounts = accounts
		self.searches = searches
		self.global_filters = global_filters
		self.sites = {}

	@property
	def api_throttle_secs(self):
		'''Get the current api throttle seconds, which limits amount of calls per second.'''
		return self.__api_throttle_secs

	@api_throttle_secs.setter
	def api_throttle_secs(self,val):
		'''Set the api throttle seconds, if not currently logged in.

		Args:
		    val (int): Number of seconds required between api calls

		Returns:
		    None
		'''
		if not self.__logged_in:
			self.__api_throttle_secs = val
		else:
			raise Exception( 'ERROR : API THROTTLE SECS CANNOT BE EDITTED ONCE LOGGED IN' )

	def login( self, accounts=None ):
		''' Login to each site in the accounts dictionary.

		Logging in creates a new instance for each job board site. After an instance
		of a job board site has been created the api_throttle_secs cannot be changed.

		Args:
			accounts (dict,optional): Dictionary of each job board account in the following format.
				accounts = {
					'ziprecruiter': { 'email':Z_EMAIL, 'password':Z_PASSWORD, 'enabled':True }
					,'monster': { 'email':M_EMAIL, 'password':M_PASSWORD, 'enabled':True }
					,...
				}
				Unsupported accounts included in this dictionary will be ignored.

		Returns:
			bool: True if successful. Exception otherwise.
		'''
		self.__logged_in = False
		if isinstance( accounts, dict ):
			self.accounts = accounts
		for site, account in self.accounts.items():
			if site in SITES:

				# IF ACCOUNT ENABLED, PROCEED WITH LOGGING IN. IF ENABLED NOT IN ACCOUNT DICT, ASSUME ACCOUNT ENABLED.
				if 'enabled' in account and not account[ 'enabled' ]:
					print( 'INFO  : {0} : ACCOUNT DISABLED, SKIPPING LOGIN'.format( site.title() ) )
					continue

				# LOGIN TO SITE
				site_instance = SITES[ site ]()
				site_instance.api_throttle_secs = self.api_throttle_secs
				if not site_instance.login( account[ 'email' ], account[ 'password' ] ):
					raise ValueError( 'ERROR : {0} : COULD NOT LOGIN TO YOUR ACCOUNT : {1} : {2}'.\
						format( site, str( account[ 'email' ] ), account[ 'password' ] ) )
				else:
					print( 'INFO  : {0} : LOGIN SUCCESSFUL'.format( site.title() ) )
				self.sites.update( { site : site_instance } )
			else:
				print( 'INFO  : {0} : SITE NOT SUPPORTED. SKIPPING LOGIN'.format( site.title() ) )
		self.__logged_in = True
		return True

	def run( self, quantity_per_search=10, schedule_every_mins=30, give_up_on_search_secs=0 ):
		'''Apply to jobs using each search in searches for each job site in accounts.

		Args:
			quantity_per_search (int): Max jobs to apply to for each search for each job site.
			schedule_every_mins (int): The number of minutes between runs of the searches
				and applications to those search results. If <= 0, then do not schedule and
				the searches will all run once.
			give_up_on_search_secs (int): The number of seconds to wait before giving up on
				a search and not going to any more pages for that search to try to find
				a job that has not been applied to.

		Returns:
			Nothing
		'''
		if give_up_on_search_secs == -1:							# if negative time to fill search, give infinite
			give_up_on_search_secs = 9999
		elif give_up_on_search_secs == 0:							# if 0 time, then assume formula
			expected_results_per_page = 0.5							# expect one usable result every 2 pages visited
			pages_needed = int( quantity_per_search / expected_results_per_page )
			time_spent_getting_pages = self.api_throttle_secs * pages_needed
			time_spent_applying = self.api_throttle_secs * quantity_per_search
			give_up_on_search_secs = time_spent_getting_pages + time_spent_applying

		def apply_to_jobs_for_site( site ):
			'''Iterate over each search and apply to jobs matching those filters for this site.

			Args:
				site (str): The name of the job board site to apply for jobs on.

			Returns:
				Nothing
			'''
			total = len( self.searches ) * quantity_per_search
			pbar = trange( 
				total
				,desc=site.title() + ' | Applying'
				,unit='Jobs'
				,leave=False 
			)
			
			for search in self.searches:
				pbar.set_description( site.title() + ' | ' + search['keywords'].title() + ' | Applying' )
				pbar.refresh()
				def run_search_and_apply():
					search_filters = self.global_filters
					search_filters.update( search )
					try:
						search_results = self.sites[ site ].search(
							quantity_per_search
							,**search_filters
						)
						for search_result in search_results:
							if self.sites[ site ].apply( search_result ):
								pbar.update( 1 )
					except:
						traceback.print_exc()

				t = threading.Thread( target=run_search_and_apply )
				t.start()
				t.join( give_up_on_search_secs )
				if t.isAlive():
					pbar.set_description( site.title() + ' | ' + search['keywords'].title() + ' | TIMEOUT FOR SEARCH!' )
					pbar.refresh()
					time.sleep( 3 )

		# START APPLYING FOR EACH JOB SITE AND SCHEDULE EACH SITE TO RUN EVERY SO OFTEN
		threads = []
		for site in self.sites:
			t=threading.Thread( target=apply_to_jobs_for_site, args=( site, ) )         # start running immediately
			t.daemon = True
			t.start()
			threads.append(t)
			if schedule_every_mins > 0:
				schedule.every( schedule_every_mins ).minutes.do(
						apply_to_jobs_for_site
						,site=site
					)                                                                   # schedule to run later
		[ t.join() for t in threads ]

		# INFINITE LOOP TO CONTINUE RUNNING SCHEDULE
		while True:
			schedule.run_pending()
			time.sleep(1)
