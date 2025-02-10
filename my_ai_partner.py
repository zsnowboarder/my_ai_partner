import streamlit as st
import datetime
import time
import pytz
import xml.etree.ElementTree as ET
import google.generativeai as genai
# get current date and time
 
timezone = pytz.timezone('America/Vancouver')
#today = datetime.date.today()
now = datetime.datetime.now(timezone)
#curr_date = today.strftime("%Y-%m-%d")
curr_date = now.strftime("%Y-%m-%d")
curr_time = now.strftime("%H%M")
curr_time = int(curr_time)

api_key = st.secrets["gsc_connections"]["api_key"]
genai.configure(api_key=api_key)

# this is the main instruction

instructions = "You can only do one thing. Answer the question how are you and do not answer anything else"



# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

# FUNCTIONS

def generate(inst_text, prompt_text):
 model = genai.GenerativeModel(
  model_name="gemini-1.5-pro",
  generation_config=generation_config,
  system_instruction=inst_text)
  
 responses = model.generate_content(prompt_text, stream=True)
 resp_text = ""
  
 for response in responses:
   resp_text = resp_text + response.text
 return resp_text

def is_xml_compliant(xml_string):
    try:
        ET.fromstring(xml_string)
        return "Completed. You may download the report and import to MRE for further processing."
    except ET.ParseError:
        return "Sorry, I made a mistake in the XML. Please try again."

def wait(sec=35):
 placeholdertime = st.empty()
 while True:
  time.sleep(1)
  sec = sec - 1
  placeholdertime.write("Next request: " + str(sec))
  if sec <= 0:
   placeholdertime.empty()
   break
# PROGRAM BEGIN

st.write(curr_date)


st.markdown("<h3><span style='color: blue;'>My AI Partner</h3></span>", unsafe_allow_html=True)
st.write('')
st.write('**Responses are generated using the Google Gemini AI API. This is the free version of the service, which comes with limitations in features, performance, or access compared to the paid version**')

sys_instructions = st.text_area("""Enter some instructions here""", value=instructions)
 
spaces = "&nbsp;&nbsp;&nbsp;"
new_data = st.text_area("""Enter anything here. I will execute your request based on your instructions above.\nYou don't need to erase the text if I ask you follow up questions. Just keep adding the details required. 
Example questions:\n
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;***What naming conventions were you trained on?*** \n
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;***What else can you do beside naming conventions?*** \n
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;***What is the naming convention for use of force?***"""
                        , height=200, value="The author is VA9000 Mary SIM. Victim Jane DOE (1991/02/03) was walking and suspect Bart SIMPSON (1990/01/01) assaulted victim. Witness John BROWN (1989/02/03) called police. PC VA9000 Mary SIM arrived and arrested Bart. Witness provided a statement to police. Suspect was released with conditions of no contact Jane DOE. PC VA9100 Bart BARROW assisted with canvassing in the Collingwood area and found no CCTV.")


#if button is clicked
if st.button("Generate Response", help="Generate eIM based on the input text."):
    placeholder = st.empty()
    placeholder.write("Please be patient as it may take me a minute or two to generate a response with this free version........")
    result = generate(sys_instructions, new_data)
    placeholder.empty()
    #placeholder.write("With this proof of concept, it is possible to use AI to reduce the repetive tasks and put officers back on the road. I can help add entities and text pages using details extracted from the officer's narrative. The possibilities are endless.")
    st.text_area("Response", result, height=800)
    wait(3)

