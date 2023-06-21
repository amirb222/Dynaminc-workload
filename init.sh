#!/bin/bash

sudo apt update
sudo apt install -y awscli zip jq

# Configure AWS setup (keys, region, etc)
aws configure
