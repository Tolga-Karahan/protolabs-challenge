import json
import pandas as pd
import numpy as np

def calculate_poor_ratio(radius:float)->float:
    return radius * 2 * 10

def calculate_critical_ratio(radius:float)->float:
    return radius * 2 * 40

def has_unreachable_hole_warning(holes:list)->bool:
    if not isinstance(holes, pd._libs.missing.NAType):
        holes = json.loads(holes)
        for hole in holes:
            length = hole.get("length")
            radius = hole.get("radius")
            poor_ratio = calculate_poor_ratio(radius)

            if length > poor_ratio:
                return True
        return False
    else:
        return False

def has_unreachable_hole_error(holes:list)->bool:
    if not isinstance(holes, pd._libs.missing.NAType):
        holes = json.loads(holes)
        for hole in holes:
            length = hole.get("length")
            radius = hole.get("radius")
            critical_ratio = calculate_critical_ratio(radius)

            if length > critical_ratio:
                return True
        return False
    else:
        return False


def transform_data(df:pd.DataFrame)->pd.DataFrame:
    # df["holes"] = df["holes"].apply(lambda x: np.nan if x == "<NA>" else x)
    df["has_unreachable_hole_warning"] = df["holes"].apply(lambda x: has_unreachable_hole_warning(x))
    df["has_unreachable_hole_error"] = df["holes"].apply(lambda x: has_unreachable_hole_error(x))
    return df