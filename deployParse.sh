#!/bin/bash
cd Parse
zip -r -X "../Parse.zip" *
cd ..
aws lambda update-function-code --function-name stripeParse --zip-file fileb://Parse.zip