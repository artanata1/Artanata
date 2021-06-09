import io
from flask import Flask
from flask import request
from flask import send_file
from flask import make_response
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table
from reportlab.platypus.tables import TableStyle
from reportlab.platypus import Paragraph
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
	data= [[Paragraph('<b>Laporan Laba/Rugi</b>')],
	 [],
	 [ 'Nama Perusahaan', json["nama"],], 											#1
	 ['Periode', today,], 													#2
	 [],																					#3
	 [Paragraph('<b>Penjualan Bersih</b>')], 																	#4
	 ['Penjualan','','','Rp '+str(json["penjualan"])+'.00'] ,													#5
	 ['Retur Penjualan dan Diskon','','','Rp '+str(json["returdiskon"])+'.00'] ,								#6
	 ['Penjualan Bersih','','','Rp '+str(penjualan_bersih)+'.00'] ,														
	 []	,																					#8
	 [Paragraph('<b>HARGA POKOK PENJUALAN</b>')]	,															#9
	 ['Persediaan Barang Jadi (awal)','Rp '+str(json["pbjawal"])+'.00','','']	,								#10
	 ['Harga Pokok Produksi','Rp '+str(json["hpp"])+'.00','','']	,											#11
	 ['Barang Tersedia dijual','','Rp '+str(Barang_Tersedia_dijual)+'.00',''],								
	 ['Persediaan Barang Jadi (akhir)','','Rp '+str(json["pbjakhir"])+'.00','']	,							#13
	 ['HPP','','','Rp '+str(HPP)+'.00'],																	
	 ['Laba Kotor/Penghasilan','','','Rp '+str(Penghasilan)+'.00'],													#'Rp '+json["penjualan"]+'Rp '+json["returdiskon"]-('Rp '+json["pbj"]+'Rp '+json["hpp"]+'Rp '+json["pbjakhir"])+'.00'
	 [],																					#16
	 [Paragraph('<b>BEBAN OPERASIONAL</b>')],
	 [Paragraph('<b>BEBAN PENJUALAN</b>')],
	 ['Beban Angkut Penjualan','Rp '+str(json["bangkut"])+'.00','',''],
	 ['Beban Penyusutan','Rp '+str(json["bsusut"])+'.00','',''],
	 ['Beban Perawatan Kendaraan','Rp '+str(json["brawatk"])+'.00','',''],
	 ['Total Beban Penjualan','','Rp '+str(total_beban_penjualan)+'.00',''],													#'Rp '+json["bangkut"]+json["bsusut"]+json["brawatk"]
	 [],
	 [Paragraph('<b>Beban Administrasi dan Umum</b>')],
	 ['Beban lain-lain','Rp '+str(json["blainlain"])+'.00','',''],
	 ['Total Biaya Adm dan umum','','Rp '+str(json["blainlain"])+'.00'],
	 ['TOTAL BEBAN OPS & ADUM','','Rp '+str(total_beban)+'.00',''],													#json["bangkut"]+json["bsusut"]+json["brawatk"]+json["blainlain"]
	 [],
	 ['LABA BERSIH USAHA SBLM PAJAK','','','Rp '+str(laba_bersih)+'.00'],											#json["penjualan"]+json["returdiskon"]-(json["pbj"]+json["hpp"]+json["pbjakhir"])-(json["bangkut"]+json["bsusut"]+json["brawatk"]+json["blainlain"])+'.00'
	 ['PAJAK PENGHASILAN','','','Rp '+str(pajak)+'.00'],														#pajak
	 ['LABA BERSIH USAHA STLH PAJAK','','','Rp '+str(laba_bersih_setelah_pajak)+'.00'],											#json["penjualan"]+json["returdiskon"]-(json["pbj"]+json["hpp"]+json["pbjakhir"])-(json["bangkut"]+json["bsusut"]+json["brawatk"]+json["blainlain"])+'.00'-pajak
	 
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

	t.setStyle(
		TableStyle([
			('ALIGN',(1,4),(-1,-1), 'CENTER'),
			
			('LINEBEFORE',(1,6),(-1,8),1,colors.black),
			('LINEBEFORE',(1,11),(-1,16),1,colors.black),
			('LINEBEFORE',(1,20),(-1,23),1,colors.black),
			('LINEBEFORE',(1,26),(-1,28),1,colors.black),
			('LINEBEFORE',(1,30),(-1,-1),1,colors.black)
			
		])
	)

	story.append(t)

	doc.build(story)
	pdf.seek(0)

	return pdf

def postJsonHandler(request):
	content = request.get_json()
	pdf=pdf = make_doc(content)

	return send_file(pdf, attachment_filename='test.pdf') 