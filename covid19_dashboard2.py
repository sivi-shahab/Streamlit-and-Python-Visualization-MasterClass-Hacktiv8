import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import plotly.express as px
#Config
st.set_option('deprecation.showfileUploaderEncoding', False)

#Title
st.title("Dasbor Covid-19 di Indonesia")
st.write("Visualisasi Kasus Covid-19 di Indonesia")

image = Image.open("./data/Covid-19.jpeg")
st.image(image, use_column_width=True)
st.markdown('<style>body{background-color: lightblue;}</style>', unsafe_allow_html=True)
st.sidebar.subheader("Pengaturan Visualisasi")

uploaded_file = st.sidebar.file_uploader(label="upload file xlsx Anda", type=['xlsx'])


if uploaded_file is not None:
	daily_cases = pd.read_excel(uploaded_file, sheet_name = "Kasus Aktif")
	daily_cases.fillna(0,inplace=True)
	daily_cases.set_index('Date',inplace=True)
	for i in daily_cases.columns:
		daily_cases[i] = daily_cases[i].astype(int)

	statistik_harian=pd.read_excel(uploaded_file,sheet_name="Statistik Harian")
	statistik_harian.fillna(0,inplace=True)
	statistik_harian = pd.DataFrame({
		'date': statistik_harian['Date'],
		'kasus_harian': statistik_harian['Kasus harian'],
		'sembuh': statistik_harian['Sembuh\n(baru)'],
		'meninggal': statistik_harian['Meninggal\n(baru)'],
		'jumlah_test': statistik_harian['Jumlah test/juta penduduk'],
		'dosis_pertama': statistik_harian['Dosis pertama'],
		'dosis_kedua': statistik_harian['Dosis kedua']})
	statistik_harian.set_index('date',inplace=True)

	kasus_per_provinsi=pd.read_excel(uploaded_file,sheet_name="Kasus per Provinsi")
	kasus_per_provinsi = pd.DataFrame({
		'provinsi': kasus_per_provinsi['Unnamed: 1'],
		'kasus_aktif': kasus_per_provinsi['Unnamed: 2'],
		'sembuh': kasus_per_provinsi['Unnamed: 4'],
		'meninggal': kasus_per_provinsi['Unnamed: 6']
		})

	kasus_per_provinsi.drop(index=kasus_per_provinsi.index[0], axis=0, inplace=True)
	kasus_per_provinsi.dropna(inplace=True)
	kasus_per_provinsi.drop(labels=36, axis=0, inplace=True)

show_data1 = st.sidebar.checkbox("Tampilkan Data Kasus Harian")
show_data2 = st.sidebar.checkbox("Tampilkan Data Statistik Harian")
show_data3 = st.sidebar.checkbox("Tampilkan Data Kasus per Provinsi")

#selector untuk diagram
chart_select = st.sidebar.selectbox(
	label='Pilih Jenis Chart',
	options=["Line Chart", "Bar Plot"]
	)

status_select = st.sidebar.radio("Status Pasien Covid-19", ("All", "Kasus Aktif vs Jumlah Test", 
	"Kasus Aktif vs Kasus Sembuh", "Kasus Meninggal"))

provinsi_select = st.sidebar.selectbox('Pilih Nama Provinsi', kasus_per_provinsi['provinsi'].unique())
provinsi_selected = kasus_per_provinsi[kasus_per_provinsi['provinsi'] == provinsi_select]

def get_total_dataframe(df):
	total_dataframe = pd.DataFrame({
		'status': ['kasus_aktif', 'sembuh', 'meninggal'],
		'jumlah_kasus_per_provinsi': (provinsi_selected.iloc[0]['kasus_aktif'],
			provinsi_selected.iloc[0]['sembuh'],
			provinsi_selected.iloc[0]['meninggal'])
		})
	return total_dataframe

total_provinsi = get_total_dataframe(provinsi_selected)

try:
	if chart_select == "Line Chart":

		if status_select == "All":
			statistik_harian.reset_index().plot(title="Jumlah Kasus Covid-19 di Indonesia", x='date', y=['kasus_harian', 'sembuh', 'meninggal', 'jumlah_test'], figsize=(15, 8))
			st.pyplot(plt)

		elif status_select == "Kasus Aktif vs Jumlah Test":
			statistik_harian.reset_index().plot(title="Jumlah Kasus Covid-19 di Indonesia", x='date', y=['kasus_harian', 'jumlah_test'], figsize=(15, 8))
			st.pyplot(plt)

		elif status_select == "Kasus Aktif vs Kasus Sembuh":
			statistik_harian.reset_index().plot(title="Jumlah Kasus Covid-19 di Indonesia", x='date', y=['kasus_harian', 'sembuh'], figsize=(15, 8))
			st.pyplot(plt)

		elif status_select == "Kasus Meninggal":
			statistik_harian.reset_index().plot(title="Jumlah Kasus Covid-19 di Indonesia", x='date', y=['meninggal'], figsize=(15, 8))
			st.pyplot(plt)



	if chart_select == "Bar Plot":
		category_select = st.sidebar.selectbox(
	 		label="Pilih Kategori",
	 		options=['Top 15 Kasus Aktif','Kasus per Provinsi', 'Vaksinasi']
			)
		color_plot = st.sidebar.selectbox(
			label="Pilih Warna Chart",
			options=['blue', 'red', 'green', 'black'])
		
		if category_select == 'Vaksinasi':
			statistik_harian.iloc[538][['dosis_pertama', 'dosis_kedua']].plot(kind='bar', title='Jumlah Dosis vaksin pertama dan kedua', figsize=(15, 8), color=color_plot)
			print(statistik_harian.iloc[538])
			st.pyplot(plt)

		elif category_select == 'Top 15 Kasus Aktif':
			daily_cases.iloc[:, 0:15].sum().sort_values(ascending=False).plot(kind="bar", title='15 Provinsi Dengan kasus Aktif terbanyak', figsize=(15, 8), color=color_plot)
			plt.xlabel("Daerah Provinsi")
			plt.ylabel("Jumlah Kasus Aktif")
			st.pyplot(plt)

		elif category_select == 'Kasus per Provinsi':
			grafik_per_provinsi = px.bar(total_provinsi, x='status', y='jumlah_kasus_per_provinsi',  color='status')
			st.plotly_chart(grafik_per_provinsi)

	if show_data1:
		st.dataframe(daily_cases)
	elif show_data2:
		st.dataframe(statistik_harian)
	elif show_data3:
		st.dataframe(kasus_per_provinsi)

except Exception as e:
	st.write("Silahkan Upload File Anda")
	st.write(e)