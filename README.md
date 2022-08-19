# Get Sentral Timetable
A simple Python function to summon your timetable from Sentral.

## Installation

1. Open the command line and change to the `get-sentral-timetable` directory, e.g.
    `cd Documents/Python/get-sentral-timetable`

2. Build the package using this command:
    `python setup.py sdist bdist_wheel`
3. Install the package using pip:
    `pip install dist/SentralTimetable-0.1.tar.gz `

## Troubleshooting

Try replacing `python` and `pip` with `python3` and `pip3`.

## Usage

Use `import SentralTimetable` at the top of your program.
Then, call `SentralTimetable.get_timetable()` to get the timetable in a dictionary form.
See the options for the paramaters to `get_timetable()` in the `Paramerer options` section below.

Calling `get_timetable` returns a dictionary in the following format:

```python
{
    'classes': {
        '1': {  # A class in period one
            'subject': 'Math Yr 12',
            'room': 'AG01',
            'teacher': 'A. Mathematician'
        },
        '2': None   # An empty period
    },
    'notices': [
        {
            'title': 'Basketball trials today at lunchtime!',
            'teacher': 'B. Sport',
            'date': datetime.datetime(2022, 8, 19, 10, 0),
            'content': 'See you all at lunch time on the oval!'
        }
    ]
}
```

Please note that this will autocorrect based on the number of periods and notices.

## Parameter options

### Option 1
Set the environment variables `SENTRAL_USERNAME`, `SENTRAL_PASSWORD` and `URL`

### Option 2
Create a file called `Sentral_Details.json`.
Set the contents of the file to
`{"USERNAME": "YOUR_USERNAME", "PASSWORD": "YOUR_PASSWORD", "URL": "https://YOURSCHOOL.sentral.com.au/portal/dashboard"}`

### Option 3
Pass your details into the function, for example,
`get_sentral_timetable(username="YOUR_USERNAME", password="YOUR_PASSWORD", url="https://YOURSCHOOL.sentral.com.au/portal/dashboard")`

### Option 4
Do none of the above, and the program will ask for you to manually input your details.
