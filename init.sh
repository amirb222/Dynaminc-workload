#!/bin/bash

# Detect the operating system
case "$(uname -s)" in
  Linux*)   package_manager='apt-get' ;;
  Darwin*)  package_manager='brew' ;;
  *)        echo "Unsupported operating system: $(uname -s)" && exit 1 ;;
esac

# Install necessary packages
if [ "$package_manager" = "apt-get" ]; then
  sudo apt update
  sudo apt install -y awscli zip jq
elif [ "$package_manager" = "brew" ]; then
  brew update
  brew install awscli zip jq
fi

# Configure AWS setup (keys, region, etc)
aws configure
