import customtkinter as ctk
from tkinter import *
from tkinter import messagebox
import sqlite3
from sqlite3 import Error
from time import sleep as sl
import os


class BackEnd():
    def conexao_db(self):
        self.conn = sqlite3.connect('Sistema de Logins e Cadastros.db')
        self.cursor = self.conn.cursor()

    def desconecta_db(self):
        self.conn.close()

    def criar_tabela(self):
        self.conexao_db()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                Username TEXT NOT NULL,
                Surname TEXT NOT NULL,
                Email TEXT NOT NULL,
                Contato TEXT NOT NULL,
                Birthdate TEXT NOT NULL,
                Password TEXT NOT NULL,
                ConfPassword TEXT NOT NULL
            );
        ''')
        self.conn.commit()
        self.desconecta_db()

    def cadastrar_users(self):
        self.Full_name = self.username_cadastro.get().strip().title()
        self.Surname = self.apelido_cadastro.get().strip().title()
        self.Email = self.email_cadastro.get().strip()
        self.Contato = self.contato_cadastro.get().strip()
        self.Data_Nascimento = self.dT_nascimento_cadastro.get().strip()
        self.Password = self.senha.get().strip()
        self.ConfPassword = self.confirmar_senha.get().strip()

        try:
            self.conexao_db()
            self.cursor.execute("""
                INSERT INTO users(Username, Surname, Email, Contato, Birthdate, Password, ConfPassword)
                VALUES (?, ?, ?, ?, ?, ?, ?)""", (self.Full_name, self.Surname, self.Email, self.Contato, self.Data_Nascimento, self.Password, self.ConfPassword))

            if (self.Full_name == "" or self.Surname == "" or self.Email == "" or self.Contato == "" or self.Data_Nascimento == "" or self.Password == "" or self.ConfPassword == ""):
                messagebox.showerror(title='Sistema de cadastro', message="Por favor preencha todos os campos")

            elif len(self.Full_name) < 10:
                messagebox.showwarning(title='Sistema de cadastro', message="ERRO!\nEste campo exige no mínimo 10 caracteres")

            elif len(self.Password) < 6 or not any(char in '!@#$&*' for char in self.Password) or not any(char.isalpha() for char in self.Password) or not any(char.isdigit() for char in self.Password):
                messagebox.showwarning(title='Sistema de cadastro', message="Por favor leia as instruções de criação de senha")

            elif self.Password != self.ConfPassword:
                messagebox.showerror(title='Sistema de cadastro', message="ERRO!!!\nAs senhas não coincidem")

            else:
                self.conn.commit()
                messagebox.showinfo(title='Sistema de cadastro', message=f"Parabéns {self.Full_name}, Cadastro realizado com sucesso")
                self.desconecta_db()
                self.clear_entry_cadastro()
                self.frame_cadastro.place_forget()
                self.window_users()

        except Error as ex:
            messagebox.showerror(title='Sistema de cadastro', message=f"ERRO!!! {ex}\nPor favor tente novamente!")
            print(ex)
            self.desconecta_db()

    def verificar_login(self):
        self.user_login = self.username_login.get().strip().title()
        self.Password_login = self.senha_login.get().strip()

        self.conexao_db()

        try:
            self.cursor.execute("""SELECT * FROM users WHERE (Username = ? AND Password = ?)""", (self.user_login, self.Password_login))
            self.verificar_dados = self.cursor.fetchone() # Percorrendo a Tabela Users

            if self.user_login == '' or self.Password_login == '':
                messagebox.showwarning(title='Sistema de Login', message='Todos os campos devem ser preenchidos\n Por favor preencha os campos vazios!')
            elif self.verificar_dados:
                messagebox.showinfo(title='Sistema de Login', message=f'Parabéns {self.user_login}! Você já está logado\n Seja bem-vindo ao nosso sistema de login do Destrava Dev.')

                self.window_users()

            else:
                messagebox.showerror(title='Sistema de Login', message='Usuário ou senha inválido!\n ou usuário não cadastrado')
        except sqlite3.DatabaseError as e:
            messagebox.showerror(title='Sistema de Login', message=f'Erro de banco de dados: {e}')
        finally:
            self.desconecta_db()
            self.clear_entry_login()

class Application(ctk.CTk, BackEnd):
    def __init__(self):
        super().__init__()
        self.tema()
        self.windowMain()
        self.windowLogin()        
        self.criar_tabela()

    def tema(self):
        ctk.set_appearance_mode('dark')
        ctk.set_default_color_theme('dark-blue')

    def windowMain(self):
        self.geometry("1200x800")
        self.title('Sistema de Login')
        self.iconbitmap('admin.ico')
        self.resizable(False, False)
    
    def windowLogin(self):
        # Trabalhando a Imagem:
        self.img = PhotoImage(file = "login.png")
        self.lb_img = ctk.CTkLabel(self, text = None, image = self.img)
        self.lb_img.grid(row = 2, column = 0, padx = 10)

        # Titulop da Plataforma
        self.title = ctk.CTkLabel(master=self, text = "Faça Seu Login\n ou\n Cadastre-se na Plataforma!", text_color= '#63DAF0', font=("Century Gothic bold",40))
        self.title.grid(row = 0, column = 0, pady = 10)

        # Criando Frame do Formulário de Login
        self.frame_login = ctk.CTkFrame(self, width = 560, height = 780, corner_radius = 25, border_width = 2, border_color='#E72FF0')
        self.frame_login.place(x = 660, y = 10)

        # Criar as Widgets Dentro da Frame_Login!
        self.lb_title = ctk.CTkLabel(self.frame_login, text = "Faça Seu Login", text_color= "#0F52F0", font=("Century Gothic bold", 50))
        self.lb_title.grid(row = 0, column = 0, padx = 10, pady = 40)

        self.username_login = ctk.CTkEntry(self.frame_login, width= 500,placeholder_text = "Digite Seu Usuário...".center(60), placeholder_text_color= "#F0F001", text_color = "#EF1400", border_color = "#63DAF0", font=("Century Gothic bold", 25), corner_radius = 15)
        self.username_login.grid(row = 1, column = 0, padx = 15, pady = 50)

        self.senha_login = ctk.CTkEntry(self.frame_login, width = 500, placeholder_text= 'Digite sua Senha...'.center(60), placeholder_text_color= "#F0F001", border_color = "#63DAF0", text_color = "#EF1400", show = '*', font=("Century Gothic bold", 25), corner_radius = 15)
        self.senha_login.grid(row = 2, column = 0, padx = 15, pady = 30)

        self.ver_senha = ctk.CTkCheckBox(self.frame_login, text = "Clique Para Ver a Senha Digitada:", text_color= "#63DAF0", font=("Century Gothic bold", 20), corner_radius = 50, fg_color='#EF1400', command=self.verificar_checkbox_login)
        self.ver_senha.grid(row = 4, column = 0, padx = 15, pady = 20)

        self.btn_login = ctk.CTkButton(self.frame_login, width = 200, text = "Login", text_color= "#F0F001", fg_color= '#0F52F0', font=("Century Gothic bold", 20), corner_radius = 30, command = self.verificar_login)
        self.btn_login.grid(row = 5, column = 0, padx = 15, pady = 20)

        self.lb_text = ctk.CTkLabel(self.frame_login, text="Caso não seja cadastrado:", text_color= "#63DAF0", font=("Century Gothic bold", 25))
        self.lb_text.grid(row = 6, column = 0, padx = 15, pady = 20)

        self.btn_cadastro_login = ctk.CTkButton(self.frame_login, width= 200, text = "Cadastre-se", text_color= "#F0F001",hover_color= '#050', font=("Century Gothic bold", 20), corner_radius = 30, fg_color = 'green', command = self.window_cadastro)
        self.btn_cadastro_login.grid(row = 7, column = 0, padx = 15, pady = 50)

    def verificar_checkbox_login(self):
        if self.ver_senha.get():
            self.senha_login.configure(show='')
        else:
            self.senha_login.configure(show='*')

    def window_cadastro(self):
        # Remover frame_login:
        self.frame_login.place_forget()

        #criando a frame_cadastro:
        self.frame_cadastro = ctk.CTkFrame(self, width = 560, height = 780, corner_radius = 25, border_width = 2, border_color='#E72FF0', fg_color= '#18c109')
        self.frame_cadastro.place(x = 630, y = 10)

        # Criar as Widgets Dentro da Frame_Cadastro!
        self.lb_title = ctk.CTkLabel(self.frame_cadastro, text = "Faça Seu Cadastro!", text_color= "#242424", font=("Century Gothic bold", 50))
        self.lb_title.grid(row = 0, column = 0, padx = 10, pady = 20)

        self.username_cadastro = ctk.CTkEntry(self.frame_cadastro, width = 500, placeholder_text = "Digite seu nome completo".center(50), text_color = "#fdfd01", placeholder_text_color= '#8BECF5', corner_radius = 30, font=("Century Gothic bold",25), fg_color= '#463BAC', border_color = '#63DAF0')
        self.username_cadastro.grid(row = 1, column = 0, padx = 15, pady = 20)

        self.apelido_cadastro = ctk.CTkEntry(self.frame_cadastro, width = 500, placeholder_text = "Como gostaria de ser chamado".center(50), text_color = "#fdfd01", placeholder_text_color= '#8BECF5', corner_radius = 30, font=("Century Gothic bold",25), fg_color= '#463BAC', border_color = '#63DAF0')
        self.apelido_cadastro.grid(row = 2, column = 0, padx = 15, pady = 20)
        
        self.email_cadastro = ctk.CTkEntry(self.frame_cadastro, width = 500, placeholder_text = "Digite um email válido".center(50), text_color = "#fdfd01", placeholder_text_color= '#8BECF5', corner_radius = 30, font=("Century Gothic bold",25), fg_color= '#463BAC', border_color = '#63DAF0')
        self.email_cadastro.grid(row = 3, column = 0, padx = 15, pady = 20)
        
        self.contato_cadastro = ctk.CTkEntry(self.frame_cadastro, width = 500, placeholder_text = "Digite um contato válido com DDD".center(50), text_color = "#fdfd01", placeholder_text_color= '#8BECF5', corner_radius = 30, font=("Century Gothic bold",25), fg_color= '#463BAC', border_color = '#63DAF0')
        self.contato_cadastro.grid(row = 4, column = 0, padx = 15, pady = 20)
        
        self.dT_nascimento_cadastro = ctk.CTkEntry(self.frame_cadastro, width = 500, placeholder_text = "Digite Data Nascimento - d/m/y".center(50), text_color = "#fdfd01", placeholder_text_color= '#8BECF5', corner_radius = 30, font=("Century Gothic bold",25), fg_color= '#463BAC', border_color = '#63DAF0')
        self.dT_nascimento_cadastro.grid(row = 5, column = 0, padx = 15, pady = 20)
        
        self.senha = ctk.CTkEntry(self.frame_cadastro, width = 500, placeholder_text = 'Criar Senha'.center(50), text_color = "#fdfd01", placeholder_text_color= '#8BECF5', corner_radius = 30, font=("Century Gothic bold",25), fg_color= '#463BAC', border_color = '#63DAF0', show = '*')
        self.senha.grid(row = 6, column = 0,padx = 15, pady = 20)

        self.lb_alert = ctk.CTkLabel(self.frame_cadastro, text = 'A sua senha deve conter pelo menos 1-(!@#$%&*), A, a, números e > de 5 dígitos', text_color = '#2a00fc', font=("Century Gothic",12))
        self.lb_alert.grid(row = 7, column = 0,padx = 15, pady = 1)

        self.confirmar_senha = ctk.CTkEntry(self.frame_cadastro, width = 500, placeholder_text = 'Confirmar Senha'.center(50), text_color = "#fdfd01", placeholder_text_color= '#8BECF5', corner_radius = 30, font=("Century Gothic bold",25), fg_color= '#463BAC', border_color = '#63DAF0', show = '*')
        self.confirmar_senha.grid(row = 8, column = 0,padx = 15, pady = 20)

        self.mostrar_senha_cadastro = ctk.CTkCheckBox(self.frame_cadastro, text = 'Clique aqui para revelar a senha', text_color= '#1d05f7', fg_color = '#242424', font=("Century Gothic bold", 18), corner_radius = 50, command = self.verificar_checkbox_cadastro)
        self.mostrar_senha_cadastro.grid(row = 9, column = 0, padx = 15, pady = 2)

        self.btn_salvar_cadastro = ctk.CTkButton(master=self.frame_cadastro, width = 300,text = 'CADASTRAR USUÁRIO', text_color= '#F0F001',fg_color = '#061af7',hover_color = '#FF0015', corner_radius= 30, font=("Century Gothic bold",25), command = self.cadastrar_users)
        self.btn_salvar_cadastro.grid(row = 10, column = 0, padx = 15, pady = 20)

    def verificar_checkbox_cadastro(self):
        if self.mostrar_senha_cadastro.get():
            self.senha.configure(show='')
            self.confirmar_senha.configure(show='')
        else:
            self.senha.configure(show='*')
            self.confirmar_senha.configure(show='*')

    def clear_entry_cadastro(self):
        self.username_cadastro.delete(0, END)
        self.apelido_cadastro.delete(0, END)
        self.email_cadastro.delete(0, END)
        self.contato_cadastro.delete(0, END)
        self.dT_nascimento_cadastro.delete(0, END)
        self.senha.delete(0, END)
        self.confirmar_senha.delete(0, END)

    def window_users(self):
        self.frame_login.place_forget()
        self.title.grid_forget()

        # Trabalhando a Imagem:
        self.img = PhotoImage(file = "img-2-4k.png")
        self.lb_img1 = ctk.CTkLabel(self, text = None, image = self.img)
        self.lb_img1.grid(row = 1, column = 0)

        # Titulo da Plataforma
        self.lb_title_user = ctk.CTkLabel(self, text = f"Seja Muito Bem Vindo ao Destrava Dev", text_color= '#09f3fd',fg_color="#011320" ,corner_radius=30,bg_color="#011320" ,font=("Century Gothic bold", 30))
        self.lb_title_user.place(x = 80, y = 10)

        # Criar button Logout
        self.button_logout = ctk.CTkButton(master=self, width=100, text="logout".capitalize(), fg_color="#021816", text_color= '#f1fc0c',hover_color="#1f3138", corner_radius=15, bg_color="#022d34", font=("Century Gothic bold", 15), command= self.retorn_window_login)
        self.button_logout.place(x = 1090, y = 10)

    def retorn_window_login(self):
        self.lb_img1 .grid_forget()
        self.lb_title_user.place_forget()
        self.windowLogin()

    def clear_entry_login(self):
        self.username_login.delete(0, END)
        self.senha_login.delete(0, END)

if __name__ == '__main__':
    app = Application()
    app.mainloop()
