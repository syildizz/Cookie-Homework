#!/bin/sh

if command -v uvicorn >/dev/null
then 
    uvicorn main:app
else 
    printf '%s\n' "Uvicorn is not installed. Please install uvicorn to proceed." >&2
    exit 1;
fi

