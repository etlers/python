import pandas as pd

cols = ["DAG_ID", "RUN_YN", "SCHEDULE", "TAGS"]
# 전날 데이터만으로 생성
list_pre = [
    ["A", "N", "30 * * * *", " "],
    ["B", "Y", "0 * * * *", "BIG"],
    ["C", "N", "@none", " "],
    ["Z", "N", "@none", " "],
]
# 당일 데이터
list_now = [
    ["A", "Y", "30 * * * *", " "],
    ["B", "Y", "15 3 * * *", "MID"],
    ["D", "Y", "@none", "SYNC"],
    ["Z", "N", "@none", " "],
]

# df_pre = pd.DataFrame(list_pre, columns=cols)
cols = ["DAG_ID", "RUN_YN", "SCHEDULE", "TAGS"]
df_pre = pd.DataFrame(index=range(0,0), columns=cols)
df_now = pd.DataFrame(list_now, columns=cols)

df_joined = pd.merge(
    df_pre,
    df_now,
    how='outer',
    on='DAG_ID',
    suffixes=('_L','_R'),
    indicator=True
)

list_compare = []
for key, row in df_joined.iterrows():
    list_compare.append(list(row))

list_dag_info = []
for rows in list_compare:
    list_row = rows
    if rows[7] == "right_only":
        list_row.append("추가")
    elif rows[7] == "left_only":
        list_row.append("삭제")
    else:
        div_cd = "-"
        for idx in range(1, 4):
            if rows[idx] != rows[idx+3]:
                div_cd = "변경"
                break
        list_row.append(div_cd)
    list_dag_info.append(list_row)

cols = ["DAG_ID", "PRE_RUN_YN", "PRE_SCHEDULE", "PRE_TAGS", "NOW_RUN_YN", "NOW_SCHEDULE", "NOW_TAGS", "_merge"]
cols.append("STATUS")
df_dag_info = pd.DataFrame(list_dag_info, columns=cols)
df_dag_info["UPDATE_DT"] = "2021-07-22"
df_dag_info = df_dag_info[["UPDATE_DT", "DAG_ID", "STATUS", "PRE_RUN_YN", "PRE_SCHEDULE", "PRE_TAGS", "NOW_RUN_YN", "NOW_SCHEDULE", "NOW_TAGS"]]
# 전날까지의 데이터에 금일 생성한 데이터 추가
# df_result = pd.concat([df_dag_info, df_base])
# 1년 이내의 데이터만 남기고 삭제
dels = df_dag_info[df_dag_info["UPDATE_DT"] < "2020-07-22"].index
df_result = df_dag_info.drop(dels)
# 정렬
df_result = df_result.sort_values(by=["UPDATE_DT", "DAG_ID"])
df_result.to_csv("aaa.csv", index=False)

df_copy = df_result[df_result["STATUS"] == "변경"]
print(df_copy)