import streamlit as st
from stmol import showmol
import py3Dmol
import biotite.structure.io as bsio

st.sidebar.title(' EMSFold')
st.sidebar.write(' EMSFold is an end to end single sequence protein structure predictor based on the ESM-2 language model')

#stmol
def render_mol(pdb):
    pdbview = py3Dmol.view()
    pdbview.addModel(pdb,'pdb')
    pdbview.setStyle({'cartoon':{'color':'spectrum'}})
    pdbview.setBackgroundColor('white') #(‘0xeeeeee’)
    pdbview.zoomTo()
    pdbview.zoom(2,800)
    pdbview.spin(true)
    showmol(pdbview, height = 500, width = 800)

#protein seq input
DEFAULT_SEQ="MQAKKRYFILLSAGSCLALLFYFGGVQFRASRSHSRREEHSGRNGLHQPSPDHFWPRFADALHPFFPWDQLENEDSGVHVSPRQKRDANSSVYKGKKCRMESCFDFALCKKNGFKVYVYPQQKGEKIAESYQNILAAIEGSRFYTSDPSQACLFVLSLDTLDRDQLSPQYVHNLRSKVQSLHLWNNGRNHLIFNLYSGTWPDYTEDVGFDIGQAMLAKASISTENFRPNFDVSIPLFSKDHPRTGGERGFLKFNTIPPLRKYMLVFKGKRYLTGIGSDTRNALYHVHNGEDVLLLTTCKHGKDWQKHKDSRCDRDNTEYEKYDYREMLHNATFCLVPRGRRLGSFRFLEALQAACVPVMLSNGWELPFSEVINWNQAAVIGDERLLLQIPSTIRSIHQDKILALRQQTQFLWEAYFSSVEKIVLTTLEIIQDRIFKHISRNSLIWNKHPGGLFVLPQYSSYLGDFPYYYANLGLKPPSKFTAVIHAVTPLVSQSQPVLKLLVAAAKSQYCAQIIVLWNCDKPLPAKHRWPATAVPVIVIEGESKVMSSRFLPYDNIITDAVLSLDEDTVLSTTEVDFAFTVWQSFPERIVGYPARSHFWDNSKERWGYTSKWTNDYSMVLTGAAIYHKYYHYLYTHYLPASLKNMVDQLANCEDILMNFLVSAVTKLPPIKVTQKKQYKETMMGQTSRASRWADPDHFAQRQSCMNTFASWFGYMPLIHSQMRLDPVLFKDQVSILRKKYRDIERL"
txt = st.sidebar.text_area('Input sequence', DEFAULT_SEQ, height = 275)

#EMSFold
def update(sequence=txt):
	headers = {
		'Content-Type' : 'application/x-www-form-urlencoded',headers=headers, data=sequence)
	}
	reponse = requests.post('https://api.esmatlas.com/foldsequennce/v1/pdb/' , 
	name = sequence[:3] + sequence[-3:]
	pdb_string = response.content.decode('utf-8')

	with open( 'predicted.pdb' , 'w')  as f:
		f.write(pdb_string)
	struct = bsio.load_structure(' predicted.pdb' , extra_fields=["b_factor"])
	b_value = round(struct.b_factor.mean() , 4)

	#display protein structure
	st.subheader('Structure predicted')
	render_mol(pdb_string)
	
	#pIDDT value stored in the B-factor field
	st.subheader('pIDDT')
      	st.write('pIDDT is a pre-residue estimate of the confidence in prediction. Higher the value better the prediction')
	st.info(f'pIDDT : {b_value}')

	st.download_button(
		label = "Download PDB" ,
		data = pdb_string,
		file_name = 'predicted.pdb' ,
		mime = 'text/plain' ,
	)
predict = st.sidebar.button('Predict' , on_click=update)

if not predict:
	st.warning('Enter the sequence data!!!')
