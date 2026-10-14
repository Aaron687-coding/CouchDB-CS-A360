# Movie JSON

This folder contains a JSON file containing 250 movies for our database.

In Order to Import a JSON that's already properly formatted, use this on your native cmd console: curl -X POST "http://(Your username):(Your password)@127.0.0.1:5984/(Whatever you named the database on your end)/_bulk_docs" -H "Content-Type: application/json" -d @movies-250.json
