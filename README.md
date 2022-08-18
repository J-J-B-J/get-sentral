# Get Sentral Timetable
A simple Python function to summon your timetable from Sentral.

## Usage

### Option 1
Set the environment variables `SENTRAL_USERNAME` and `SENTRAL_PASSWORD`

### Option 2
Create a file called `Sentral_Details.json`.
Set the contents of the file to
`{"USERNAME": "YOUR_USERNAME", "PASSWORD": "YOUR_PASSWORD"}`

### Option 3
Pass your details into the function, for example,
`get_sentral_timetable(username="YOUR_USERNAME", password="YOUR_PASSWORD")`

### Option 4
Do none of the above, and the program will ask for you to manually input your details.
