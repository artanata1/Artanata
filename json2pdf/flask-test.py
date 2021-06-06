import io
from flask import Flask
from flask import request
from flask import send_file
from flask import make_response
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table
from reportlab.platypus.tables import TableStyle
from datetime import date


def make_doc(json):
	pdf = io.BytesIO()

	doc = SimpleDocTemplate(pdf, pagesize=letter)

	story = []
	
	today = date.today().strftime("%Y-%m")
	penjualan_bersih=json["penjualan"]+json["returdiskon"]
	Barang_Tersedia_dijual=json["pbjawal"]+json["hpp"]
	HPP=Barang_Tersedia_dijual+json["pbjakhir"]
	Penghasilan=penjualan_bersih-HPP
	total_beban_penjualan=json["bangkut"]+json["bsusut"]+json["brawatk"]
	total_beban=total_beban_penjualan+json["blainlain"]
	laba_bersih=Penghasilan-total_beban
	
	pajak= 0 
	#hitung pajak disini
	
	#hitung pajak berakhir
	laba_bersih_setelah_pajak=laba_bersih-pajak
	
	#data dari pdfnya edit aja sesuai spacing sama JSON yang didapat
	data= [['','Laporan Laba/Rugi', '', ''],
	 [],
	 [ 'Nama Perusahaan', json["nama"], '', ''], 											#1
	 ['Periode', today, '', ''], 													#2
	 [],																					#3
	 ['Penjualan Bersih'], 																	#4
	 ['Penjualan','','',json["penjualan"]] ,													#5
	 ['Retur Penjualan dan Diskon','','',json["returdiskon"]] ,								#6
	 ['Penjualan Bersih','','',penjualan_bersih] ,														
	 []	,																					#8
	 ['HARGA POKOK PENJUALAN']	,															#9
	 ['Persediaan Barang Jadi (awal)',json["pbjawal"],'','']	,								#10
	 ['Harga Pokok Produksi',json["hpp"],'','']	,											#11
	 ['Barang Tersedia dijual','',Barang_Tersedia_dijual,''],								
	 ['Persediaan Barang Jadi (akhir)','',json["pbjakhir"],'']	,							#13
	 ['HPP','','',HPP],																	
	 ['Laba Kotor/Penghasilan','','',Penghasilan],													#json["penjualan"]+json["returdiskon"]-(json["pbj"]+json["hpp"]+json["pbjakhir"])
	 [],																					#16
	 ['BEBAN OPERASIONAL'],
	 ['BEBAN PENJUALAN'],
	 ['Beban Angkut Penjualan',json["bangkut"],'',''],
	 ['Beban Penyusutan',json["bsusut"],'',''],
	 ['Beban Perawatan Kendaraan',json["brawatk"],'',''],
	 ['Total Beban Penjualan','',total_beban_penjualan,''],													#json["bangkut"]+json["bsusut"]+json["brawatk"]
	 [],
	 ['Beban Administrasi dan Umum'],
	 ['Beban lain-lain',json["blainlain"]],
	 ['Total Biaya Adm dan umum','',json["blainlain"]],
	 ['TOTAL BEBAN OPS & ADUM','',total_beban,''],													#json["bangkut"]+json["bsusut"]+json["brawatk"]+json["blainlain"]
	 ['LABA BERSIH USAHA SBLM PAJAK','','',laba_bersih],											#json["penjualan"]+json["returdiskon"]-(json["pbj"]+json["hpp"]+json["pbjakhir"])-(json["bangkut"]+json["bsusut"]+json["brawatk"]+json["blainlain"])
	 ['PAJAK PENGHASILAN','','',pajak],														#pajak
	 ['LABA BERSIH USAHA STLH PAJAK','','',laba_bersih_setelah_pajak],											#json["penjualan"]+json["returdiskon"]-(json["pbj"]+json["hpp"]+json["pbjakhir"])-(json["bangkut"]+json["bsusut"]+json["brawatk"]+json["blainlain"])-pajak
	 
	 ]

	t=Table(data)
	
	# table stylenya untuk detail lebih lanjut lihat dokumentasi reportlab
	#
	# syntax type, koordinat awal(x,y), koordinat akhir(x,y), warna
	#
	# note: koordinat bisa negatif(-) artinya mulai dari arah sebaliknya 
	# 0,0 pojok kiri atas -1,-1 pojok kanan bawah
	#
	# melakukan set background color dari koordinat 1,1 hingga 3,3 berwarna hijau
	
	# t.setStyle(TableStyle[param,param,.....])
	
	# TableStyle([('BACKGROUND',(1,1),(-2,-2), colors.green) atau TableStyle([('BACKGROUND',(1,1),(3,3), colors.green)
	# ('TEXTCOLOR',(0,0),(1,-1), colors.red)])

	#t.setStyle(
	#	TableStyle([
	#		('BACKGROUND',(1,1),(1,1), colors.green),
	#		('TEXTCOLOR',(0,0),(1,-1), colors.red)
	#	])
	#)

	story.append(t)

	doc.build(story)
	pdf.seek(0)

	return pdf

app = Flask(__name__)

@app.route('/postjson', methods = ['POST'])
def postJsonHandler():
	print (request.is_json)
	content = request.get_json()
	pdf=pdf = make_doc(content)
	pdffile= open("test.pdf","wb")
	
	pdffile.write(pdf.getbuffer())
	pdffile.close()
	return send_file('test.pdf', attachment_filename='test.pdf') 

app.run(host='0.0.0.0', port= 8090)