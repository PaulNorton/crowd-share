![CrowdShare](media/promo.jpg) 
#CrowdShare
A python app where users can host an event and collect pictures posted with the event hashtag

### Dependencies: ###

* Built for Python 3: https://www.python.org/downloads/
* User must have the AWS CLI installed and set up with default credentials: https://aws.amazon.com/cli/
* Install the following PyPI packages:
	1. Twitter client: `pip3 install twython`
	2. Python imaging library: `pip3 install pillow`
	3. Python requests library: `pip3 install requests` 
	4. AWS Boto3 library: `pip3 install boto3`

### Installation: ###

* Clone crowd-share: `git clone https://github.com/PaulNorton/crowd-share.git`
* Run setup.py and follow instructions: `python3 setup.py`
* Run crowdshare.py: `python3 crowdshare.py`

### Usage: ###

* While app is running, post pictures to Twitter or Instagram (make sure account is public) with the hashtag for your event
* People may also send pictures via a Twitter direct message to the account the app is registered under
* Pictures will begin to appear and cycle on the screen
