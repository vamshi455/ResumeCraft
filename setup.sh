#!/bin/bash

# Create Streamlit config directory
mkdir -p ~/.streamlit/

# Create credentials file
echo "\
[general]\n\
email = \"your-email@example.com\"\n\
" > ~/.streamlit/credentials.toml

# Create config file
echo "\
[server]\n\
headless = true\n\
enableCORS = false\n\
enableXsrfProtection = false\n\
port = $PORT\n\
\n\
[theme]\n\
primaryColor = \"#2563eb\"\n\
backgroundColor = \"#ffffff\"\n\
secondaryBackgroundColor = \"#f8fafc\"\n\
textColor = \"#0f172a\"\n\
font = \"sans serif\"\n\
" > ~/.streamlit/config.toml
