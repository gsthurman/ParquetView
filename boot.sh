#!/bin/bash

# Start Flask app
cd ./flask
python app.py &
FLASK_APP_PID=$!

# Start Electron app
cd ../electron
npm start &
ELECTRON_APP_PID=$!

# Function to kill both apps when script is terminated
function cleanup {
  echo "Stopping Flask app..."
  kill -9 $FLASK_APP_PID
  echo "Stopping Electron app..."
  kill -9 $ELECTRON_APP_PID
}

# Register the cleanup function to be called on the EXIT signal
trap cleanup EXIT

# Wait indefinitely
while true; do sleep 1; done