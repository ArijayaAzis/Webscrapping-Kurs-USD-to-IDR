from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.exchange-rates.org/exchange-rate-history/usd-idr')
soup = BeautifulSoup(url_get.content,"html.parser")

#find your right key here
table = soup.find('table', attrs={'class':'history-rates-data'})
table_kurs = table.find_all('a', attrs={'class':'w'})

row_length = len(table_kurs)

temp = [] #initiating a list 

for i in range(1, row_length):
#insert the scrapping process here
	# get kurs date
    Kurs_date = table.find_all('a', attrs={'class':'w'})[i].text

    # get kurs conversion    
    Kurs_change = table.find_all('span', attrs={'class':'w'})[i].text
    
    temp.append((Kurs_date,Kurs_change)) 

temp = temp[::-1]

#change into dataframe
data = pd.DataFrame(temp, columns = ('Kurs_date','Kurs_change'))

#insert data wrangling here
#Step 1 & 2 untuk mengambil nominal IDR saja
data['Kurs_change'] = data['Kurs_change'].str[-10:-4]
data['Kurs_change'] = data['Kurs_change'].str.replace(',','')
#Step 3 untuk mengubah tipe data
data['Kurs_date'] = data['Kurs_date'].astype('datetime64[ns]')
data['Kurs_change'] = data['Kurs_change'].astype('float64') 
# untuk mengatur kolom 'kurs_date' sebagai index
data = data.set_index('Kurs_date')

#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'{data["Kurs_change"].mean().round(2)}' #be careful with the " and ' 

	# generate plot
	ax = data.plot(figsize = (10,9)) 
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]

	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)