#!/bin/bash
cd function
zip -r -X "../Archive.zip" *
cd ..
aws lambda update-function-code --function-name stripeParse --zip-file fileb://Archive.zip