import numpy as np
import streamlit as st

def calculate_shear_resistance(bw, d, fck, fyw, phi, s, bs, Vsd, theta, alpha):
    """
    Calcola la resistenza a taglio di una sezione rettangolare in cemento armato secondo NTC 2018.
    
    Parameters:
    bw (float): Larghezza della sezione (cm).
    d (float): Altezza utile della sezione (cm).
    fck (float): Resistenza caratteristica del calcestruzzo (MPa).
    fyw (float): Tensione di snervamento dei ferri trasversali (MPa).
    phi (float): diametro delle staffe (mm).
    s (float): Interasse staffe (cm).
    bs (float): braccio delle staffe (int)
    Vsd (float): Taglio sollecitante di progetto (kN).
    theta (float): Angolo di inclinazione dei puntoni (gradi).
    
    Returns:
    dict: Dizionario con i valori di Vrd,max, Vrd,s e il risultato della verifica.
    """
    ns = 100/s #numero di staffe in un metro 
    Asw = (np.pi*phi**2/4)*ns*bs/10**2

    # Conversione angolo theta in radianti
    theta_rad = np.radians(theta) # * 3.14159 / 180
    tan_theta = np.tan(theta_rad)
    cot_theta = 1 / tan_theta 

    alpha_rad = np.radians(alpha) # * 3.14159 / 180
    tan_alpha = np.tan(alpha_rad)
    cot_alpha = 1 / tan_alpha

    st.write(f"cot(alpha) = {cot_alpha:.2f}")
    st.write(f"cot(atheta) = {cot_theta:.2f}")


    # Resistenza media del calcestruzzo (MPa)
    fcd = 0.85*(fck / 1.5)  # Valore di progetto del calcestruzzo
    fyd = fyw/1.15 
    wsw = ((Asw / s)*fyd)/(bw*(0.5*fcd)) #percentuale di armatura trasversale
    cot_theta_calc = np.sqrt(1/(wsw*np.sin(alpha_rad)) - 1)
    theta_calc = np.tan(cot_theta_calc)
    

    # Resistenza a taglio - compressione (Vrd,max)
    Vrd_c = 0.9 * d * bw * 0.5* fcd* (cot_alpha + cot_theta)/(1+ cot_theta**2)

    # Resistenza a taglio - trazione (Vrd,s)
    Vrd_s = (Asw / s) * fyd * 0.9* d * (cot_alpha + cot_theta) * np.sin(alpha_rad)

    # Verifica
    Vrd = min(Vrd_c, Vrd_s)
    verification = "Soddisfatta" if Vsd <= Vrd else "Non soddisfatta"

    delta_asl = 0.5*Asw # armatura tesa necessaria per assorbire la differenza tra la componente orizzontale della forza di compressione sul puntone di calcestruzzo e la
    #componente orizzontale della forza di trazione
    #sull’armatura trasversale:

    return {
        "Vrd_c": Vrd_c / 10,  # Conversione in kN
        "Vrd_s": Vrd_s / 10,      # Conversione in kN
        "Vrd": Vrd / 10,          # Conversione in kN
        "wsw": wsw, #percentuale di armatura
        "theta_calc": theta_calc,
        "Verifica": verification
    }

# Streamlit App
st.title("Verifica di Resistenza a Taglio per una Sezione Rettangolare secondo NTC 2018")

st.header("Input")

# Input utente
col1, col2 = st.columns(2)
with col1:
    bw = st.number_input("Larghezza della sezione bw (cm)", min_value=10.0, value=23.0, step=1.0)
    d = st.number_input("Altezza utile della sezione d (cm)", min_value=10.0, value=90.0, step=1.0)
    fck = st.number_input("Resistenza caratteristica del calcestruzzo fck (MPa)", min_value=10.0, value=35.0, step=1.0)
    theta = st.slider("Angolo di inclinazione dei puntoni (gradi)", min_value=22, max_value=45, value=45, step=1)
    alpha = st.slider("Angolo di inclinazione delle staffe (gradi)", min_value=0, max_value=90, value=90, step=1)
with col2:
    fyw = st.number_input("Tensione di snervamento dei ferri trasversali fyw (MPa)", min_value=100.0, value=430.0, step=10.0)
    phi = st.number_input("diametro staffe (mm)", min_value=1, value=8, step=1)
    s = st.number_input("Interasse staffe s (cm)", min_value=5.0, value=20.0, step=1.0)
    bs = st.number_input("numero di braccia delle staffe (int)", min_value=1.0, value=2.0, step=1.0)
    Vsd = st.number_input("Taglio sollecitante di progetto Vsd (kN)", min_value=1.0, value=100.0, step=1.0)

# Calcolo
results = calculate_shear_resistance(bw, d, fck, fyw, phi, s, bs, Vsd, theta, alpha)

# Output risultati
st.subheader("Risultati della Verifica")
st.write(f"**Vrd,c** (Resistenza a taglio calcestruzzo): {results['Vrd_c']:.2f} kN")
st.write(f"**Vrd,s** (Resistenza a taglio delle staffe): {results['Vrd_s']:.2f} kN")
st.write(f"**Vrd** (Resistenza a taglio minima): {results['Vrd']:.2f} kN")
st.write(f"**wsw** (percentuale di armatura resistente a taglio): {results['wsw']:.2f}")
st.write(f"**theta_calc** (theta calcolata): {results['theta_calc']:.2f}")
st.write(f"**Verifica**: {results['Verifica']}")

if results['Verifica'] == "Non soddisfatta":
    st.warning("La resistenza a taglio della sezione NON soddisfa i requisiti richiesti.")
else:
    st.success("La resistenza a taglio della sezione soddisfa i requisiti richiesti.")
