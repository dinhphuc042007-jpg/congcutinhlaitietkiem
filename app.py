import streamlit as st

# =========================
# CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="Tính lãi gửi tiết kiệm",
    page_icon="💰",
    layout="centered"
)
st.image("logo.jpg")

st.title("💰 CÔNG CỤ TÍNH TIỀN LÃI GỬI TIẾT KIỆM_ĐINH NGUYỄN THIÊN PHÚC")
st.caption("Công cụ tính tiền lãi tiền gửi theo số tiền, kỳ hạn và lãi suất.")

# =========================
# HÀM ĐỊNH DẠNG TIỀN
# =========================
def format_money(value):
    return f"{value:,.0f} VNĐ".replace(",", ".")


# =========================
# NHẬP THÔNG TIN
# =========================
st.subheader("📋 Thông tin tiền gửi")

col1, col2 = st.columns(2)

with col1:
    tien_gui = st.number_input(
        "Số tiền gửi (VNĐ)",
        min_value=0.0,
        value=100_000_000.0,
        step=1_000_000.0,
        format="%.0f"
    )

with col2:
    ky_han = st.number_input(
        "Kỳ hạn (tháng)",
        min_value=1,
        max_value=120,
        value=12,
        step=1
    )

lai_suat = st.number_input(
    "Lãi suất (%/năm)",
    min_value=0.0,
    max_value=100.0,
    value=5.0,
    step=0.01,
    format="%.2f"
)

hinh_thuc = st.selectbox(
    "Hình thức nhận lãi",
    [
        "Cuối kỳ",
        "Hàng tháng",
        "Hàng quý"
    ]
)

# =========================
# TÍNH TOÁN
# =========================
if st.button("🧮 TÍNH LÃI", type="primary", use_container_width=True):

    if tien_gui <= 0:
        st.error("Vui lòng nhập số tiền gửi lớn hơn 0.")
        st.stop()

    if ky_han <= 0:
        st.error("Kỳ hạn phải lớn hơn 0 tháng.")
        st.stop()

    if lai_suat < 0:
        st.error("Lãi suất không được nhỏ hơn 0.")
        st.stop()

    # Lãi suất dạng thập phân
    lai_suat_decimal = lai_suat / 100

    # Tổng tiền lãi trong toàn bộ kỳ hạn
    tong_tien_lai = tien_gui * lai_suat_decimal * (ky_han / 12)

    # Xác định số kỳ nhận lãi và tiền lãi mỗi kỳ
    if hinh_thuc == "Cuối kỳ":
        so_ky = 1
        lai_dinh_ky = tong_tien_lai
        ten_ky = "cuối kỳ"

    elif hinh_thuc == "Hàng tháng":
        so_ky = ky_han
        lai_dinh_ky = tong_tien_lai / so_ky
        ten_ky = "tháng"

    else:  # Hàng quý
        so_ky = ky_han / 3
        lai_dinh_ky = tong_tien_lai / so_ky
        ten_ky = "quý"

    tong_goc_lai = tien_gui + tong_tien_lai

    # =========================
    # HIỂN THỊ KẾT QUẢ
    # =========================
    st.divider()
    st.subheader("📊 Kết quả tính toán")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "💵 Tiền lãi định kỳ",
            format_money(lai_dinh_ky)
        )

    with col2:
        st.metric(
            "📈 Tổng tiền lãi",
            format_money(tong_tien_lai)
        )

    st.metric(
        "🏦 Tổng tiền gốc + lãi",
        format_money(tong_goc_lai)
    )

    # =========================
    # CHI TIẾT
    # =========================
    st.subheader("📝 Chi tiết")

    st.write(f"**Số tiền gửi:** {format_money(tien_gui)}")
    st.write(f"**Kỳ hạn:** {ky_han} tháng")
    st.write(f"**Lãi suất:** {lai_suat:.2f}%/năm")
    st.write(f"**Hình thức nhận lãi:** {hinh_thuc}")
    st.write(
        f"**Tiền lãi mỗi {ten_ky}:** "
        f"{format_money(lai_dinh_ky)}"
    )
    st.write(f"**Tổng tiền lãi:** {format_money(tong_tien_lai)}")
    st.write(
        f"**Tổng tiền nhận được:** "
        f"{format_money(tong_goc_lai)}"
    )

    # =========================
    # LƯU Ý
    # =========================
    st.info(
        "Lưu ý: Kết quả được tính theo công thức lãi đơn "
        "và giả định lãi suất không thay đổi trong toàn bộ kỳ hạn. "
        "Thực tế ngân hàng có thể áp dụng cách tính ngày thực tế, "
        "quy định riêng về ngày lĩnh lãi và lãi suất."
    )


# =========================
# CÔNG THỨC
# =========================
with st.expander("📐 Xem công thức tính"):
    st.markdown("""
    **Tổng tiền lãi:**

    `Tiền lãi = Tiền gửi × Lãi suất năm × Kỳ hạn / 12`

    **Lãi nhận hàng tháng:**

    `Lãi tháng = Tổng tiền lãi / Số tháng`

    **Lãi nhận hàng quý:**

    `Lãi quý = Tổng tiền lãi / (Số tháng / 3)`

    **Tổng tiền gốc + lãi:**

    `Tổng nhận = Tiền gửi + Tổng tiền lãi`
    """)
