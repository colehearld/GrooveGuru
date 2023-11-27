# GrooveGuru README

## What is GrooveGuru?

GrooveGuru is a web application that recommends songs to a user based on their listening history on spotify. Recommendations are primarily determined by how the song *sounds*. The program does this by gathering metrics about the song from spotify and comparing them to a dataset of 600,000 different tracks using the k-nearest-neighbor algorithm. Users can then choose to like or dislike the recommendation to create greater accuracy for future recommendations. 

## Setup Instructions

**Note: In order to use GrooveGuru you MUST have a spotify account and be logged in on the browser**

### Step 1: Update Spotify Dataset Path
In order to run GrooveGuru successfully, you need to configure the local path to the Spotify dataset. Navigate to `engine.py` and locate the `spotify_data_path` variable. Update its value with the path to your local dataset.

```python
# engine.py
spotify_data_path = "path/to/your/local/dataset"
```
### Step 2: Run the Main Program
Execute the main program by running main.py

### Step 3: Set Up React App
Open a command prompt and change the directory to GrooveGuru\react-app.

### Step 4: Run React App
Run the following command to start the development server for the React app. Note that Node.js must be installed on your system.

```commandline
npm run dev
```

If you encounter a dependency error or a VITE error, try running `npm update`

If the issue persists, force install the dependencies using `npm install --force`

### Step 5: Open Web Address
After successfully starting the development server, a web address will be displayed in the command prompt. Open this address in your web browser to access the frontend.
