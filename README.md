## Parser for calling Watson Alchemy News API and save the results

### Install requirements
Clone/Download the project, change directory `cd` to the folder.

Install python requirements with [pip]():

```
pip install -r requirements.txt
```

### Use your API KEY

Edit the `main.py` file and use your api key – replace with __YOUR_API_KEY__, or make sure you use your key as an argument when in command line.

### Run

Run the application with 
```
python main.py -h
```

to see the available options.

```
python main.py -f 1478304000 -t 1478991600 -q shooting -o news.dat -a YOUR_API_KEY
```
is an example which runs by default even when running with no arguements.


