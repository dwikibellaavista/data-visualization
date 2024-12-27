import streamlit as st
import pandas as pd
import plotly.express as px
import plotly


# Menampilkan versi library
st.sidebar.title("📋 Versi Library")
st.sidebar.write(f"Streamlit: {st.__version__}")
st.sidebar.write(f"Pandas: {pd.__version__}")
st.sidebar.write(f"Plotly: {plotly.__version__}")

# Mengatur CSS untuk tombol
st.markdown(
    """
    <style>
    .stButton > button {
        width: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def read_data(file_path):
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        st.error(f"Error reading the data: {e}")
        return None

def main_page():
    st.title("Aplikasi Analisis Data Siswa")

    # Sidebar untuk navigasi
    st.sidebar.header(f"Selamat datang! ^_^")

    if st.sidebar.button("📂 Dashboard"):
        st.session_state["active_menu"] = "dashboard"
    if st.sidebar.button("📂 Data Siswa"):
        st.session_state["active_menu"] = "data_siswa"
    if st.sidebar.button("📂 Data Math Score"):
        st.session_state["active_menu"] = "data_math"
    if st.sidebar.button("📂 Data Reading Score"):
        st.session_state["active_menu"] = "data_reading"
    if st.sidebar.button("📂 Data Writing Score"):
        st.session_state["active_menu"] = "data_writing"

    # Menampilkan konten
    if "active_menu" not in st.session_state:
        st.session_state["active_menu"] = "dashboard"  # Set default menu to dashboard
    if st.session_state["active_menu"] == "dashboard":
        show_dashboard()
    elif st.session_state["active_menu"] == "data_siswa":
        show_data_siswa()
    elif st.session_state["active_menu"] == "data_math":
        show_data_math_score()
    elif st.session_state["active_menu"] == "data_reading":
        show_data_reading_score()
    elif st.session_state["active_menu"] == "data_writing":
        show_data_writing_score()

def show_dashboard():
    data = read_data("exams.csv")

    if data is not None:
        total_students = len(data)

        # Slider
        if "num_rows" not in st.session_state:
            st.session_state["num_rows"] = 5  # Set default value for slider

        st.session_state["num_rows"] = st.sidebar.slider("Pilih jumlah baris yang ditampilkan:", 1, total_students, st.session_state["num_rows"])
        
        st.sidebar.text("===================================")
        
        st.write("Menampilkan data:")
        st.dataframe(data.head(st.session_state["num_rows"]))
        st.write(f"Jumlah baris yang ditampilkan: {st.session_state['num_rows']}")

        # Set kolom untuk X-axis dan Y-axis
        score_columns = ["math score", "reading score", "writing score"]
        available_columns = data.columns.tolist()
        
        # Validasi kolom yang diperlukan
        valid_columns = [col for col in score_columns if col in available_columns]

        if len(valid_columns) < 3:
            st.error("Data tidak memiliki semua kolom 'math score', 'reading score', dan 'writing score'.")
        else:
            st.sidebar.header("Box Plot")

            box_x_columns = [col for col in available_columns if col not in valid_columns]

            if not box_x_columns:
                st.error("Tidak ada kolom yang tersedia untuk kategori Box Plot selain 'math score', 'reading score', dan 'writing score'.")
            else:
                box_y = st.sidebar.selectbox("Nilai untuk Box Plot", valid_columns, index=0)
                box_x = st.sidebar.selectbox("Kategori untuk Box Plot", box_x_columns)

                st.subheader("Box Plot")
                fig_box = px.box(
                    data,
                    x=box_x,
                    y=box_y,
                    color=box_x,
                    title=f"Box Plot: {box_y} berdasarkan {box_x}",
                    labels={box_x: box_x, box_y: box_y},
                    hover_data=data.columns
                )
                st.plotly_chart(fig_box)

                st.sidebar.text("===================================")

                st.sidebar.header("Bar Plot")

                # Sumbu X
                bar_x = st.sidebar.selectbox("Kolom untuk Sumbu X (Skor)", valid_columns, index=0)

                st.subheader("Bar Plot")
                fig_bar = px.histogram(
                    data,
                    x=bar_x,
                    nbins=10,  # Jumlah bin untuk membagi rentang nilai
                    title=f"Bar Plot Frekuensi: {bar_x}",
                    labels={bar_x: bar_x, 'count': 'Frekuensi'},
                )
                fig_bar.update_traces(marker=dict(color='rgba(135, 206, 250, 0.8)'))  # Warna biru soft dengan transparansi
                fig_bar.update_layout(
                    xaxis_title=bar_x,
                    yaxis_title="Frekuensi",
                    bargap=0.1,  # Jarak antar bar
                    showlegend=False  # Menonaktifkan legend
                )
                st.plotly_chart(fig_bar)

                st.sidebar.text("===================================")

                st.sidebar.header("Scatter Plot")
                x_axis = st.sidebar.selectbox("X-axis", valid_columns, index=0)
                y_axis = st.sidebar.selectbox("Y-axis", valid_columns, index=1)
                category_column = st.sidebar.selectbox("Kategori berdasarkan Warna", available_columns)
                filter_column = st.sidebar.selectbox("Filter berdasarkan Kolom", available_columns)
                
                unique_values = data[filter_column].dropna().unique().tolist()
                selected_filter = st.sidebar.selectbox(f"Filter {filter_column}:", ["Semua"] + unique_values)

                if selected_filter != "Semua":
                    filtered_data = data[data[filter_column] == selected_filter]
                else:
                    filtered_data = data

                st.sidebar.text("===================================")

                st.subheader("Scatter Plot")
                fig_scatter = px.scatter(
                    filtered_data, 
                    x=x_axis, 
                    y=y_axis, 
                    color=category_column,
                    title=f"Scatter Plot: {y_axis} vs {x_axis}",
                    labels={x_axis: x_axis, y_axis: y_axis},
                    hover_data=data.columns
                )
                fig_scatter.update_traces(marker=dict(size=8, opacity=0.7))
                fig_scatter.update_layout(dragmode='pan')  # Mode interaktif
                st.plotly_chart(fig_scatter)

                st.subheader("Data setelah Filter")
                st.dataframe(filtered_data)

                st.sidebar.header("AVERAGE")
                average_math = data["math score"].mean()
                average_reading = data["reading score"].mean()
                average_writing = data["writing score"].mean()

                st.sidebar.text(f"Math Score: {average_math:.2f}")
                st.sidebar.text(f"Reading Score: {average_reading:.2f}")
                st.sidebar.text(f"Writing Score: {average_writing:.2f}")

def show_data_siswa():
    st.subheader("Data Siswa")

    data = read_data("exams.csv")
    if data is not None:
        total_students = len(data)

        if "num_rows_siswa" not in st.session_state:
            st.session_state["num_rows_siswa"] = 5  # Set default value for slider

        st.session_state["num_rows_siswa"] = st.sidebar.slider(
            "Pilih jumlah baris yang ditampilkan:",
            1, total_students, st.session_state["num_rows_siswa"]
        )

        data_siswa = pd.DataFrame({
            'Gender': data['gender'],
            'Race/Ethnicity': data['race/ethnicity'],
            'Parental Level of Education': data['parental level of education']
        })

        st.write("Menampilkan data siswa:")
        st.dataframe(data_siswa.head(st.session_state["num_rows_siswa"]))
        st.write(f"Jumlah baris yang ditampilkan: {st.session_state['num_rows_siswa']}")

def show_data_math_score():
    st.subheader("Data Math Score")

    data = read_data("exams.csv")
    if data is not None:
        total_students = len(data)

        if "num_rows_math" not in st.session_state:
            st.session_state["num_rows_math"] = 5  # Set default value for slider

        st.session_state["num_rows_math"] = st.sidebar.slider(
            "Pilih jumlah baris yang ditampilkan:",
            1, total_students, st.session_state["num_rows_math"]
        )

        data_math = pd.DataFrame({
            'Gender': data['gender'],
            'Math Score': data['math score']
        })

        st.write("Menampilkan data siswa:")
        st.dataframe(data_math.head(st.session_state["num_rows_math"]))
        st.write(f"Jumlah baris yang ditampilkan: {st.session_state['num_rows_math']}")

def show_data_reading_score():
    st.subheader("Data Reading Score")
    data = read_data("exams.csv")
    if data is not None:
        total_students = len(data)

        if "num_rows_read" not in st.session_state:
            st.session_state["num_rows_read"] = 5  # Set default value for slider

        st.session_state["num_rows_read"] = st.sidebar.slider(
            "Pilih jumlah baris yang ditampilkan:",
            1, total_students, st.session_state["num_rows_read"]
        )

        data_reading = pd.DataFrame({
            'Gender': data['gender'],
            'Reading Score': data['reading score']
        })

        st.write("Menampilkan data siswa:")
        st.dataframe(data_reading.head(st.session_state["num_rows_read"]))
        st.write(f"Jumlah baris yang ditampilkan: {st.session_state['num_rows_read']}")

def show_data_writing_score():
    st.subheader("Data Writing Score")

    data = read_data("exams.csv")
    if data is not None:
        total_students = len(data)

        if "num_rows_write" not in st.session_state:
            st.session_state["num_rows_write"] = 5  # Set default value for slider

        st.session_state["num_rows_write"] = st.sidebar.slider(
            "Pilih jumlah baris yang ditampilkan:",
            1, total_students, st.session_state["num_rows_write"]
        )

        data_write = pd.DataFrame({
            'Gender': data['gender'],
            'Writing Score': data['writing score']
        })

        st.write("Menampilkan data siswa:")
        st.dataframe(data_write.head(st.session_state["num_rows_write"]))
        st.write(f"Jumlah baris yang ditampilkan: {st.session_state['num_rows_write']}")



main_page()