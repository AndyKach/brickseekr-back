from datetime import datetime
from pydantic import BaseModel, Field


class LegoSet(BaseModel):
    id:                str                          = Field()
    name:              str | None                   = Field(default='-')
    year:              int | None                   = Field(default=0)
    rating:          float | None                   = Field(default=0.0)
    # google_rating:   float | None                   = Field(default=0.0)

    theme:             str | None                   = Field(default='-')
    themeGroup:        str | None                   = Field(default='-')
    subtheme:          str | None                   = Field(default='-')

    images:           dict | None                   = Field(default={})
    pieces:            int | None                   = Field(default=0)
    dimensions:       dict | None                   = Field(default={})
    weigh:           float | None                   = Field(default=0.0)
    tags:             list | None                   = Field(default=[])
    description:       str | None                   = Field(default='-')
    ages_range:       dict | None                   = Field(default={})

    minifigures_ids:  list | None               = Field(default=[])
    minifigures_count: int | None               = Field(default=0)

    extendedData:     dict                      = Field(default={'cz_url_name': "None", 'cz_category_name': "None"})

    launchDate: datetime | str | None           = Field(default=None)
    exitDate:   datetime | str | None           = Field(default=None)
    updated_at: datetime | str | None           = Field(default=None)
    created_at: datetime | str | None           = Field(default_factory=datetime.now)


"""

lego_set_id=,
images=,
name=,
year=,
weigh=,
dimensions=,
ages=,
created_at=,

"""

