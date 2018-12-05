#!/bin/bash
aws lambda invoke --function-name stripeParse --invocation-type RequestResponse --log-type Tail --payload file://inputfile.txt outputfile.txt