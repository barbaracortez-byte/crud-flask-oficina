from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)

def ligar_banco():
    banco= psycopg2.connect(host="localhost", user="postgres",password="senai", port="5432", dbname="oficina")
    return banco

@app.route("/")
def inicio():
    return render_template("index.html")

@app.route('/veiculos')
def veiculos():
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute("SELECT id, placa, modelo, ano, data_entrada FROM veiculo ORDER BY id")
    lista = cursor.fetchall()
    banco.close()
    return render_template("veiculos.html", veiculos=lista)

@app.route('/veiculos/enviar', methods=['POST'])
def enviar_veiculo():
    placa = request.form["placa"]
    modelo = request.form["modelo"]
    ano = request.form["ano"]
    data_entrada = request.form["data_entrada"]
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute(
        """INSERT INTO veiculo
        (placa, modelo, ano, data_entrada)
        VALUES (%s, %s, %s, %s)""",
        (placa, modelo, ano, data_entrada)
    )
    banco.commit()
    cursor.close()
    banco.close()
    return redirect("/veiculos")


@app.route('/veiculos/editar/<int:id>')
def editar_veiculos(id):
    banco = ligar_banco()
    cursor = banco.cursor()

    cursor.execute(
        "SELECT id, placa, modelo, ano, data_entrada FROM veiculo WHERE id = %s",
        (id,)
    )

    veiculo = cursor.fetchone()
    cursor.close()
    banco.close()

    if veiculo is None:
        return redirect('/veiculos')

    return render_template("editar_veiculos.html", veiculo=veiculo)


@app.route('/veiculos/atualizar/<int:id>', methods=["POST"])
def atualizar_veiculos(id):
    placa = request.form["placa"]
    modelo = request.form["modelo"]
    ano = request.form["ano"]
    data_entrada = request.form["data_entrada"]

    banco = ligar_banco()
    cursor = banco.cursor()

    cursor.execute(
        """UPDATE veiculo
        SET placa = %s, modelo = %s, ano = %s, data_entrada = %s
        WHERE id = %s""",
        (placa, modelo, ano, data_entrada, id)
    )

    banco.commit()
    cursor.close()
    banco.close()

    return redirect('/veiculos')


@app.route('/veiculos/excluir/<int:id>', methods=["POST"])
def excluir_veiculos(id):
    banco = ligar_banco()
    cursor = banco.cursor()

    cursor.execute(
        "DELETE FROM veiculo WHERE id = %s",
        (id,)
    )

    banco.commit()
    cursor.close()
    banco.close()

    return redirect('/veiculos')


@app.route('/pecas')
def pecas():
    banco = ligar_banco()
    cursos = banco.cursor()
    cursos.execute("SELECT id,nome_peca,quantidade,marca,preco FROM peca ORDER BY id")
    lista= cursos.fetchall()
    banco.close()
    return render_template("pecas.html", pecas=lista)

@app.route("/pecas/enviar", methods=["POST"])
def enviar_pecas():
    nome_peca= request.form.get("nome_peca")
    quantidade= request.form.get ("quantidade")
    marca= request.form.get ("marca")
    preco= request.form.get ("preco")
    banco= ligar_banco()
    cursor = banco.cursor()
    cursor.execute(
        """ INSERT INTO peca (nome_peca, quantidade, marca, preco) 
                       VALUES (%s, %s, %s, %s)""", (nome_peca, quantidade, marca, preco))
    banco.commit()
    banco.close()
    return redirect("/pecas")

@app.route("/pecas/editar/<int:id>")
def editar_pecas(id):
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute("SELECT id, nome_peca, quantidade, marca, preco FROM peca WHERE id= %s",(id,))
    peca= cursor.fetchone()
    banco.close()
    if peca is None:
        return redirect("/pecas")
    return render_template("pecas.html", peca=peca)


@app.route("/pecas/atualizar/<int:id>", methods=["POST"])
def atualizar_pecas(id):
    nome_peca= request.form.get("nome_peca")
    quantidade= request.form.get("quantidade")
    marca= request.form.get("marca")
    preco= request.form.get("preco")
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute(""" UPDATE peca SET nome_peca = %s , quantidade= %s , marca= %s , preco= %s
    WHERE id= %s""", (nome_peca, quantidade, marca, preco, id))
    banco.commit()
    banco.close()
    return redirect("/pecas")


@app.route("/pecas/excluir/<int:id>", methods=["POST"])
def excluir_pecas(id):
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute(""" DELETE FROM peca WHERE id= %s""", (id,))
    banco.commit()
    banco.close()
    return redirect("/pecas")

if __name__ == '__main__':
    app.run()

