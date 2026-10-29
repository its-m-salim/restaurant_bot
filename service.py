from connection import *




async def create_user(username, full_name, tg_id):
    try:
        conn = await connection_db()
        await conn.execute("""
        insert into users(username, full_name, telegram_id) values
            ($1, $2, $3)
""", username, full_name, str(tg_id))
        return True
    except Exception as error:
        print(f"{type(error)}: {error} scu.py")     
    finally:
        await conn.close()   




async def get_all_dishes():
    try:
        conn = await connection_db()
        dishes = await conn.fetch("""
        select * from dishes
        
""")
        return dishes
    except Exception as error:
        print(f"{type(error)}: {error} sgb.py")     
    finally:
        await conn.close()   





async def delete_dishs(b_id):
    try:
        conn = await connection_db()
        result = await conn.fetchrow("""
        delete from dishes where
        id = $1
        returning id
""", int(b_id))
        return result
    except Exception as error:
        print(f"{type(error)}: {error} sdb.py")     
        return False
    finally:
        await conn.close()   



async def profile(tg_id):
    try:
        conn = await connection_db()
        user = await conn.fetchrow("""
        select * from users where telegram_id = $1
""", str(tg_id))
        return user
    except Exception as error:
        print(f"{type(error)}: {error} sp.py")    
        return False 
    finally:
        await conn.close()   



async def get_dish_pic(dish_id):
    try:
        conn = await connection_db()
        dish_photo = await conn.fetchrow("""
        select photo_file_id 
        from dishes where
        id = $1
""", int(dish_id))

        return dish_photo

    except Exception as error:
        print(f"{type(error)}: {error} sdp.py")     
    finally:
        await conn.close()   

        




async def about_dish(dish_id):
    try:
        conn = await connection_db()
        dish = await conn.fetchrow("""
        select * from dishes where id = $1
""", int(dish_id))
        return dish
    except Exception as error:
        print(f"{type(error)}: {error} sad.py")    
        return False 
    finally:
        await conn.close()   




async def get_categories():
    try:
        conn = await connection_db()
        category = await conn.fetch("""
        select * from categories
""")
        return category
    except Exception as error:
        print(f"{type(error)}: {error} sgc.py")     
        return False
    finally:
        await conn.close()   





async def become_admin(tg_id):
    try:
        conn = await connection_db()
        admin = await conn.fetchrow("""
        update users
        set is_admin = true
        where telegram_id = $1
        returning id
""", str(tg_id))

        if not admin:
            return False
        return True
    except Exception as error:
        print(f"{type(error)}: {error} sba.py")     
    finally:
        await conn.close()   


async def set_password(password, tg_id):
    try:
        conn = await connection_db()
        await conn.execute("""
        update users
        set password = $1
        where telegram_id = $2
""", password, str(tg_id))
        return True
    except Exception as error:
        print(f"{type(error)}: {error} ssp.py")     
        return True
    finally:
        await conn.close()   


async def get_category_dishes(category_id):
    try:
        conn = await connection_db()
        dishes = await conn.fetch("""
        select * from dishes
        where category_id  = $1
""", int(category_id))

        return dishes
    except Exception as error:
        print(f"{type(error)}: {error} sgcd.py")     
    finally:
        await conn.close()   


async def take_new_order(tg_id, dish_id, quantity, table_n, customer_name):
    try:
        conn = await connection_db()
        result = await conn.fetchrow("""
        insert into orders(telegram_id, dish_id, quantity, table_number, customer_name) values
            ($1, $2, $3, $4, $5)
            returning id
""", str(tg_id), int(dish_id), int(quantity), int(table_n), customer_name)

        if not result:
            return False

        return True
    except Exception as error:
        print(f"{type(error)}: {error} sto.py")  
        return False   
    finally:
        await conn.close()   