import os
from dataclasses import dataclass
from typing import List, Optional

import pandas as pd
from pandera import Field, SchemaModel
from pandera.typing import Series


@dataclass(frozen=True)
class XY:
    keys: pd.DataFrame
    x: pd.DataFrame
    y: pd.DataFrame

    def __post_init__(self) -> None:
        KeyDataSchema.validate(self.keys)

    def save(
        self,
        directory: str,
        prefix: Optional[str] = None,
    ) -> List[str]:
        os.makedirs(
            directory,
            exist_ok=True,
        )
        keys_file, x_file, y_file = XY.make_file_paths(
            directory=directory,
            prefix=prefix,
        )
        self.keys.to_csv(keys_file, index=False)
        self.x.to_csv(x_file, index=False)
        self.y.to_csv(y_file, index=False)
        return [keys_file, x_file, y_file]

    @staticmethod
    def make_file_paths(
        directory: str,
        prefix: Optional[str] = None,
    ) -> List[str]:
        keys_file = os.path.join(directory, f"{prefix}xy_keys.csv")
        x_file = os.path.join(directory, f"{prefix}xy_x.csv")
        y_file = os.path.join(directory, f"{prefix}xy_y.csv")
        return [keys_file, x_file, y_file]


def load_xy_from_files(
    keys_file: str,
    x_file: str,
    y_file: str,
) -> XY:
    return XY(
        keys=pd.read_csv(keys_file),
        x=pd.read_csv(x_file),
        y=pd.read_csv(y_file),
    )


class KeyDataSchema(SchemaModel):
    store_id: Series[str] = Field(
        nullable=False,
        coerce=True,
    )
    item_id: Series[str] = Field(
        nullable=False,
        coerce=True,
    )
    date_id: Series[int] = Field(
        ge=1,
        nullable=False,
        coerce=True,
    )

    class Config:
        name = "KeyDataSchema"
        strict = True
        coerce = True
