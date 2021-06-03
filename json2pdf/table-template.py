import io

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table
from reportlab.platypus.tables import TableStyle


def make_doc():
	pdf = io.BytesIO()

	doc = SimpleDocTemplate(pdf, pagesize=letter)

	story = []
	#data dari pdfnya edit aja sesuai spacing sama JSON yang didapat
	
	data= [['00', '01', '02', '03', '04'],
	 ['10', '11', '12', '13', '14'],
	 ['20', '21', '22', '23', '24'],
	 ['30', '31', '32', '33', '34']]
	
	t=Table(data)
	
	# table stylenya untuk detail lebih lanjut lihat dokumentasi reportlab
	#
	# syntax type, koordinat awal(x,y), koordinat akhir(x,y), warna
	#
	# note: koordinat bisa negatif(-) artinya mulai dari arah sebaliknya 
	# 0,0 pojok kiri atas -1,-1 pojok kanan bawah
	#
	# melakukan set background color dari koordinat 1,1 hingga 3,3 berwarna hijau
	# 
	# TableStyle([('BACKGROUND',(1,1),(-2,-2), colors.green) atau TableStyle([('BACKGROUND',(1,1),(3,3), colors.green)

	t.setStyle(TableStyle([('BACKGROUND',(1,1),(1,1), colors.green),
	 ('TEXTCOLOR',(0,0),(1,-1), colors.red)]))

	story.append(t)

	doc.build(story)
	pdf.seek(0)

	return pdf


if __name__ == "__main__":
	
	# membuat file bernama test.pdf 
	pdf = make_doc()
	
	pdffile= open("test.pdf","wb")
	
	pdffile.write(pdf.getbuffer())
	pdffile.close()