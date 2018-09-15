

<p align="left">
<img src="https://github.com/ConnorSMaynes/monster/blob/master/monster/logo.png" alt="Monster.com Unofficial API" >
</p>

A simple unofficial api for Monster.com job board.

Completely headless. Everything runs on python requests.

## Methods

- `login` : Login to Monster.com with your email and password.
- `search` : search for jobs. returns a list of search results named tuples with ApplyLink ( quick apply job link ) and DetailsLink ( link to job desciption and other job details ). generator. The following filters are supported:
  - keywords
  - posted x days ago
  - type ( full-time, internship, temporary )
- `apply` : apply to the job at the given url ( ApplyLink ) returned from `search`
- `batchApply` : apply to a bunch of jobs at once. progress bar.
- `getJobDetails` : get details on a given job from the DetailsLink of the search result returned from `search`. This method will also accept a job id or the apply url and will lookup the job details.

## Installation

```bash
pip install git+git://github.com/ConnorSMaynes/monster
```

## Usage

```python
from monster import Monster

# LOGIN
m = Monster()
if m.login( USERNAME, PASSWORD ):

      # BATCH APPLY TO JOBS
      z.batchApply( m.search( quantity=5, keywords='developer' ) ) # apply to a bunch of jobs with progress bar.

      # APPLY TO JOBS AND GET DETAILS
      Jobs = z.search( quantity=5, keywords='developer' )
      for Job in Jobs:                                            # apply to jobs and do some other stuff
          JobDetails = z.getJobDetails( Job )                       
          AppResult = z.apply( Job )
          if AppResult:
              print( JobDetails )
```

## Similar Projects

This project was inspired by others:
- [getJob](https://github.com/jonathanhwinter/getJob)
- [ZipRecruiterHack](https://github.com/Original-heapsters/ZipRecruiterHack)

## License

Copyright © 2018, [ConnorSMaynes](https://github.com/ConnorSMaynes). Released under the [MIT](https://github.com/ConnorSMaynes/ziprecruiter/blob/master/LICENSE).
