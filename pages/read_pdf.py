import json
import re

import streamlit as st
from PyPDF2 import PdfReader

st.title("Aplikasi PDF ke Teks & Extract Surat")

# =========================
# Helper Functions
# =========================


def normalize_text(text):
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


patterns = {
    "nomor": r"Nomor\s*:\s*(C\.Tel\.[\w\/\-\.\s]+?)\s(?=[A-Z][a-zA-Z]+\s*:|$)",
    "kepada": r"Kepada\s*:\s*(.+?)(?=\s+[A-Z][a-zA-Z]+\s*:|$)",
    "dari": r"Dari\s*:\s*(.+?)(?=\s+[A-Z][a-zA-Z]+\s*:|$)",
    "lampiran": r"Lampiran\s*:\s*(.+?)(?=\s+[A-Z][a-zA-Z]+\s*:|$)",
    "perihal": r"Perihal\s*:\s*(.*?)(?=\s*\d+\.|\s+[A-Z][a-zA-Z]+\s*:|$)",
}

tanggal_pattern = r"\d{1,2}\s+[A-Za-z]+\s+\d{4}"
lokasi_pattern = r"(STO\s+[A-Za-z]+(?:\s+[A-Za-z]+){0,2})"


def extract_fields(text):
    text = normalize_text(text)
    result = {}

    # Extract field utama
    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        result[key] = match.group(1).strip() if match else None

    # Extract tanggal (ambil 2 pertama)
    tanggal_list = re.findall(tanggal_pattern, text)
    result["tanggal_kirim"] = tanggal_list[0] if len(tanggal_list) > 0 else None
    result["tanggal_pelaksanaan"] = tanggal_list[1] if len(tanggal_list) > 1 else None

    # Extract lokasi STO
    lokasi_list = re.findall(lokasi_pattern, text)
    result["lokasi"] = list(set(lokasi_list)) if lokasi_list else []

    return result


def render_template(data):
    template = f"""
1. Menunjuk dan menindaklanjuti Notadinas dari {data.get('dari','-')} nomor {data.get('nomor','-')} tanggal {data.get('tanggal_kirim','-')} tentang {data.get('perihal','-')}.

2. Sehubungan dengan hal tersebut, maka kami memberikan izin Masuk {data.get('perihal','-')} pada tanggal {data.get('tanggal_pelaksanaan','-')}. Adapun tim yang akan melakukan pekerjaan adalah sebagai berikut :

Lokasi      : {", ".join(data.get('lokasi', []))}
PIC Mitra   : {data.get('pic_mitra','-')}
Pelaksana   : {data.get('pelaksana','-')}
Tim Teknis  :
{data.get('tim','-')}

3.	Maka dari itu, mohon untuk tim yang akan melakukan pekerjaan diatas dapat melengkapi prosedur dengan ketentuan sebagai berikut:
    1.	Jam Kerja Mitra adalah jam kerja yang berlaku di TELKOM yaitu Jam 08.00 s.d 17.00 (kecuali ada ijin khusus).
    2.	Mengisi dan menandatangani form Non-Disclosure Agreement (NDA) di pos security (Harap membawa materei Rp.10.000).
    3.	Melaksanakan protocol Kesehatan yang berlaku secara disiplin.
    4.	Menyerahkan kartu identitas (KTP/SIM/Paspor) di Pos Satpam/Security di site STO hingga pekerjaan selesai.
    5.	Melaksanakan kegiatan sesuai tanggal yang diperlukan pada hari kerja.
    6.	Mitra Kerja yang lokasi kerjanya berdasarkan kontrak, bekerjanya menetap di suatu Gedung TelkomGroup dan berjangka waktu diwajibkan selalu  menggunakan Kartu Pengenal/ ID Card yang pencetakannya sesuai dengan aturan yang berlaku.
    7.	Tidak diperkenankan masuk ke lokasi tanpa menggunakan Surat Ijin Masuk Lokasi serta Identitas yang diberikan Security (Kartu Tamu) dan dipakai selama berada dilokasi TelkomGroup. Apabila ditemukan dalam lokasi tidak menggunakan Identitas sebagai bukti lapor akan dikeluarkan dari lokasi.
    8.	Pada waktu bekerja harus diawasi oleh WASPANG / PIC Unit kerja terkait.
    9.	Memastikan standarisasi Instalasi/maintenance sesuai SOP yang berlaku.
    10.	Memastikan tidak timbul gangguan terhadap perangkat eksisting PT.TELKOM serta menjaga kebersihan, kerapian, dan ketertiban di lokasi selama kegiatan berlangsung.
    11.	Mengisi uraian kegiatan secara umum di log book satpam secara detail di log book ruang perangkat.
    12.	Setiap karyawan yang bertugas melaksanakan pekerjaan harus dilengkapi dengan sarana Keselamatan dan Kesehatan Kerja serta mentaati protokol kesehatan dan menggunakan Alat Pelindung Diri (APD) sesuai dengan jenis pekerjaan.
    13.	Harus menggunakan perlengkapan kerja (Celana Panjang, Baju Kerja, Sepatu). Tidak diperbolehkan bekerja tanpa pakaian yang tidak sopan (celana pendek/ singlet, sandal atau tanpa alas kaki).
    14.	Dilarang merokok selama melakukan pekerjaan kecuali waktu istirahat dan ditempat khusus merokok (Smoking Area).
    15.	Dilarang membuang sampah limbah hasil pekerjaan sisa bungkus makanan kesembarang tempat.
    16.	Pekerjaan pada ketinggian ≥ 2 (dua) meter wajib menggunakan Safety Belt (Body Harness), Pekerjaan di bawah tanah (manhole) wajib menggunakan Masker dan kelengkapan sesuai jenis pekerjaannya.
    17.	Tidak dibenarkan berada diluar lokasi kerja yang telah ditentukan (keluar masuk lokasi yang tidak ada hubungan pekerjaan).
    18.	Demi keselamatan kerjanya Mitra harus mengindahkan dan mentaati teguran dari pengawas K3L atau P2K3 selama bekerja dilingkungan TelkomGroup.
    19.	Dilarang menggunakan peralatan milik TelkomGroup kecuali ada ijin dari pihak yang berwenang.
    20.	Memperhatikan aspek K3L selama melaksanakan pekerjaan.
    21.	Semua alat alat kerja yang dipergunakan harus dalam kondisi baik dan tidak dapat menyebabkan kecelakaan.
    22.	Bila ada pekerjaan Pengelasan maka lokasi tersebut harus diamankan dari bahan bahan yang mudah terbakar dan disiapkan Alat Pemadam Api Ringan (APAR).
    23.	Apabila dalam pelaksanaan pekerjaan dianggap dapat membahayakan maka pekerjaan dapat dihentikan sementara. Pekerjaan dapat dilanjutkan apabila kondisi atau situasi dirasa cukup aman.
    24.	Bila selesai bekerja, alat alat kerja harus diatur rapi, semua hasil limbah kerja dibersihkan dan lingkungan kerja dirapihkan kembali.
    25.	Memberikan laporan ke Unit Security And Safety terdekat, bila mana terjadi kecelakaan  baik yang ada korban maupun yang tidak ada korban
    26.	Sewaktu melaksanakan Pekerjaan agar menjaga perangkat / instalasi yang ada, apabila terjadi gangguan akibat pekerjaan tersebut merupakan tanggung jawab saudara.
    27.	Melaporkan kondisi akhir kepada petugas Security saat mengembalikan kunci ruangan.
    28.	Mitra kerja diharuskan mengelas kembali tutup Manhole seperti semula.	
    29.	Apabila Ketentuan tersebut dilanggar maka pihak Mitra dapat diberikan surat teguran hingga sangsi administratif	

4. Untuk kepentingan pengawasan kegiatan dan koordinasi, kami menunjuk {data.get('nama_waspang','-')}.

5. Demikian surat izin ini dibuat. Atas perhatian dan kerjasamanya diucapkan terimakasih.
"""
    return template


# =========================
# Main App Flow
# =========================

uploaded_file = st.file_uploader("Pilih file PDF", type="pdf")

if uploaded_file is not None:
    reader = PdfReader(uploaded_file)

    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""

    # Preview raw text
    st.subheader("Hasil Teks")
    st.text_area("Isi PDF", text, height=250)

    # Extract
    data = extract_fields(text)

    st.subheader("Hasil Extract (JSON)")
    st.json(data)

    # Generate text
    generated_text = render_template(data)

    st.subheader("Generated Surat")
    st.text_area("Output", generated_text, height=300)

    st.download_button("Download Hasil", generated_text, file_name="surat_output.txt")
