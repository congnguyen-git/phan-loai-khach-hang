import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Hệ thống Phân loại Khách hàng", layout="wide")
st.title(" Ứng dụng Phân loại & Chăm sóc Khách hàng")
st.markdown("Vui lòng tải lên file dữ liệu để xem biểu đồ và chiến lược chăm sóc.")

# Nút cho thằng bạn tự tải file lên
uploaded_file = st.file_uploader("Tải file 'rfm_clustered_results.csv' vào đây", type=['csv'])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    st.subheader("1. Tổng quan Dữ liệu Khách hàng")
    st.dataframe(df.head(10))

    st.subheader("2. Trực quan hóa Phân cụm Khách hàng (Biểu đồ Phân tán 3D)")
    df['Tên_Cụm'] = df['Cluster'].astype(str)
    
    # Đã thêm tham số 'labels' để dịch tên các trục x, y, z sang tiếng Việt
    fig = px.scatter_3d(df, x='Recency', y='Frequency', z='Monetary',
                        color='Tên_Cụm',
                        title='Phân bố Khách hàng theo R-F-M (Thang đo Logarit)',
                        labels={
                            'Recency': 'Ngày mua gần nhất (R)',
                            'Frequency': 'Tần suất mua (F)',
                            'Monetary': 'Tổng chi tiêu (M)',
                            'Tên_Cụm': 'Cụm KH'
                        },
                        log_x=True, log_y=True, log_z=True, height=750)
    
    fig.update_traces(marker=dict(size=4, opacity=0.8))
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("3. Chiến lược Chăm sóc tự động theo Phân khúc")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.success(" Nhóm VIP (Cụm 1)\n\n**Hành động:** Gửi quà tri ân, chăm sóc 1-1, mời tham gia sự kiện.")
    with col2:
        st.info(" Nhóm KH Mới (Cụm 0)\n\n**Hành động:** Gửi email cảm ơn, tặng voucher 10% lần mua tiếp theo.")
    with col3:
        st.warning(" Nhóm Tiềm Năng (Cụm 2)\n\n**Hành động:** Gửi bản tin sản phẩm mới, nhắc nhở điểm tích lũy.")
    with col4:
        st.error(" Nhóm Rủi Ro (Cụm 3)\n\n**Hành động:** Tiếp thị lại (Remarketing), khảo sát tặng ưu đãi lớn (Giảm 30-50%).")