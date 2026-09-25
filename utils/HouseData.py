from pydantic import BaseModel, Field
from typing import Literal


class HouseData(BaseModel):
    longitude: float = Field(ge=-180, le=180, description="Longitude of the block")
    latitude: float = Field(ge=-90, le=90, description="Latitude of the block")
    housing_median_age: float = Field(
        ge=0, description="Median age of houses in the block"
    )
    total_rooms: float = Field(
        ge=1, description="Total number of rooms in the block"
    )
    total_bedrooms: float = Field(
        ge=0, description="Total number of bedrooms in the block"
    )
    population: float = Field(ge=0, description="Population of the block")
    households: float = Field(
        ge=1, description="Number of households in the block"
    )
    median_income: float = Field(
        ge=0, description="Median income of households (in tens of thousands of USD)"
    )
    ocean_proximity: Literal[
        "NEAR BAY", "<1H OCEAN", "INLAND", "NEAR OCEAN", "ISLAND"
    ] = Field(description="Proximity of the block to the ocean")
