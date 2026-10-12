
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Quản lý điểm sinh viên",
    page_icon="🎓",
    layout="wide"
)

st.title("QUẢN LÝ ĐIỂM SINH VIÊN")
st.write("Bảng theo dõi kết quả học tập của 10 sinh viên.")

# 1. Tạo dữ liệu mẫu
data = {
    "MSSV": [
        "SV001", "SV002", "SV003", "SV004", "SV005",
        "SV006", "SV007", "SV008", "SV009", "SV010"
    ],
    "Họ tên": [
        "Nguyễn Văn An", "Trần Thị Bình", "Lê Văn Cường",
        "Phạm Thị Dung", "Hoàng Văn Đức", "Vũ Thị Hà",
        "Đặng Văn Hùng", "Bùi Thị Lan", "Đỗ Văn Minh",
        "Ngô Thị Ngọc"
    ],
    "Chuyên cần": [8, 9, 7, 10, 6, 8, 9, 7, 10, 8],
    "Giữa kỳ": [7, 8, 6, 9, 5, 7, 8, 6, 9, 8],
    "Cuối kỳ": [8, 9, 7, 9, 4, 8, 9, 6, 10, 7]
}

df = pd.DataFrame(data)

# 2. Tính điểm tổng kết
df["Tổng kết"] = (
    df["Chuyên cần"] * 0.1
    + df["Giữa kỳ"] * 0.3
    + df["Cuối kỳ"] * 0.6
).round(2)

# 3. Xếp loại
def xep_loai(diem):
    if diem >= 8.5:
        return "Giỏi"
    elif diem >= 7:
        return "Khá"
    elif diem >= 5:
        return "Trung bình"
    else:
        return "Chưa đạt"

df["Xếp loại"] = df["Tổng kết"].apply(xep_loai)

# 4. Hiển thị bảng điểm
st.subheader("1. Bảng điểm sinh viên")
st.dataframe(
    df[[
        "Họ tên", "Chuyên cần", "Giữa kỳ",
        "Cuối kỳ", "Tổng kết", "Xếp loại"
    ]],
    use_container_width=True,
    hide_index=True
)

# 5. Thống kê chung
st.subheader("2. Thống kê lớp học")

diem_tb = df["Tổng kết"].mean()
sv_max = df.loc[df["Tổng kết"].idxmax()]
sv_min = df.loc[df["Tổng kết"].idxmin()]
so_sv_dat = int((df["Tổng kết"] >= 5).sum())

c1, c2, c3 = st.columns(3)
c1.metric("Điểm trung bình lớp", f"{diem_tb:.2f}")
c2.metric("Sinh viên đạt", f"{so_sv_dat}/10")
c3.metric("Sinh viên chưa đạt", f"{10-so_sv_dat}/10")

st.write(
    f"🏆 **Cao nhất:** {sv_max['Họ tên']} "
    f"- {sv_max['Tổng kết']:.2f} điểm"
)
st.write(
    f"📉 **Thấp nhất:** {sv_min['Họ tên']} "
    f"- {sv_min['Tổng kết']:.2f} điểm"
)

# 6. Chọn sinh viên
st.subheader("3. Tra cứu điểm từng sinh viên")

ten_sv = st.selectbox("Chọn sinh viên:", df["Họ tên"])
sv = df[df["Họ tên"] == ten_sv].iloc[0]

st.write(f"**MSSV:** {sv['MSSV']}")

c1, c2, c3 = st.columns(3)
c1.metric("Chuyên cần", f"{sv['Chuyên cần']:.1f}")
c2.metric("Giữa kỳ", f"{sv['Giữa kỳ']:.1f}")
c3.metric("Cuối kỳ", f"{sv['Cuối kỳ']:.1f}")

c4, c5 = st.columns(2)
c4.metric("Điểm tổng kết", f"{sv['Tổng kết']:.2f}")
c5.metric("Xếp loại", sv["Xếp loại"])

# 7. Biểu đồ
st.subheader("4. Biểu đồ điểm tổng kết")
st.bar_chart(
    df.set_index("Họ tên")["Tổng kết"],
    y_label="Điểm tổng kết"
)

# 8. Thông tin người tạo
st.divider()
st.caption("Người tạo: [Nguyễn Nhật Trí] | MSSV: [052208003771]")

