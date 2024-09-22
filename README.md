# academic-paper-to-vr

 I want to be able to read a paper, as well as listen to it at the same time.
 I have a set of xreal air glasses, which support youtube and phone screen
 sharing.

 Therefore, I would like to automate the process of taking a paper, converting
 it to audio, mixing the two together, and creating a video.


# Setup

Ensure the environment is setup. Mine is set up in a venv with the requirements.txt file.

Ensure OPENAI_API_KEY is set as an environment variable.
 - The openai api key is used to clean text to ensure smooth diction, create the audio file, and potentially parse any images on the screen.

## Example Use:

```
pip freeze > requirements.txt
```

```
python gen.py papers/do_things_that_dont_scale.pdf
```

```
python gen.py papers
```