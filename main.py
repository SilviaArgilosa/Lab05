import flet as ft
from alert import AlertManager
from deposito_strumenti import DepositoStrumenti

FILE_STRUMENTI = "strumenti.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DAL DEPOSITO DI STRUMENTI DEL LAB03 ---
    deposito = DepositoStrumenti("Deposito Strumenti Musicali", "Alessandro Visconti")
    try:
        deposito.carica_file_strumenti(FILE_STRUMENTI)  # Carica il file
    except FileNotFoundError as e:
        alert.show_alert(f"❌ {e}")  # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile del deposito
    txt_titolo = ft.Text(value=deposito.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {deposito.get_responsabile()}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=deposito.get_responsabile(), label="Responsabile")

    # ListView per mostrare la lista di strumenti aggiornata
    lista_strumenti = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere un nuovo strumento (tipo, marca, anno, contatore posti)
    etichetta_testo = ft.Text (value = "Aggiungi nuovo strumento", size =20)
    tipo = ft.TextField(label="Tipo")
    marca = ft.TextField(label="Marca")
    anno = ft.TextField(label="Anno")

    prezzo = ft.Text(value="0") #inizializza il prezzo a zero

    #descrivo le funzioni per aggiungere\togliere valore al prezzo
    def aggiungi_prezzo(e):
        valore_iniziale = int(prezzo.value)
        prezzo.value = str(valore_iniziale + 1)
        prezzo.update()

    def rimuovi_prezzo(e):
        valore_iniziale = int(prezzo.value)
        prezzo.value = str(valore_iniziale - 1)
        prezzo.update()

    #aggiungo i bottoni vicino allo zero
    togli = ft.IconButton(icon = ft.Icons.REMOVE, icon_color = "green", on_click=rimuovi_prezzo)
    aggiungi = ft.IconButton(icon = ft.Icons.ADD, icon_color = "red", on_click=aggiungi_prezzo)

    riga_strumenti = ft.Row([tipo, marca, anno, togli, prezzo, aggiungi])

    # --- FUNZIONI APP ---
    def aggiorna_lista_strumenti():
        lista_strumenti.controls.clear()
        for strumento in deposito.strumenti_ordinati_per_marca():
            stato = "✅" if strumento.disponibile else "⛔"
            lista_strumenti.controls.append(ft.Text(f"{stato} {strumento}"))
        lista_strumenti.update()

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"

    def conferma_responsabile(e):
        deposito.set_responsabile(input_responsabile.value)
        txt_responsabile.value = f"Responsabile: {deposito.get_responsabile()}"

    # Handlers per la gestione dei pulsanti utili all'inserimento di un nuovo strumento

    def aggiungi_strumento(e):
    # legge i valori attuali dei campi (dare un nome nuovo alla variabile per non sovrascrivere l'altra)
        try:
            t = tipo.value
            m = marca.value
            a = int(anno.value)
            p = int(prezzo.value)

            if t == "" or m == "" or a == "" or p == "":
                print ("Campo mancante!")
                return None

            deposito.aggiungi_strumento(t, m, a, p)
            #aggiungiamo lo strumento al deposito usando i valori letti
            aggiorna_lista_strumenti()
            #aggiunge il nuovo strumento

            #svuota i campi e li aggiorna
            tipo.value = ""
            marca.value = ""
            anno.value = ""
            prezzo.value = "0"

            tipo.update()
            marca.update()
            anno.update()
            prezzo.update()

        except ValueError:
            alert.show_alert("Errore: Valore non valido")


    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.Button("Conferma", on_click=conferma_responsabile)

    # Pulsanti per la gestione dell'inserimento di un nuovo strumento
    btnAggiungiStrumento = ft.Button(content="Aggiungi strumento", on_click=aggiungi_strumento)


    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 3
        etichetta_testo,
        riga_strumenti,
        btnAggiungiStrumento,

        # Sezione 4
        ft.Divider(),
        ft.Text("Strumenti", size=20),
        lista_strumenti,
    )
    aggiorna_lista_strumenti()

ft.run(main)
