import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta

#класс данных работников
class Em_Data:
  def __init__(self,name,phone,tgId,dr,status,ID):
    self.name = name
    self.phone = phone
    self.tgId = tgId
    self.dr = dr
    self.status = status
    self.ID = ID

#класс данных работников
class Ad_Data:
  def __init__(self,name,phone,tgId,dr,status,ID):
    self.name = name
    self.phone = phone
    self.tgId = tgId
    self.dr = dr
    self.status = status
    self.ID = ID

#класс данных заказов
class Or_Em_Data:
  def __init__(self,em_Id,or_Id,role,rt,rv,id):
    self.Em_Id = em_Id
    self.Or_Id = or_Id
    self.role = role
    self.rt = rt
    self.rv = rv
    self.id = id

#класс данных расписания
class Sc_Data:
  def __init__(self,em_Id,or_Id,startTime,endTime,address,date):
    self.Em_Id = em_Id
    self.Or_Id = or_Id
    self.startTime = startTime
    self.endTime = endTime
    self.address= address
    self.date = date


class Sheets:
    def __init__(self,name):
        # Авторизация
        json_creds = json.loads(os.getenv("json"))

        # В случае, если переносы сломаны
        json_creds["private_key"] = json_creds["private_key"].replace("\\n", "\n")

        # Авторизация
        scope = ["https://spreadsheets.google.com/feeds",
                "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(json_creds, scope)
        client = gspread.authorize(creds)

        # Открытие таблицы по названию
        self._sheet = client.open(name)

    def sh_change(self,name):
        sheet_name = name
        if sheet_name in [ws.title for ws in self._sheet.worksheets()]:
            self.sheet = self._sheet.worksheet(sheet_name)
        else:
            print(f"Лист '{sheet_name}' не найден ❌")

    #вывод прошлых дней
    def date_past(self,days):
        result=datetime.now()-timedelta(days=days)
        return result.date()

    #вывод сегоднещней даты
    def date_now(self):
        now = datetime.now()
        return now.date()

    #сравнение дат
    def date_comparison(self,date1,date2):
        date1 = datetime.strptime(date1, "%Y-%m-%d").date()
        date2 = datetime.strptime(date2, "%Y-%m-%d").date()
        if date1 > date2:
            return True
        return False
    
    #поиск по слову Employ
    def Em_search(self, dataa,col = 3):
        self.sh_change("Employees")
        cells= self.sheet.findall(dataa, in_column=col)
        result=[]
        for a in cells:
            cell_lists  = self.sheet.range(f"A{a.row}:F{a.row}")
            name=cell_lists[0].value
            phone=cell_lists[1].value
            tgID=cell_lists[2].value
            dr=cell_lists[3].value
            status=cell_lists[4].value
            ID=cell_lists[5].value
            result.append(Em_Data(name,phone,tgID,dr,status,ID))
        return result
    
    #поиск по слову Admin
    def Ad_search(self, dataa,col = 3):
        self.sh_change("Admins")
        cells= self.sheet.findall(dataa, in_column=col)
        result=[]
        for a in cells:
            cell_lists  = self.sheet.range(f"A{a.row}:F{a.row}")
            name=cell_lists[0].value
            phone=cell_lists[1].value
            tgID=cell_lists[2].value
            dr=cell_lists[3].value
            status=cell_lists[4].value
            ID=cell_lists[5].value
            result.append(Ad_Data(name,phone,tgID,dr,status,ID))
        return result
    
    #поиск по работнике в or_em
    def search_by_or_em(self,Em_Id,col = 1):
        self.sh_change("Order_Employees")
        data = self.sheet.findall(Em_Id, in_column=col)
        result=[]
        for rows in data:
            if rows == []: break
            row  = self.sheet.range(f"A{rows.row}:F{rows.row}")
            em_Id=row[0]
            or_Id=row[1]
            role=row[2]
            rt=row[3]
            rv=row[4]
            id=row[5]
            result.append(Or_Em_Data(em_Id,or_Id,role,rt,rv,id))
        return result

    #поиск по работнике в расписание
    def search_by_sc(self,Em_Id,col=1):
        self.sh_change("Schedule")
        data = self.sheet.findall(Em_Id, in_column=col)
        result=[]
        for rows in data:
            if rows == []: break
            row  = self.sheet.range(f"A{rows.row}:F{rows.row}")
            em_Id=row[0].value
            or_Id=row[1].value
            startTime=row[2].value
            endTime=row[3].value
            address=row[4].value
            date=row[5].value
            result.append(Or_Em_Data(em_Id,or_Id,startTime,endTime,address,date))
        return result

    # Запись
    def append_data(self,st,date,startTime,dr,price,address):
        self.sh_change("Orders")
        self.sheet.append_rows([[st,date,startTime,dr,price,"new",address,self.date_now().strftime("%d.%m.%Y")]])
    def append_task(self,name):
        self.sh_change("Tasks")
        self.sheet.append_rows([["purchase",f"Buy for {name}","new",self.date_now().strftime("%d.%m.%Y")]])
                 
        

    #Удаление точной строки
    def delete_data(self,id):
        self.sh_change("Order_Employees")
        self.sheet.delete_rows(id)

     # Запись
    def update_data(self,index):
        self.sh_change("Employees")
        if(self.sheet.acell(f"E{index}").value == "active"):
            self.sheet.update(f"E{index}", [["inactive"]])
            return "inactive"
        else:
            self.sheet.update(f"E{index}", [["active"]])
            return "active"

    def update_status(self,index,status):
        self.sh_change("Orders")
        self.sheet.update(f"H{index}",[[status]])
    
if __name__ == "__main__":
    sh = Sheets("Example")
    
