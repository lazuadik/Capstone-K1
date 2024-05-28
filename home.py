import streamlit as st
import pandas as pd
import sistem_rekomendasi_modul
import gspread
from oauth2client.service_account import ServiceAccountCredentials
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('db-gsheets-422915-23989a936cd5.json', scope)
client = gspread.authorize(creds)

st.header("Selamat datang di Rekomendasi Karir IT!")
st.write("Masukkan input, nanti kami akan merekomendasikan jalur karir yang cocok denganmu!")

# Buat store data ke database input
dt = client.open('Streamlit database').worksheet('input')

with st.form(key='my_form'):
    nama = st.text_input("Masukkan Nama: ")
    data1 = st.text_input("Masukkan pengelolaan informasi pembelajaran: ")
    data2 = st.text_input("Masukkan pengelolaan situasi yang dihadapi: ")
    data3 = st.text_input("Masukkan kreativitas dalam bersikap: ")
    data4 = st.text_input("Masukkan pola komunikasi: ")
    data5 = st.text_input("Masukkan interaksi dengan lingkungan pembelajaran: ")
    data6 = st.text_input("Masukkan Pengambilan Keputusan dan Kepemimpinan: ")
    data7 = st.text_input("Masukkan minat karir dan kesesuaian potensi bidang pekerjaan: ")
    data8 = st.text_input("Masukkan saran pengembangan diri 1: ")
    data9 = st.text_input("Masukkan saran pengembangan diri 2: ")
    data10 = st.text_input("Masukkan saran pengembangan diri 3: ")
    data11 = st.text_input("Masukkan saran pengembangan diri 4: ")
    submitted = st.form_submit_button(label="Submit")

    # ini disini data nama dan data 1 - 10 dimasukin ke database dulu

    if submitted:
        # Mulai dari sini, sistem rekomendasinya berjalan
        df_new = pd.DataFrame(columns=['Pengelolaan informasi pembelajaran', 'Pengelolaan situasi yang dihadapi', 'Kreativitas dalam bersikap', 'Pola Komunikasi', 'Interaksi dengan lingkungan pembelajaran', 'Pengambilan Keputusan dan Kepemimpinan', 'Minat Karir dan Kesesuaian potensi bidang pekerjaan', 'Saran Pengembangan Diri 1', 'Saran Pengembangan Diri 2', 'Saran Pengembangan Diri 3', 'Saran Pengembangan Diri 4'])

        item_df = pd.read_csv('training_data_cleaned_translated.csv')

        df_new.loc[len(df_new)] = [data1, data2, data3, data4, 
                                data5, data6, data7, data8,
                                data9, data10, data11]

        df_cleaned_new = sistem_rekomendasi_modul.get_user_input(df_new)
        item_ranking_new, item_ranking_aggregated, item_df  = sistem_rekomendasi_modul.tfidf_new(df_cleaned_new, item_df)
        top_3_new, top_3_aggregated = sistem_rekomendasi_modul.result(item_ranking_new, item_ranking_aggregated, item_df)

        # Membuat dataframe dengan index 1, 2, 3 untuk rekomendasi
        top_3_df_new = top_3_new
        top_3_df_aggregated = top_3_aggregated.set_index('Urutan')

        # Menampilkan DataFrame tanpa indeks default menggunakan Streamlit
        st.subheader("\nRekomendasi top berdasarkan agregasi skor kesamaan pengguna lain:")
        st.write(top_3_df_aggregated)

        top_3_new_joined = ', '.join(top_3_new)
        top_3_aggregated_joined = ', '.join(top_3_aggregated)

        row_dt = [nama,data1,data2,data3,data4,data5,data6,data7,data8,data9,data10,data11,top_3_new_joined,top_3_aggregated_joined]
        
        # Update database
        dt.append_row(row_dt)
        st.success("Terima kasih sudah berpartisipasi! Semoga anda senang dengan hasil rekomendasinya.")
