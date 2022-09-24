import os
from googleapiclient.http import MediaFileUpload
from googleapiclient.http import MediaIoBaseDownload
from Google import Create_Service
import mimetypes
import io

CLIENT_SECRET_FILE = 'yourOAuthSecret.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']


konekapi = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
path_up = "./Upload"
idfolder = 'folderId'
files = []
daftarfile = []

kueri = f"parents = '{idfolder}' and trashed = false"

def upload():
    for nmfile in os.listdir(path_up):
        mime = mimetypes.MimeTypes().guess_type(nmfile)[0]
        print("Sedang mengupload file : ",nmfile," mimeType : ",mime)
        metadata = {
            'name' : nmfile,
            'parents' : [idfolder],
            'mimeType' : mime
        }
        uploadmedia = MediaFileUpload("./Upload/{0}".format(nmfile), mimetype=mime, resumable=True)

        konekapi.files().create(
            body = metadata,
            media_body = uploadmedia,
            fields = 'id'
        ).execute()
        
def daftar():
    page_token = None
    nomor = 0
    while True :
        response = konekapi.files().list(q=kueri,spaces='drive', fields = 'nextPageToken,''files(id,name)',pageToken = page_token).execute()
        for file in response.get('files', []):
            namafile = file.get("name")
            idfile = file.get("id")
            daftarfile.append(idfile)
            print("[",nomor, "]. ", namafile, " id : " , idfile)
            nomor += 1
        files.extend(response.get('files',[]))
        page_token = response.get('nextPageToken', None)
        if page_token is None :
            break


def download():
    daftar()
    print("\n")
    nomorurut = int(input("Masukkan [index] file yang akan diunduh : "))
    idfiledw = daftarfile[nomorurut]
    permintaan = konekapi.files().get_media(fileId=idfiledw)
    fileinfo = konekapi.files().get(fileId=idfiledw).execute()
    namafile = fileinfo.get("name")
    print(f'Sedang mengunduh : {namafile} .....')
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fd=fh, request=permintaan)
    done = False
    while not done :
        done = downloader.next_chunk()
        print(f'\n{namafile} selesai diunduh !\n')

    fh.seek(0)

    with open (os.path.join('./Download', namafile), 'wb') as f :
        f.write(fh.read())
        f.close

def menu():
    pilih = int(input("Selamat datang\n1. Lihat daftar\t2. Unduh berkas\t3. Unggah berkas \n(1, 2, 3)?: \n"))
    match pilih :
        case 0 :
            exit()
        case 1 :
            print("Daftar file : [index]")
            daftar()
            print("\n")
            menu()
        case 2 : 
            download()
            print("\n")
            menu()
        case 3 : 
            upload()
            print("\n")
            menu()
        case default :
            print("pilihan tidak tersedia")
            print("\n")
            menu()
    
if __name__ == "__main__":
    menu()