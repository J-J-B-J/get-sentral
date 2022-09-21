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
            'teacher': 'A. Mathematician',
            'colour': '#FF00FF'  # The colour for the bar on the left
        },
        '2': None   # An empty period
    },
    'notices': [
        {
            'title': 'Basketball trials today at lunchtime!',
            'teacher': 'B. Sport',
            'date': (2022, 8, 19, 10, 0),   # Year, month, day, hour, minute that the notice was posted at
            'date string': 'Friday, 19 August 2022 at 10:00 am',  # The time that was read from the Sentral website
            'content': 'See you all at lunch time on the oval!'
        }
    ],
    'events': [
        {
            'title': 'Subject Selections due',
            'flag': '',  # Flags can be empty
            'date': 'December 2'  # The date attribute is the date of the event
        },
        {
            'title': 'Assessment: Australian Geography',
            'flag': 'Year 10',  # Flags are usually year numbers
            'date': 'April 23 10:30 am'   # The date attribute can have a date and time too
        }
    ]
}
```

Please note that this will autocorrect based on the number of periods and notices.

## Parameter options

- Debug must be set to `True` or `False`, unless otherwise specified
- The username and password must be valid
- The URL must be valid and **must end with /portal/dashboard**


### Option 1
Set the environment variables `SENTRAL_USERNAME`, `SENTRAL_PASSWORD`, `URL` and `DEBUG`

Setting environment variables:
- [From the command line](https://www.schrodinger.com/kb/1842)
- [In JetBrains apps](https://www.jetbrains.com/help/pycharm/run-debug-configuration.html#run-debug-parameters)

### Option 2
Create a file called `Sentral_Details.json`.
Set the contents of the file to
```json
{
    "USERNAME": "YOUR_USERNAME",
    "PASSWORD": "YOUR_PASSWORD",
    "URL": "https://YOUR_SCHOOL.sentral.com.au/portal/dashboard",
    "DEBUG": false
}
```
**Debug must be set to `true` or `false` (no capital)**

### Option 3
Pass your details into the function, for example:

```python
get_sentral_timetable(username="YOUR_USERNAME", password="YOUR_PASSWORD", url="https://YOURSCHOOL.sentral.com.au/portal/dashboard")
```

### Option 4
Do none of the above, and the program will ask for you to manually input your details via the `input()` function.

**N.B.** If you use this program as a library instead of a plain old program, be sure to overwrite the input using `lambda`, or else the`input()` function could interrupt your program.
