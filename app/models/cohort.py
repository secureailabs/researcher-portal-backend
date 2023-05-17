from typing import List

from pydantic import EmailStr, Field, StrictStr

from app.models.common import SailBaseModel


# example of cohort is
#  "cohort": {
#     "filter": [
#         {
#             "series_name": "gender",
#             "operator": "eq",
#             "value": "female"
#         },
#         {
#             "series_name": "body_mass_index",
#             "operator": "gt",
#             "value": 30
#         }
#     ],
#     "filter_operator": [
#         "and"
#     ]
# }


# create a cphort model that can be used to validate the cohort
class CohortFilter(SailBaseModel):
    series_name: StrictStr = Field(...)
    operator: StrictStr = Field(...)
    value: StrictStr = Field(...)


class Cohort(SailBaseModel):
    filter: List[CohortFilter] = Field(...)
    filter_operator: List[StrictStr] = Field(...)
