import parse_schedule as ps


def main():
    file = "current_schedule"
    df = ps.prepare_df(full_path=f"downloads\\{file}.xlsx")
    ps.save_df(df, f"raw_{file}")
    ps.save_df(ps.split_schedule(df, "upper"), f"upper_{file}")
    ps.save_df(ps.split_schedule(df, "lower"), f"lower_{file}")


if __name__ == "__main__":
    main()
