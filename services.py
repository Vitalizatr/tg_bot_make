import asyncio
import pandas as pd
import googlesheets as gs
import ann

sheet = gs.Sheets("cleaning_firm")

df_employees = pd.DataFrame()
df_admins = pd.DataFrame()
df_orders = pd.DataFrame()
df_schedule = pd.DataFrame()
df_summary = pd.DataFrame()
df_order = pd.DataFrame()
df_leads = pd.DataFrame()
df_tasks = pd.DataFrame()
df_inventory = pd.DataFrame()

async def refresh_data_1_min():
    global df_orders, df_schedule,df_summary
    while True:
        try:

            # Order_Employees
            sheet.sh_change("Order_Employees")
            data = sheet.sheet.get_all_values()
            df_orders = pd.DataFrame(data[1:], columns=["em_id","or_id","role","rt","rv","em__or_id"])

            # Schedule
            sheet.sh_change("Schedule")
            data = sheet.sheet.get_all_values()
            df_schedule = pd.DataFrame(data[1:], columns=["em_id","or_id","st","et","address","date","status"])



            #Summary
            order_counts = df_orders.groupby("em_id").size().reset_index(name="order_count")
            df_summary = df_employees.merge(order_counts, on="em_id", how="left")
            df_summary["order_count"] = df_summary["order_count"].fillna(0).astype(int)
            df_summary = df_summary[["em_id","name","phone","status","order_count"]]

            print("✅ Таблицы обновлены 1 min")

        except Exception as e:
            print("❌ Ошибка обновления таблиц:", e)

        await asyncio.sleep(60)  # повторяем каждую минуту

async def refresh_data_5_min():
    global df_employees,df_admins,df_order,df_leads
    while True:
        try:
            # Employees
            sheet.sh_change("Employees")
            data = sheet.sheet.get_all_values()
            df_employees = pd.DataFrame(data[1:], columns=["name","phone","tgId","dr","status","em_id"])
            df_employees.set_index("tgId", inplace=False)
            # Employees
            sheet.sh_change("Admins")
            data = sheet.sheet.get_all_values()
            df_admins = pd.DataFrame(data[1:], columns=["name","phone","tgId","dr","status","ad_id"])
            df_admins.set_index("tgId", inplace=False)


            # Order
            sheet.sh_change("Orders")
            data = sheet.sheet.get_all_values()
            df = pd.DataFrame(data[1:], columns=["st","data","startTime","dr","price","address","created","status","or_id","cl_id"])

            if(len(df_order) < len(df)):
                await ann.notify_users(df_employees["tgId"],"Nová objednávka")
            
            df_order = df     
            
            # Leads
            sheet.sh_change("Leads")
            data = sheet.sheet.get_all_values()
            df = pd.DataFrame(data[1:], columns=["source","name","phone","email","mes","status","created","lead_id"])

            if(len(df_leads) < len(df)):
                await ann.notify_users(df_admins["tgId"],"Nová aplikace")

            df_leads = df
            print("✅ Таблицы обновлены 5 min")
        except Exception as e:
            print("❌ Ошибка обновления таблиц:", e)

        await asyncio.sleep(300) 


async def refresh_data_10_min():
    global df_tasks,df_inventory
    while True:
        try:
            # Tasks
            sheet.sh_change("Tasks")
            data = sheet.sheet.get_all_values()
            df_tasks = pd.DataFrame(data[1:], columns=["taskId","type","description","status","created"])

            for row in df_tasks.iterrows():
                status = row["status"]
                dis = row["description"]

                if(status == "new"):
                    await ann.notify_users(df_admins["tgId"],f"New Task : {dis}")


            #Invenory
            data = sheet.sheet.get_all_values()
            df_inventory = pd.DataFrame(data[1:], columns=["name","stock","minstock","unit","itemId"])
            for row in df_inventory.iterrows():
                unit = float(row["unit"])
                minstock = float(row["minstock"])

                if unit < minstock:
                    sheet.append_task(row['name'])
            
            print("✅ Таблицы обновлены 10 min")
        except Exception as e:
            print("❌ Ошибка обновления таблиц:", e)

        await asyncio.sleep(600) 

if __name__ == "__main__":
    sheet.sh_change("Employees")
    data = sheet.sheet.get_all_values()
    df_employees = pd.DataFrame(data[1:], columns=["name","phone","tgId","dr","status","em_id"]) 
    res = df_employees[df_employees["tgId"] == str(988103602)]
    ID = res.iloc[0]["em_id"]   
    print(ID)