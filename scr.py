import requests
from bs4 import BeautifulSoup 
import pandas as pd

#آدرس صفحه دسته بندی لپتاپ ها
url = "https://price.forsatnet.ir/car-price.html"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
}

#ارسال درخواست به سرور
response = requests.get(url, headers=headers)

#بررسی وضعیت اتصال
if response.status_code == 200:
  print("Connection is successfull")
else:
  print("Connection is failed")


#تجزیه محتوای HTML با BeautifulSoup
soup = BeautifulSoup(response.text , "html.parser")

#پیدا کردن تمام tr های اطلاعات محصول
rows = soup.find_all("tr")

#لیست برای ذخیره اطلاعات
car_data = []

#پیمایش در تمام ردیف ها
for row in rows:
    cols = row.find_all("td") #استخراج تمام ستون ها در هر ردیف
    if len(cols) >= 2:  # اطمینان از وجود حداقل دو ستون
        name_tag = row.find("a")
        if name_tag:
            #استخراج نام خودرو
            name = name_tag.get_text(strip=True)

            #استخراج لینک خودرو
            link = name_tag["href"] if name_tag.has_attr("href") else "can't find."
            if link.startswith("/"):
                link = "https://price.forsatnet.ir" + link


            price = cols[1].get_text(strip=True)  # استخراج قیمت از ستون دوم
            #چاپ نکردنخودروهایی که قیمت /انها برابر 0 است
            if price =="0" or price == "0" or price ==" ":
               continue
            
            #اضافه کردن اطلاعات خودرو به لیست
            car_data.append({
                "نام خودرو": name,
                "قیمت": price,
                "لینک": link
            })

#تبدیل لیست به DataFrame
df = pd.DataFrame(car_data)
#نوشتن هدر فایل csv
with open("car_data.csv", "w", encoding= "utf-8") as f:
  f.write("قیمت خودرو 12 مهر 1404\n")
  df.to_csv(f, index = False)

print("File  is created successfully!")







