#!/bin/bash
docker run --rm -v $(pwd):/iexdownload -i -t -d iexdownload /bin/bash
