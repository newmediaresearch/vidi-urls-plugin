#!/bin/bash
set -e

cp -r vidi_urls /opt/cantemo/portal/portal/plugins/
supervisorctl restart all
