# savingsplanhelper
Python script to help determine savings plan commitment


# Instructions

```sh
# Install enviroment
virtualenv venv -p python3
source venv/bin/activate
pip3 install -r requirements.txt

# Make script executable
chmod +x graph.py
```

## Data source
Make sure to download the cost report as a csv from AWS. 
    * insert screenshot *

```sh
report.csv|head -1|sed 's/ //g' > usage.csv
report.csv|grep BoxUsage >> usage.csv
```

### Run application
```sh
python3 graph.py
# or
./graph.py
```

#### Important Notice
The [AWSPricing module](https://github.com/lyft/awspricing) can take a while to download since it may download a cache of ~1.5GB. Let it go, the script will let you know when it is done downloading.


