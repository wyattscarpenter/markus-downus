i want to be able to seamlessly transition from markdown to json
this json will be in a particular format with a particular selection of fields
heres an example:

# first level

name: This is the Name
effect: the effect
attacks: this one, this one
meta_tags: this, that, these

## second level

name: Here We Are
table: 
outcomes: 
1: one
2: two
3-6: a whole bunch

name: Another more normal one
effect: the effect
flavor_text: flavor text
meta_tags: this, that, this

So this would look like the json
```{json}
{
  "first_level": {
    "this_is_the_name": {
      "name": "This is the Name",
      "effect": "the effect",
      "attacks": ["this one", "this one"],
      "meta_tags": ["this", "that", "these"]
    },
    "second_level": {
      "here_we_are": {
        "name": "Here We Are",
        "table": {
          "outcomes": {
            "1": "one",
            "2": "two",
            "3-6": "a whole bunch"
          }
        }
      },
      "another_more_normal_one": {
        "name": "Another more normal one",
        "effect": "the effect",
        "flavor_text": "flavor text",
        "meta_tags": ["this", "that", "this"]
      }
    }
  }
}
```

This should be done in a python script