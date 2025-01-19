import streamlit as st

def calculate_shear_resistance(bw, d, fck, fyw, Asw, s, Vsd):
    """
    Calcola la resistenza a taglio di una sezione rettangolare in cemento armato secondo NTC 2018.
    
    Parameters:
    bw (float): Larghezza della sezione (cm).
    d (float): Altezza utile della sezione (cm).
    fck (float): Resistenza caratteristica del calcestruzzo (MPa).
    fyw (float): Tensione di snervamento dei ferri trasversali (MPa).
    Asw (float): Area totale dell'armatura trasversale (cm^2).
    s (float): Interasse staffe (cm).
    Vsd (float): Taglio sollecitante di progetto (kN).
    
    Returns:
    dict: Dizionario con i valori di Vrd,max, Vrd,s e il risultato della verifica.
    """
    # Resistenza media del calcestruzzo (MPa)
    fcd = fck / 1.5  # Valore di progetto del calcestruzzo

    # Resistenza a taglio massima (Vrd,max)
    cot_theta = 1.2  # Approccio conservativo
    tan_theta = 1 / cot_theta
    Vrd_max = 0.54 * (1 - fck / 250) * bw * d * fcd * (1 / (cot_theta + tan_theta))

    # Resistenza a taglio delle staffe (Vrd,s)
    Vrd_s = (Asw / s) * fyw * d / 1.15

    # Verifica
    Vrd = min(Vrd_max, Vrd_s)
    verification = "Soddisfatta" if Vsd <= Vrd else "Non soddisfatta"

    return {
        "Vrd_max (kN)": Vrd_max / 10,  # Conversione in kN
        "Vrd_s (kN)": Vrd_s / 10,      # Conversione in kN
        "Vrd (kN)": Vrd / 10,          # Conversione in kN
        "Verifica": verification
    }

# Streamlit App
st.title("Verifica di Resistenza a Taglio per una Sezione Rettangolare (NTC 2018)")

st.sidebar.header("Parametri di Input")

# Input utente
bw = st.sidebar.number_input("Larghezza della sezione bw (cm)", min_value=10.0, value=30.0, step=1.0)
d = st.sidebar.number_input("Altezza utile della sezione d (cm)", min_value=10.0, value=50.0, step=1.0)
fck = st.sidebar.number_input("Resistenza caratteristica del calcestruzzo fck (MPa)", min_value=10.0, value=30.0, step=1.0)
fyw = st.sidebar.number_input("Tensione di snervamento dei ferri trasversali fyw (MPa)", min_value=100.0, value=450.0, step=10.0)
Asw = st.sidebar.number_input("Area totale dell'armatura trasversale Asw (cm^2)", min_value=0.1, value=2.0, step=0.1)
s = st.sidebar.number_input("Interasse staffe s (cm)", min_value=5.0, value=20.0, step=1.0)
Vsd = st.sidebar.number_input("Taglio sollecitante di progetto Vsd (kN)", min_value=1.0, value=100.0, step=1.0)

# Calcolo
if st.sidebar.button("Calcola"):
    results = calculate_shear_resistance(bw, d, fck, fyw, Asw, s, Vsd)

    # Output risultati
    st.subheader("Risultati della Verifica")
    st.write(f"**Vrd,max** (Resistenza a taglio massima): {results['Vrd_max (kN)']:.2f} kN")
    st.write(f"**Vrd,s** (Resistenza a taglio delle staffe): {results['Vrd_s (kN)']:.2f} kN")
    st.write(f"**Vrd** (Resistenza a taglio minima): {results['Vrd (kN)']:.2f} kN")
    st.write(f"**Verifica**: {results['Verifica']}")

    if results['Verifica'] == "Non soddisfatta":
        st.warning("La resistenza a taglio della sezione NON soddisfa i requisiti richiesti.")
    else:
        st.success("La resistenza a taglio della sezione soddisfa i requisiti richiesti.")
