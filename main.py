import flet as ft
import sqlite3

def xor_encrypt_decrypt(data, key):
    return ''.join(chr(ord(c) ^ key) for c in data)

def main(page: ft.Page):
    selected_index = None
    token = str("token")
    encryption_key = 123
    token_verified = False

    def check_token(e):
        nonlocal token, token_verified
        entered_token = token_input.value
        if entered_token == "your_secret_token":
            token_verified = True
            page.add(ft.Text("Token verified!", color=ft.colors.GREEN_400))
            load_data()
        else:
            token_verified = False
            page.add(ft.Text("Invalid token!", color=ft.colors.RED_400))
        page.update()

    def select_item(e):
        nonlocal selected_index
        if selected_index is not None:
            lv.controls[selected_index].bgcolor = None
        selected_index = e.control.data
        lv.controls[selected_index].bgcolor = ft.colors.CYAN_100
        page.update()

    def add_item(e):
        nonlocal selected_index
        login_text = text_label.value
        password_text = password_label.value
        resource_text = resource_label.value
        if login_text and password_text and resource_text:
            encrypted_password = xor_encrypt_decrypt(password_text, encryption_key)
            add_to_database(login_text, encrypted_password, resource_text)
            item_container = ft.Container(
                content=ft.Text(f"{resource_text}: {login_text}", color=ft.colors.WHITE),
                data=len(lv.controls),
                on_click=select_item,
                padding=10,
                border_radius=12,
                bgcolor=ft.colors.BLACK54,
                margin=ft.Margin(top=8, bottom=8, left=0, right=0),
            )
            lv.controls.append(item_container)
            text_label.value = ""
            password_label.value = ""
            resource_label.value = ""
            page.update()

    def remove_item(e):
        nonlocal selected_index
        if selected_index is not None:
            login_text = lv.controls[selected_index].content.value.split(":")[1].strip().split(" ")[0]
            remove_from_database(login_text)
            lv.controls.pop(selected_index)
            selected_index = None
            page.update()

    def add_to_database(login_text, encrypted_password, resource_text):
        c = sqlite3.connect('my_data_base.db')
        cursor = c.cursor()
        social_text = "default"
        cursor.execute("INSERT INTO Users (login, password, resource, social) VALUES (?, ?, ?, ?)",
        (login_text, encrypted_password, resource_text, social_text))
        c.commit()
        c.close()

    def remove_from_database(login_text):
        c = sqlite3.connect('my_data_base.db')
        cursor = c.cursor()
        cursor.execute("DELETE FROM Users WHERE login = ?", (login_text,))
        c.commit()
        c.close()

    def load_data():
        lv.controls.clear()
        c = sqlite3.connect('my_data_base.db')
        cursor = c.cursor()
        cursor.execute("SELECT login, password, resource FROM Users")
        rows = cursor.fetchall()
        for row in rows:
            if token_verified:
                decrypted_password = xor_encrypt_decrypt(row[1], encryption_key)
                item_container = ft.Container(
                    content=ft.Text(f"{row[2]}: {row[0]} - {decrypted_password}", color=ft.colors.WHITE),
                    data=len(lv.controls),
                    on_click=select_item,
                    padding=10,
                    border_radius=12,
                    bgcolor=ft.colors.BLACK54,
                )
            else:
                item_container = ft.Container(
                    content=ft.Text(f"{row[2]}: {row[0]}", color=ft.colors.WHITE),
                    data=len(lv.controls),
                    on_click=select_item,
                    padding=10,
                    border_radius=12,
                    bgcolor=ft.colors.BLACK54,
                )
            lv.controls.append(item_container)
        c.close()
        page.update()

    lv = ft.ListView(expand=True, spacing=12, width=300, height=300)
    load_data()

    remove_btn = ft.ElevatedButton(
        "Remove",
        on_click=remove_item,
        bgcolor=ft.colors.RED_500,
        color=ft.colors.WHITE,
        width=150,
        height=40,
    )
    text_label = ft.TextField(
        label="Write login to add",
        width=250,
        height=40,
        bgcolor=ft.colors.BLACK,
        color=ft.colors.WHITE,
        border_radius=8,
    )
    password_label = ft.TextField(
        label="Write password to add",
        password=True,
        width=250,
        height=40,
        bgcolor=ft.colors.BLACK,
        color=ft.colors.WHITE,
        border_radius=8,
    )
    resource_label = ft.TextField(
        label="Write resource to add",
        width=250,
        height=40,
        bgcolor=ft.colors.BLACK,
        color=ft.colors.WHITE,
        border_radius=8,
    )
    add_btn = ft.ElevatedButton(
        "Add",
        on_click=add_item,
        bgcolor=ft.colors.GREEN_400,
        color=ft.colors.WHITE,
        width=150,
        height=40,
    )

    token_input = ft.TextField(
        label="Enter token to decrypt passwords",
        password=True,
        width=250,
        height=40,
        bgcolor=ft.colors.BLACK,
        color=ft.colors.WHITE,
        border_radius=8,
    )
    verify_btn = ft.ElevatedButton(
        "Verify Token",
        on_click=check_token,
        bgcolor=ft.colors.BLUE_500,
        color=ft.colors.WHITE,
        width=150,
        height=40,
    )

    page.add(
        ft.Column(
            [
                ft.Row([token_input, verify_btn], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([lv], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([text_label, password_label, resource_label], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([add_btn, remove_btn], alignment=ft.MainAxisAlignment.CENTER),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=25,
        )
    )

def data_base():
    c = sqlite3.connect('my_data_base.db')
    cursor = c.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Users(
        login TEXT NOT NULL,
        password TEXT NOT NULL,
        resource TEXT NOT NULL,
        social TEXT NOT NULL)
    """)
    c.commit()
    c.close()

data_base()
ft.app(target=main)