# The structure of the game database

Game state, as manipulated by the Olympia C code, is stored in a
series of text files containing objects. These objects contain nested
lists of other objects and values. For the usual reasons, scalars
are represented as a list of length 1.

The major types of objects are: locations, factions, characters,
items, skills, ships, gates, and miscellaneous stuff. An object
is called a "box" by the code.

A location looks like this:

> 3608 loc castle
> na Oleg's Summer Residence
> LI
>  wh 10620
>  hl 7988 7998
> SL
>  de 50
>  cl 6

The line "3608 loc castle" says that this is box number 3806, of the
kind location, with a subkind of castle. It has a name. It has 2
nested lists describing it. LI wh "where" is a list of length 1 saying
where the castle is: it's in box 10620, which is an identifier which
maps to province 'ah20' on the map (See: oid.py). LI hl "here list" is
a list of boxes which are inside the castle -- in this case the noble 7988
and the tower 7998. The castle is level 6 and has a defense of 50.
And it has a name.

The JSON version of this object is a bit easier to deal with:

> {
>   "LI": {
>     "hl": [ "7988", "7998" ],
>     "wh": [ "10620" ]
>   },
>   "SL": {
>     "cl": [ "6" ],
>     "de": [ "50" ]
>   },
>   "firstline": [ "3608 loc castle" ],
>   "na": [ "Oleg's Summer Residence" ]
> }

