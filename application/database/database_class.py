import os
import sqlite3

DIR_SEP = os.path.sep
DATABASE_PATH = 'application{sep}database{sep}'.format(sep=DIR_SEP)


class Database:
    def __init__(self, name):
        self.name = DATABASE_PATH+name

        self.criar_tabelas()

    def __str__(self):
        return self.name.split(DIR_SEP)[-1]

    def criar_tabelas(self):
        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()

        cursor.execute('''create table if not exists estudantes
                          (id integer primary key autoincrement,
                           nome text,
                           idade integer,
                           sexo character(1),
                           unique (nome))''')

        conn.commit()
        conn.close()

    def verificar_sexo(self, sex: str):
        sexo = sex[0].upper()

        if sexo not in ['M', 'F']:
            msg = 'Valor {} nao permitido para o '.format(sex)
            msg += 'campo sexo'

            raise Exception(msg)

        return sexo

    def fetchone_estudante(self, cursor, _id):
        cursor.execute('''select id, nome, sexo,
                          idade from estudantes
                          where id=?''',
                       (_id,))

        aluno = cursor.fetchone()

        if aluno is None:
            dados = {}

        else:
            dados = {'id': aluno[0],
                     'nome': aluno[1],
                     'sexo': aluno[2],
                     'idade': aluno[3]}

        return dados

    def inserir_estudante(self, data):
        nome = data['nome']
        idade = data['idade']
        sexo = self.verificar_sexo(data['sexo'])

        self.criar_tabelas()

        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()

        cursor.execute('''insert into estudantes
                          (nome, idade, sexo)
                          values (?, ?, ?)''',
                       (nome, idade, sexo))

        aluno = self.fetchone_estudante(cursor, cursor.lastrowid)

        conn.commit()
        conn.close()

        return aluno

    def filtrar_estudantes(self, data):
        self.criar_tabelas()

        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()

        comando = self.criar_comando_filtro(data)
        cursor.execute(comando)

        result = []
        for aluno in cursor.fetchall():
            result.append({'id': aluno[0],
                           'nome': aluno[1],
                           'sexo': aluno[2],
                           'idade': aluno[3]})

        conn.close()

        return result

    def criar_comando_filtro(self, data):
        comando = 'select id, nome, sexo, idade'
        comando += ' from estudantes where '

        for k, v in data.items():
            if isinstance(v, str):
                comando += '{}=\'{}\' and '.format(k, v)

            elif isinstance(v, list):
                if any(isinstance(x, str) for x in v):
                    elementos = ['\'{}\''.format(x) for x in v]
                    elementos = ','.join(elementos)
                    comando += '{} in ({}) and '.format(k, elementos)

                else:
                    elementos = [str(x) for x in v]
                    elementos = ','.join(elementos)
                    comando += '{} in ({}) and '.format(k, elementos)
            
            else:
                comando += '{}={} and '.format(k, v)

        comando = comando[:-5]
        
        return comando

    def listar_estudantes(self):
        self.criar_tabelas()

        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()

        cursor.execute('''select id, nome, sexo,
                          idade from estudantes''')

        result = []
        for aluno in cursor.fetchall():
            result.append({'id': aluno[0],
                           'nome': aluno[1],
                           'sexo': aluno[2],
                           'idade': aluno[3]})

        conn.close()

        return result

    def deletar_estudante(self, estudante_id):
        self.criar_tabelas()

        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()

        aluno = self.fetchone_estudante(cursor, estudante_id)

        cursor.execute('''delete from estudantes
                          where id=?''',
                       (estudante_id,))

        conn.commit()
        conn.close()

        return aluno

    def alterar_estudante(self, data):
        self.criar_tabelas()

        estudante_id = data['id']

        if 'sexo' in data:
            data['sexo'] = self.verificar_sexo(data['sexo'])

        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()

        aluno = self.fetchone_estudante(cursor, estudante_id)

        if aluno:
            novos_dados = {'nome': data.get('nome', aluno['nome']),
                           'sexo': data.get('sexo', aluno['sexo']),
                           'idade': data.get('idade', aluno['idade'])}

            cursor.execute('''update estudantes
                              set nome=?, sexo=?,
                              idade=? where id=?''',
                           (novos_dados['nome'],
                            novos_dados['sexo'],
                            novos_dados['idade'],
                            estudante_id))

            aluno = self.fetchone_estudante(cursor, estudante_id)

        conn.commit()
        conn.close()

        return aluno
