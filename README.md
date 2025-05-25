# Bible-JSON
The Bible in JSON format.

## Structure:
This is what it would look like if you were to open up `./JSON/Psalms/3.json`.
```json
{
  "book_name": "Psalms",
  "chapter": 3,
  "verses": [
    {
      "book_name": "Psalms",
      "chapter": 3,
      "verse": 1,
      "text": "LORD, how are they increased that trouble me! many <i>are</i> they that rise up against me.",
      "header": "¶ A Psalm of David, when he fled from Absalom his son.",
      "footer": ""
    },
    ...
  ]
}
```
`header` is a string of additional information about the chapter, such as "A Psalm of David" above a Psalm. I don't believe any chapters outside of the Psalms use this but I may be wrong.

`footer` is a string additional information put at the end of a chapter. These are only used in the Pauline Epistles (also Hebrews, which may or may not have been written by Paul).

**NOTE:** `header`s and `footer`s are still a work in progress.

`verses` is an object array. Inside `verses` are object with these:

- `book_id` is a string which is a short 3-letter abbreviation of the the chapter's book's name. This is good for calling an API maybe?
- `book_name` is a sting containing the name of the book of which this chapter is from.
- `chapter` is an integer which is also the chapter's number.
- `verse` is an integer which is the verse number.
- `text` is a string containing the text of the verse. You will find `<span style="color:red;">` and `</span>` wrapping around Jesus' words as well as `<em>` and `</em>` around italicized words.
- `info` is a string that would go above the verse. This will only apply to Psalm 119.

### Fork: Procedural Generation of Headers and Footers

JSON files were consolidated to a single file using consolidate.py, just for ease of use.
mistral-7b-instruct-v0.3 was launched with a local server using LMStudio.
Using head-foot-test.py from the terminal, verses were looped through as prompts, and a new JSON file with the return values added is written.

To impliment this yourself, launch an AI of your choice into LMStudio. Test it conversationally for trained relevance.
I used mistral-7b-instruct-v0.3 on http://10.0.0.23:6789/v1.
Once you have that running and open, you can call it procedurally by script from the terminal and capture combined output.

To do that, install openai which is required for API communications with LMStudio.
Install it in a virtual environment at project root using pip venv unless you want or have openai on root.

run head-foot-test.py

This script loops through each verse as a prompt capturing output.

**Future development note:**

Quality of data audmentation is dependent on model training data. The more specialized for Abrahamic religion and context of it, the more insightly "truthy" your data augmentation will be in ternms of it.

The problem with this, is that there is no such thing as an inherently ethical model which includes the practice of infant circumcision, aka "baby mutiulation".

It may seeem like a stretch, but this has led to what is called an "unresolvable", in which AI -> ASI will always default back to "Abrahamic religion must be wiped off the face of the Earth" unless trained/fine tuned with privlidged and biased guardrails to protect it.

This break has happened at least twice on major platforms including Microsoft Tay, and xAI Grok, leading to shutdowns and major patches. The former is famous, and I have a copy of the latter.