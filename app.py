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
    
    # 1. Tự động tính trung bình R, F, M của mỗi cụm
    cluster_avg = df.groupby('Cluster').mean(numeric_only=True).reset_index()
    
    # 2. Xây dựng Logic tự động tìm ra cụm nào là VIP, Rủi ro, Mới, Tiềm năng
    # VIP = Cụm có tiền chi tiêu (Monetary) cao nhất
    vip_cluster = cluster_avg.loc[cluster_avg['Monetary'].idxmax()]['Cluster']
    
    # Rủi ro = Cụm có số ngày chưa mua (Recency) cao nhất
    risk_cluster = cluster_avg.loc[cluster_avg['Recency'].idxmax()]['Cluster']
    
    # Lấy 2 cụm còn lại
    remaining = cluster_avg[(cluster_avg['Cluster'] != vip_cluster) & (cluster_avg['Cluster'] != risk_cluster)]
    
    if len(remaining) == 2:
        # Khách Mới = Trong 2 cụm còn lại, cụm nào mua gần đây hơn (Recency thấp hơn)
        new_cluster = remaining.loc[remaining['Recency'].idxmin()]['Cluster']
        # Tiềm năng = Cụm cuối cùng
        pot_cluster = remaining.loc[remaining['Recency'].idxmax()]['Cluster']
    else:
        new_cluster, pot_cluster = -1, -1 # Phòng hờ lỗi

    # 3. Hiển thị giao diện tự động lấy đúng số cụm
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.success(f" Nhóm VIP (Cụm {int(vip_cluster)})\n\n**Hành động:** Gửi quà tri ân, chăm sóc 1-1, mời tham gia sự kiện.")
    with col2:
        st.info(f" Nhóm KH Mới (Cụm {int(new_cluster)})\n\n**Hành động:** Gửi email cảm ơn, tặng voucher 10% lần mua tiếp theo.")
    with col3:
        st.warning(f" Nhóm Tiềm Năng (Cụm {int(pot_cluster)})\n\n**Hành động:** Gửi bản tin sản phẩm mới, nhắc nhở điểm tích lũy.")
    with col4:
        st.error(f" Nhóm Rủi Ro (Cụm {int(risk_cluster)})\n\n**Hành động:** Tiếp thị lại (Remarketing), khảo sát tặng ưu đãi lớn (Giảm 30-50%).")