from flask import Flask, render_template
import json
import urllib.request

aplikasi = Flask(__name__, template_folder='template')

#memanggil data json
url = "https://covid19.mathdro.id/api/deaths"
f = urllib.request.urlopen(url).read().decode()
# Reading from file 
data = json.loads(f) 


datacovid = []
#menambahkan data kedalam dictionary kemudian input kedalam list
for i in range(10):
    covid =  dict()
    covid['Negara'] = data[i]["countryRegion"]
    covid['Positif'] = data[i]["confirmed"]
    covid['meninggal'] = data[i]["deaths"]
    covid['sembuh'] = data[i]["recovered"]
    covid['dirawat'] = data[i]["active"]
    datacovid.append(covid)

# menambahkan data positif, meninggal dan sembuh dari dictionary
listsembuh = []
listmeninggal = []
listpositif = []

for x in range (10):
    listpositif.append(datacovid[x]['Positif'])
    listmeninggal.append(datacovid[x]['meninggal'])
    listsembuh.append(datacovid[x]['sembuh'])

#menghitung persentase dari jumlah meninggal dan sembuh
persensembuh = list(map(lambda x, y : x / y * 100, listsembuh, listpositif))
persenmeninggal = list(map(lambda x, y : x / y * 100, listmeninggal, listpositif))


#memasukan persentase tadi kedalam data covid
for i in range(10):
    datacovid[i]['recopercentage'] = persensembuh[i]
    datacovid[i]['diepercentage'] = persenmeninggal[i]


def filtering(x):
    if x > 2.6:
        return True
    else:
        return False

@aplikasi.route('/')
def home():

    return render_template('index.html',covid = datacovid)


@aplikasi.route('/sorted')
def sorting():

    sortdata = sorted(datacovid, key = lambda i : i['Negara'])

    return render_template ('sorted.html', covid = sortdata)

@aplikasi.route('/filter')
def percentage():
    datafilter = []
    filterdata = filter(filtering, persenmeninggal)
    for i in filterdata:
        indek = persenmeninggal.index(i)
        dict_filter = dict()
        dict_filter['Negara'] = datacovid[indek]['Negara']
        dict_filter['Positif'] = datacovid[indek]['Positif']
        dict_filter['meninggal'] = datacovid[indek]['meninggal']
        dict_filter['sembuh'] = datacovid[indek]['sembuh']
        dict_filter['dirawat'] = datacovid[indek]['dirawat']
        dict_filter['recopercentage'] = datacovid[indek]['recopercentage']
        dict_filter['diepercentage'] = datacovid[indek]['diepercentage']
        datafilter.append(dict_filter)
    
    urutkan = sorted(datafilter, key = lambda i : i['diepercentage'], reverse=True)

    return render_template ('filter.html', covid = urutkan)

@aplikasi.route('/about')
def about():
    datakelompok = [
        {
            "gambar" : "https://cdn.discordapp.com/attachments/774188066562637824/807589527962648576/1.jpg",
            "nim":   "19102001",
            "nama" : "Alfi Arisandi"
        },
        {
            "gambar" : "https://cdn.discordapp.com/attachments/774188066562637824/807589523621937232/3.jpg",
            "nim":   "19102009",
            "nama" : "Ricky Ridho Oetomo"
        },
        {
            "gambar" : "https://cdn.discordapp.com/attachments/774188066562637824/807589520236085248/2.jpg",
            "nim":   "19102031",
            "nama" : "Candra Eka Saputra"
        }
    ]

    return render_template('about.html', nama = datakelompok)

aplikasi.run(debug=True)