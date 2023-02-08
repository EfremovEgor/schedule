import pandas as pd
import dataframe_image as dfi
import re
from parse_data import download_schedule
import os


def split_schedule(df: pd.DataFrame, week: str) -> pd.DataFrame:
    df = df.copy()
    for idx in df.index:
        text = df["Пара"].loc[idx]

        if "/" in text:
            line = text.split("/")
            item = line[0 if week == "upper" else 1]
            if len(line) > 2:
                item = ""
                for i, v in enumerate(line):
                    if i == len(line) // 2 and week == "upper":
                        break
                    elif i >= len(line) // 2 and week == "lower":
                        break
                    item += v + "/"
                df.at[idx, "Пара"] = item[:-1]
            else:
                df.at[idx, "Пара"] = item
        if ("русский язык" in text.lower()) or ("иностранный язык" in text.lower()):
            df.at[idx, "Пара"] = "Модуль"
        if "физическая культура" in text.lower():
            df.at[idx, "Пара"] = "Физическая культура"
        text = df["Пара"].loc[idx]
        items = text.split(";")
        items = [item.strip() for item in items]
        for item in items:
            if item.lower() == "дот":
                df.at[idx, "Кабинет"] = item
            if re.compile("[а-я]+-\d+").match(item.lower()):
                df.at[idx, "Кабинет"] = item
        df.at[idx, "Пара"] = items[0]
    return df


def save_df(df: pd.DataFrame, name: str) -> None:
    if not os.path.exists(os.path.join(os.getcwd(), "output")):
        os.mkdir(os.path.join(os.getcwd(), "output"))
    df_styled = df.style.hide(axis="index")
    df_styled.set_properties(**{"text-align": "left"})
    df.reset_index(drop=True, inplace=True)
    dfi.export(
        df_styled,
        f"output\\{name}.png",
    )


def prepare_df(
    df: pd.DataFrame = None, full_path: str = "downloads\\schedule.xlsx"
) -> pd.DataFrame:
    full_name: tuple = tuple(full_path.split("\\")[-1].split("."))
    if df is None:
        download_schedule(
            folder_path="\\".join(full_path.split("\\")[:-1]),
            downloaded_file_name=full_name[0],
        )
        try:
            df = pd.read_excel(full_path)
        except FileNotFoundError as ex:
            print(str(ex))
            return
    df.dropna(how="all", axis=1, inplace=True)
    df.dropna(how="all", axis=0, inplace=True)
    df.drop(labels=[0, 1, 2, 3], inplace=True)
    df.drop(
        labels=df.columns[[1, 4, 5, 6, 7, 8, 9]],
        axis=1,
        inplace=True,
    )
    df.fillna("", inplace=True)
    df.columns = ["День", "Время", "Пара"]
    df["Кабинет"] = ""
    return df
