#!/usr/bin/env python3
"""
💰 Gerenciador de Despesas Pessoais
Interface gráfica moderna com CustomTkinter.
"""

import os
from datetime import datetime
from tkinter import messagebox

# Força o backend X11 no Linux para corrigir renderização ruim no Wayland
os.environ["GDK_BACKEND"] = "x11"

import customtkinter as ctk

import database as db
from graficos import criar_grafico_barras, criar_grafico_pizza

# ─── Configurações de Escala e Renderização (Correção Linux) ──────────
ctk.deactivate_automatic_dpi_awareness()

# ─── Tema e cores ─────────────────────────────────────────────────────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

CORES = {
    "bg_escuro": "#2b2b2b",  # Grafite escuro - background
    "bg_card": "#353535",  # Grafite médio - card/surface
    "bg_input": "#303030",  # Grafite - input/editor
    "accent": "#5d7bae",  # Azul suave
    "accent_hover": "#3d5478",  # Azul escuro suave
    "sucesso": "#7a9e5a",  # Verde suave
    "erro": "#b0626e",  # Vermelho suave
    "aviso": "#b8975a",  # Amarelo suave
    "texto": "#a9b1c6",  # Cinza azulado suave
    "texto_sec": "#6b7394",  # Cinza médio suave
    "borda": "#3e3e4e",  # Borda suave
    "linha_par": "#353535",  # Grafite médio
    "linha_impar": "#303030",  # Grafite
}

MESES_PT = [
    "Janeiro",
    "Fevereiro",
    "Março",
    "Abril",
    "Maio",
    "Junho",
    "Julho",
    "Agosto",
    "Setembro",
    "Outubro",
    "Novembro",
    "Dezembro",
]


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        db.inicializar_banco()

        self.title("💰 Gerenciador de Despesas")
        self.geometry("800x800")
        self.minsize(700, 600)
        self.configure(fg_color=CORES["bg_escuro"])

        self.mes_atual = datetime.now().month
        self.ano_atual = datetime.now().year
        self.despesa_selecionada = None

        self._criar_layout()
        self._atualizar_lista()

    # ─── Layout principal ─────────────────────────────────────────────
    def _criar_layout(self):
        # Header
        header = ctk.CTkFrame(
            self, fg_color=CORES["bg_card"], corner_radius=15, height=70
        )
        header.pack(fill="x", padx=15, pady=(15, 8))
        header.pack_propagate(False)

        ctk.CTkLabel(
            header,
            text="💰 Gerenciador de Despesas",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=CORES["accent"],
        ).pack(side="left", padx=20)

        # Seletor de mês/ano
        nav = ctk.CTkFrame(header, fg_color="transparent")
        nav.pack(side="right", padx=20)

        ctk.CTkButton(
            nav,
            text="◀",
            width=35,
            height=35,
            corner_radius=10,
            fg_color=CORES["bg_input"],
            hover_color=CORES["accent"],
            command=self._mes_anterior,
        ).pack(side="left", padx=3)

        self.lbl_mes = ctk.CTkLabel(
            nav,
            text="",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=CORES["texto"],
            width=180,
        )
        self.lbl_mes.pack(side="left", padx=5)
        self._atualizar_label_mes()

        ctk.CTkButton(
            nav,
            text="▶",
            width=35,
            height=35,
            corner_radius=10,
            fg_color=CORES["bg_input"],
            hover_color=CORES["accent"],
            command=self._proximo_mes,
        ).pack(side="left", padx=3)

        # Corpo: duas colunas
        corpo = ctk.CTkFrame(self, fg_color="transparent")
        corpo.pack(fill="both", expand=True, padx=15, pady=8)
        corpo.columnconfigure(0, weight=1)
        corpo.columnconfigure(1, weight=2)
        corpo.rowconfigure(0, weight=1)

        self._criar_painel_esquerdo(corpo)
        self._criar_painel_direito(corpo)

        # Rodapé com total
        rodape = ctk.CTkFrame(
            self, fg_color=CORES["bg_card"], corner_radius=15, height=55
        )
        rodape.pack(fill="x", padx=15, pady=(8, 15))
        rodape.pack_propagate(False)

        self.lbl_total = ctk.CTkLabel(
            rodape,
            text="Total: R$ 0,00",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=CORES["sucesso"],
        )
        self.lbl_total.pack(expand=True)

    # ─── Painel esquerdo: formulário + ações ──────────────────────────
    def _criar_painel_esquerdo(self, parent):
        painel = ctk.CTkFrame(parent, fg_color=CORES["bg_card"], corner_radius=15)
        painel.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        titulo = ctk.CTkLabel(
            painel,
            text="➕ Nova Despesa",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=CORES["accent"],
        )
        titulo.pack(pady=(15, 10), padx=15, anchor="w")

        # Descrição
        ctk.CTkLabel(
            painel,
            text="Descrição",
            text_color=CORES["texto_sec"],
            font=ctk.CTkFont(size=12),
        ).pack(padx=15, anchor="w")
        self.ent_desc = ctk.CTkEntry(
            painel,
            placeholder_text="Ex: Conta de luz",
            fg_color=CORES["bg_input"],
            border_color=CORES["borda"],
            corner_radius=10,
            height=36,
        )
        self.ent_desc.pack(fill="x", padx=15, pady=(2, 8))

        # Valor
        ctk.CTkLabel(
            painel,
            text="Valor (R$)",
            text_color=CORES["texto_sec"],
            font=ctk.CTkFont(size=12),
        ).pack(padx=15, anchor="w")
        self.ent_valor = ctk.CTkEntry(
            painel,
            placeholder_text="0,00",
            fg_color=CORES["bg_input"],
            border_color=CORES["borda"],
            corner_radius=10,
            height=36,
        )
        self.ent_valor.pack(fill="x", padx=15, pady=(2, 8))

        # Data
        ctk.CTkLabel(
            painel,
            text="Data",
            text_color=CORES["texto_sec"],
            font=ctk.CTkFont(size=12),
        ).pack(padx=15, anchor="w")
        self.ent_data = ctk.CTkEntry(
            painel,
            placeholder_text="DD/MM/AAAA",
            fg_color=CORES["bg_input"],
            border_color=CORES["borda"],
            corner_radius=10,
            height=36,
        )
        self.ent_data.pack(fill="x", padx=15, pady=(2, 8))
        self.ent_data.insert(0, datetime.now().strftime("%d/%m/%Y"))

        # Categoria
        ctk.CTkLabel(
            painel,
            text="Categoria",
            text_color=CORES["texto_sec"],
            font=ctk.CTkFont(size=12),
        ).pack(padx=15, anchor="w")
        categorias = db.listar_categorias()
        self._cat_map = {c[1]: c[0] for c in categorias}
        nomes = [c[1] for c in categorias]
        self.cmb_cat = ctk.CTkComboBox(
            painel,
            values=nomes,
            fg_color=CORES["bg_input"],
            border_color=CORES["borda"],
            corner_radius=10,
            dropdown_fg_color=CORES["bg_card"],
            button_color=CORES["accent"],
            height=36,
        )
        self.cmb_cat.pack(fill="x", padx=15, pady=(2, 8))
        if nomes:
            self.cmb_cat.set(nomes[0])

        # Observação
        ctk.CTkLabel(
            painel,
            text="Observação",
            text_color=CORES["texto_sec"],
            font=ctk.CTkFont(size=12),
        ).pack(padx=15, anchor="w")
        self.ent_obs = ctk.CTkEntry(
            painel,
            placeholder_text="(opcional)",
            fg_color=CORES["bg_input"],
            border_color=CORES["borda"],
            corner_radius=10,
            height=36,
        )
        self.ent_obs.pack(fill="x", padx=15, pady=(2, 12))

        # Checkbox Pago
        self.chk_paga_var = ctk.IntVar(value=0)
        self.chk_paga = ctk.CTkCheckBox(
            painel,
            text="Despesa Paga",
            variable=self.chk_paga_var,
            text_color=CORES["texto"],
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=CORES["sucesso"],
            hover_color=CORES["accent_hover"],
            border_color=CORES["borda"],
        )
        self.chk_paga.pack(padx=15, pady=(0, 15), anchor="w")

        # Botões
        btn_frame = ctk.CTkFrame(painel, fg_color="transparent")
        btn_frame.pack(fill="x", padx=15, pady=(0, 8))

        self.btn_salvar = ctk.CTkButton(
            btn_frame,
            text="💾 Salvar",
            height=38,
            corner_radius=10,
            fg_color=CORES["accent"],
            hover_color=CORES["accent_hover"],
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self._salvar_despesa,
        )
        self.btn_salvar.pack(fill="x", pady=3)

        self.btn_limpar = ctk.CTkButton(
            btn_frame,
            text="🧹 Limpar",
            height=34,
            corner_radius=10,
            fg_color=CORES["bg_input"],
            hover_color=CORES["borda"],
            font=ctk.CTkFont(size=12),
            command=self._limpar_form,
        )
        self.btn_limpar.pack(fill="x", pady=3)

        # Botões de ação (editar/excluir)
        act_frame = ctk.CTkFrame(painel, fg_color="transparent")
        act_frame.pack(fill="x", padx=15, pady=(0, 8))

        self.btn_editar = ctk.CTkButton(
            act_frame,
            text="✏️ Editar",
            height=34,
            corner_radius=10,
            fg_color="#4a8a8f",
            hover_color="#3a6e73",
            text_color="#d0d0d0",
            font=ctk.CTkFont(size=12),
            command=self._editar_despesa,
            state="disabled",
        )
        self.btn_editar.pack(fill="x", pady=2)

        self.btn_excluir = ctk.CTkButton(
            act_frame,
            text="🗑️ Excluir",
            height=34,
            corner_radius=10,
            fg_color="#8f4a55",
            hover_color="#6e3a42",
            text_color="#d0d0d0",
            font=ctk.CTkFont(size=12),
            command=self._excluir_despesa,
            state="disabled",
        )
        self.btn_excluir.pack(fill="x", pady=2)

        # Botão gráficos
        ctk.CTkButton(
            painel,
            text="📊 Ver Gráficos",
            height=38,
            corner_radius=10,
            fg_color="#7a6a9e",
            hover_color="#5e5280",
            text_color="#d0d0d0",
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self._mostrar_graficos,
        ).pack(fill="x", padx=15, pady=(5, 15))

    # ─── Painel direito: lista de despesas ────────────────────────────
    def _criar_painel_direito(self, parent):
        painel = ctk.CTkFrame(parent, fg_color=CORES["bg_card"], corner_radius=15)
        painel.grid(row=0, column=1, sticky="nsew")

        ctk.CTkLabel(
            painel,
            text="📋 Despesas do Mês",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=CORES["accent"],
        ).pack(pady=(15, 5), padx=15, anchor="w")

        # Cabeçalho da tabela
        cab = ctk.CTkFrame(
            painel, fg_color=CORES["bg_input"], corner_radius=8, height=36
        )
        cab.pack(fill="x", padx=15, pady=(5, 2))
        cab.pack_propagate(False)

        colunas = [
            ("Data", 90),
            ("Descrição", 170),
            ("Categoria", 130),
            ("Valor", 90),
            ("Status", 60),
        ]
        for texto, largura in colunas:
            ctk.CTkLabel(
                cab,
                text=texto,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=CORES["aviso"],
                width=largura,
            ).pack(side="left", padx=8)

        # Área de scroll para despesas
        self.scroll_frame = ctk.CTkScrollableFrame(
            painel,
            fg_color="transparent",
            corner_radius=10,
            scrollbar_button_color=CORES["accent"],
        )
        self.scroll_frame.pack(fill="both", expand=True, padx=15, pady=(2, 15))

    # ─── Atualizar lista de despesas ──────────────────────────────────
    def _atualizar_lista(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        despesas = db.listar_despesas(self.mes_atual, self.ano_atual)
        total = db.total_mensal(self.mes_atual, self.ano_atual)

        if not despesas:
            ctk.CTkLabel(
                self.scroll_frame,
                text="Nenhuma despesa registrada neste mês.",
                text_color=CORES["texto_sec"],
                font=ctk.CTkFont(size=13),
            ).pack(pady=40)
        else:
            for i, d in enumerate(despesas):
                cor_bg = CORES["linha_par"] if i % 2 == 0 else CORES["linha_impar"]
                row = ctk.CTkFrame(
                    self.scroll_frame,
                    fg_color=cor_bg,
                    corner_radius=8,
                    height=38,
                    cursor="hand2",
                )
                row.pack(fill="x", pady=1)
                row.pack_propagate(False)

                # Formatar data
                try:
                    dt = datetime.strptime(d["data"], "%Y-%m-%d")
                    data_fmt = dt.strftime("%d/%m/%Y")
                except ValueError:
                    data_fmt = d["data"]

                ctk.CTkLabel(
                    row,
                    text=data_fmt,
                    width=90,
                    text_color=CORES["texto"],
                    font=ctk.CTkFont(size=12),
                ).pack(side="left", padx=8)
                ctk.CTkLabel(
                    row,
                    text=d["descricao"][:25],
                    width=170,
                    text_color=CORES["texto"],
                    font=ctk.CTkFont(size=12),
                    anchor="w",
                ).pack(side="left", padx=8)
                ctk.CTkLabel(
                    row,
                    text=d["categoria"][:18],
                    width=130,
                    text_color=CORES["texto_sec"],
                    font=ctk.CTkFont(size=11),
                ).pack(side="left", padx=8)
                ctk.CTkLabel(
                    row,
                    text=f"R$ {d['valor']:,.2f}".replace(",", "X")
                    .replace(".", ",")
                    .replace("X", "."),
                    width=90,
                    text_color=CORES["erro"],
                    font=ctk.CTkFont(size=12, weight="bold"),
                ).pack(side="left", padx=8)

                status_txt = "✅" if d.get("paga", 0) else "⏳"
                ctk.CTkLabel(
                    row,
                    text=status_txt,
                    width=60,
                    text_color=CORES["texto"],
                    font=ctk.CTkFont(size=14),
                ).pack(side="left", padx=8)

                desp_id = d["id"]
                row.bind(
                    "<Button-1>", lambda _, did=desp_id: self._selecionar_despesa(did)
                )
                for child in row.winfo_children():
                    child.bind(
                        "<Button-1>",
                        lambda _, did=desp_id: self._selecionar_despesa(did),
                    )

        self.lbl_total.configure(
            text=f"Total do mês: R$ {total:,.2f}".replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )

    # ─── Navegação de meses ───────────────────────────────────────────
    def _atualizar_label_mes(self):
        self.lbl_mes.configure(text=f"{MESES_PT[self.mes_atual - 1]} {self.ano_atual}")

    def _mes_anterior(self):
        if self.mes_atual == 1:
            self.mes_atual = 12
            self.ano_atual -= 1
        else:
            self.mes_atual -= 1
        self._atualizar_label_mes()
        self._atualizar_lista()

    def _proximo_mes(self):
        if self.mes_atual == 12:
            self.mes_atual = 1
            self.ano_atual += 1
        else:
            self.mes_atual += 1
        self._atualizar_label_mes()
        self._atualizar_lista()

    # ─── CRUD ─────────────────────────────────────────────────────────
    def _validar_form(self):
        desc = self.ent_desc.get().strip()
        if not desc:
            messagebox.showwarning("Atenção", "Informe a descrição.")
            return None

        valor_txt = self.ent_valor.get().strip().replace(",", ".")
        try:
            valor = float(valor_txt)
            if valor <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Atenção", "Informe um valor válido.")
            return None

        data_txt = self.ent_data.get().strip()
        try:
            dt = datetime.strptime(data_txt, "%d/%m/%Y")
            data_iso = dt.strftime("%Y-%m-%d")
        except ValueError:
            messagebox.showwarning("Atenção", "Data inválida. Use DD/MM/AAAA.")
            return None

        cat_nome = self.cmb_cat.get()
        cat_id = self._cat_map.get(cat_nome)
        if not cat_id:
            messagebox.showwarning("Atenção", "Selecione uma categoria.")
            return None

        obs = self.ent_obs.get().strip()
        paga = self.chk_paga_var.get()
        return desc, valor, data_iso, cat_id, obs, paga

    def _salvar_despesa(self):
        dados = self._validar_form()
        if not dados:
            return

        if self.despesa_selecionada:
            db.editar_despesa(self.despesa_selecionada, *dados)
            messagebox.showinfo("Sucesso", "Despesa atualizada!")
        else:
            db.adicionar_despesa(*dados)
            messagebox.showinfo("Sucesso", "Despesa adicionada!")

        self._limpar_form()
        self._atualizar_lista()

    def _editar_despesa(self):
        if not self.despesa_selecionada:
            return
        desp = db.buscar_despesa(self.despesa_selecionada)
        if not desp:
            return

        self._limpar_form(manter_selecao=True)
        self.ent_desc.insert(0, desp["descricao"])
        self.ent_valor.insert(0, str(desp["valor"]).replace(".", ","))
        self.ent_data.delete(0, "end")
        try:
            dt = datetime.strptime(desp["data"], "%Y-%m-%d")
            self.ent_data.insert(0, dt.strftime("%d/%m/%Y"))
        except ValueError:
            self.ent_data.insert(0, desp["data"])
        self.cmb_cat.set(desp["categoria"])
        if desp["observacao"]:
            self.ent_obs.insert(0, desp["observacao"])

        if desp.get("paga", 0):
            self.chk_paga.select()
        else:
            self.chk_paga.deselect()

        self.btn_salvar.configure(text="💾 Atualizar")

    def _excluir_despesa(self):
        if not self.despesa_selecionada:
            return
        if messagebox.askyesno("Confirmar", "Deseja excluir esta despesa?"):
            db.excluir_despesa(self.despesa_selecionada)
            self._limpar_form()
            self._atualizar_lista()

    def _selecionar_despesa(self, despesa_id):
        self.despesa_selecionada = despesa_id
        self.btn_editar.configure(state="normal")
        self.btn_excluir.configure(state="normal")
        # Destacar visualmente
        for widget in self.scroll_frame.winfo_children():
            if isinstance(widget, ctk.CTkFrame):
                widget.configure(fg_color=CORES["linha_par"])
        desp = db.buscar_despesa(despesa_id)
        if desp:
            self.title(f"💰 Selecionado: {desp['descricao']}")

    def _limpar_form(self, manter_selecao=False):
        self.ent_desc.delete(0, "end")
        self.ent_valor.delete(0, "end")
        self.ent_data.delete(0, "end")
        self.ent_data.insert(0, datetime.now().strftime("%d/%m/%Y"))
        self.ent_obs.delete(0, "end")
        self.chk_paga.deselect()
        categorias = db.listar_categorias()
        if categorias:
            self.cmb_cat.set(categorias[0][1])
        self.btn_salvar.configure(text="💾 Salvar")

        if not manter_selecao:
            self.despesa_selecionada = None
            self.btn_editar.configure(state="disabled")
            self.btn_excluir.configure(state="disabled")
            self.title("💰 Gerenciador de Despesas")

    # ─── Gráficos ─────────────────────────────────────────────────────
    def _mostrar_graficos(self):
        resumo = db.resumo_por_categoria(self.mes_atual, self.ano_atual)
        if not resumo:
            messagebox.showinfo(
                "Info", "Nenhuma despesa neste mês para gerar gráficos."
            )
            return

        janela = ctk.CTkToplevel(self)
        janela.title(f"📊 Gráficos - {MESES_PT[self.mes_atual - 1]} {self.ano_atual}")
        janela.geometry("500x800")
        janela.configure(fg_color=CORES["bg_escuro"])

        categorias = [r[0] for r in resumo]
        valores = [r[1] for r in resumo]

        frame_graficos = ctk.CTkFrame(janela, fg_color="transparent")
        frame_graficos.pack(fill="both", expand=True, padx=10, pady=10)
        frame_graficos.columnconfigure(0, weight=1)
        frame_graficos.rowconfigure(0, weight=1)
        frame_graficos.rowconfigure(1, weight=1)

        criar_grafico_pizza(frame_graficos, categorias, valores, 0, linha=0)
        criar_grafico_barras(frame_graficos, categorias, valores, 0, linha=1)


# ─── Ponto de entrada ─────────────────────────────────────────────────
if __name__ == "__main__":
    app = App()
    app.mainloop()
