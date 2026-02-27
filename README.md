# Consonance and Vowels
This is an entry into the Leonardo competition with the theme of Harmony.

## How to run
This is a Flask app, that runs as a Python script, which then runs a local website, which can then be opened on the web browser with the URL `http://localhost:5000/`.

### Starting the server
As this contains a `pyproject.toml` file, any Python package manager *should* work, such as the abilities provided natively by VSCode. However, failing that, a `uv.lock` has been provided if you wish to use `uv`.

Run the program like so:

#### If the packages have been installed with pip
```
python .
```

#### If you wish to install them and run with uv
```
uv run .
```

### Avoiding Firefox
The web app makes use of the `WebSocketStream` API, introduced in Chrome 124. However, as this has not been standardised yet, this API does not exist in Firefox at the moment. Therefore, a soft-lockout has been added that breaks the website if the API is not detected.

### Keeping in mind the download cache
As it has to fetch the BritFone pronunciation dictionary from the internet, it stores it in the `.dlcache/` directory for ease of access. Measures have been taken such that this download does not fail under the school's SSL restrictions, however, if this does not work, manual intervention may be required.

#### Manual download (if automatic download fails)
Download the csv file [here](https://raw.githubusercontent.com/JoseLlarena/Britfone/refs/heads/master/britfone.main.3.0.1.csv), placing it in `.dlcache` with the name `britfone.csv`.

## Further information
Please refer to the help menu in the bottom right of the webpage as to more help about usage.
