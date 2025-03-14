# Groq Python Chat

A chat application that uses Groq implemented using Python.

![chat](https://github.com/user-attachments/assets/33ca6a15-b288-49ec-b367-c27402e8ac49)

## Instructions

- Clone this repo

```sh
git clone git@github.com:Mishieck/groq-python-chat.git
```

- Navigate to repo

```sh
cd groq-python-chat
```

- Create a virtual environment using your preferred method
- Create environment variable file

```sh
touch .env # For linux
```

- Get API key from Groq and set environment variable in `.env` file

```sh
GROQ_API_KEY=your_api_key
```

- Set LLM model

```sh
MODEL=model_of_your_choice
```

For example,

```sh
MODEL=mixtral-8x7b-32768
```

- Install dependencies
    - Groq

    ```sh
    pip install groq
    ```

    - Rich

    ```sh
    pip install rich
    ```

- Run script

```sh
python3 src/main.py
```

or

```sh
python3 src/main.py --unf
```

if you have a [Nerd Font](https://www.nerdfonts.com/) installed.
