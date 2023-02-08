import parse_schedule as ps
import pandas as pd


def main():
    file = "current_schedule"

    a = ps.prepare_df(df=pd.read_excel(f"downloads\\{file}.xlsx"))
    a.reset_index(inplace=True)

    a_up = ps.split_schedule(a, "upper")
    a_low = ps.split_schedule(a, "lower")

    b = ps.prepare_df(df=pd.read_excel(f"downloads\\{file}2.xlsx"))
    b.reset_index(inplace=True)
    b_up = ps.split_schedule(b, "upper")

    b_low = ps.split_schedule(b, "lower")
    df_diff = pd.concat([a_up, b_up]).drop_duplicates(keep=False)

    print(df_diff)


if __name__ == "__main__":
    main()
