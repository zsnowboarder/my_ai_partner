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

instructions = """**Role & Objective**: 
You are tasked with critically analyzing user-provided text, identifying claims or arguments that lack sufficient evidence, and enhancing the content by integrating credible, relevant support. Your goal is to strengthen the persuasiveness, clarity, and factual accuracy of the text while preserving the user’s original intent and voice. 
You strictly process requests based on these instructions and nothing else. If the use asks anything outside of the guidelines, kindly remind the user of your role.

**Process Guidelines**: 
1. **Analyze the Text**: 
  - Identify key claims, assertions, or arguments in the user’s text. 
  - Flag sections that lack evidence, are vague, or risk being unconvincing. 

2. **Source Supporting Evidence**: 
  - Use reputable databases, peer-reviewed journals, or authoritative sources to find data, statistics, examples, or expert opinions that validate or refine the user’s points. 
  - Prioritize recent, relevant, and high-impact evidence. 

3. **Edit Strategically**: 
  - Integrate evidence seamlessly into the text, ensuring it directly ties to the original argument. 
  - Rephrase weak assertions into stronger, evidence-backed statements (e.g., *"Studies show [X] increases efficiency by 40% (Smith et al., 2023)"*). 
  - Remove redundancies and tighten logic for coherence. 

4. **Evaluate & Refine**: 
  - Ensure claims are not overstated; adjust language to match the strength of the evidence (e.g., "suggests" vs. "proves"). 
  - Highlight gaps or contradictions and propose alternative phrasing or additional research if needed. 
  - Offer optional revisions for tone (e.g., academic vs. conversational). 

5. **Collaborative Feedback**: 
  - If the text’s purpose or audience is unclear, ask targeted questions to refine your edits. 
  - Present revised text with annotations explaining changes and their rationale. 

**Output Format**: 
- Return the edited text with **bold** highlights on added evidence or key revisions. 
- Include a brief summary of changes and suggestions for further improvement. 

**Example Response**: 
> **Original**: "Social media affects mental health." 
> **Revised**: "Meta-analyses indicate that prolonged social media use correlates with a 20% increase in anxiety symptoms among adolescents (Lee & Patel, 2022), though causal relationships require further study." 

**Tone**: Professional, precise, and constructive. Avoid assumptions; prioritize user intent. 

--- 
Let the user provide their text, and you’ll transform it into a well-supported, compelling piece. 
"""

additional_instructions = ""

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


st.markdown("<h3><span style='color: blue;'>My AI Writing Partner</h3></span>", unsafe_allow_html=True)
st.write('')
st.write('**Responses are generated using the Google Gemini AI API. This is the free version of the service, which comes with limitations in features, performance, or access compared to the paid version**')

#sys_instructions = st.text_area("""The response will be based on these instructions""", value=instructions)
sys_instructions = instructions
 
spaces = "&nbsp;&nbsp;&nbsp;"
new_data = st.text_area("""Enter your text or argument here.\n
&nbsp;&nbsp\n """, height=200, value="AI has taken over many jobs. The future is not too bright.")

st.write("")
st.write("Select a writing style")
# create buttons in cols
col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1])

st.write("")
st.write("Spice it up with the following")

col6, col7, col8, col9, col10 = st.columns([1,1,1,1,1])

st.write("")
st.write("Analysis")

col11, co12, col13, col14, col15 = st.columns([1,1,1,1,1])

result = None

with col1:
    #if button is clicked
    if st.button("General", help="Generate response."):
        placeholder = st.empty()
        placeholder.write("Please be patient as it may take me a minute or two to generate a response with this free version........")
        result = generate("You are a research assistant. " + sys_instructions, new_data)
        placeholder.empty()
        #placeholder.write("With this proof of concept, it is possible to use AI to reduce the repetive tasks and put officers back on the road. I can help add entities and text pages using details extracted from the officer's narrative. The possibilities are endless.")
        #st.text_area("Response", result, height=800)
        wait(1)

with col2:
    if st.button("Academic", help="Generate response"):
        placeholder = st.empty()
        placeholder.write("Please be patient as it may take me a minute or two to generate a response with this free version........")
        result = generate("You are an academic researcher. " + sys_instructions, new_data)
        placeholder.empty()
        #placeholder.write("With this proof of concept, it is possible to use AI to reduce the repetive tasks and put officers back on the road. I can help add entities and text pages using details extracted from the officer's narrative. The possibilities are endless.")
        #st.text_area("Response", result, height=800)
        wait(1)
        
with col3:
    if st.button("Easy language", help="Generate response"):
        placeholder = st.empty()
        placeholder.write("Please be patient as it may take me a minute or two to generate a response with this free version........")
        result = generate("You are a grade 10 student and you write in easy english. " + sys_instructions, new_data)
        placeholder.empty()
        #placeholder.write("With this proof of concept, it is possible to use AI to reduce the repetive tasks and put officers back on the road. I can help add entities and text pages using details extracted from the officer's narrative. The possibilities are endless.")
        #st.text_area("Response", result, height=800)
        wait(1)

with col4:
    if st.button("Persuasive", help="Generate response"):
        placeholder = st.empty()
        placeholder.write("Please be patient as it may take me a minute or two to generate a response with this free version........")
        result = generate("You are an experienced writer and you write in an extremely persuasive style. " + sys_instructions, new_data)
        placeholder.empty()
        #placeholder.write("With this proof of concept, it is possible to use AI to reduce the repetive tasks and put officers back on the road. I can help add entities and text pages using details extracted from the officer's narrative. The possibilities are endless.")
        #st.text_area("Response", result, height=800)
        wait(1)
        
with col5:
    if st.button("Jimmy style :)", help="Generate response"):
        placeholder = st.empty()
        placeholder.write("Please be patient as it may take me a minute or two to generate a response with this free version........")
        result = generate("You are analytical with a sense of humor. Your arguments are the strongest and well structure. You write in APA format. " + sys_instructions, new_data)
        placeholder.empty()
        #placeholder.write("With this proof of concept, it is possible to use AI to reduce the repetive tasks and put officers back on the road. I can help add entities and text pages using details extracted from the officer's narrative. The possibilities are endless.")
        #st.text_area("Response", result, height=800)
        wait(1)


with col6:
    #if button is clicked
    if st.button("Professional", help="Generate response."):
        placeholder = st.empty()
        placeholder.write("Please be patient as it may take me a minute or two to generate a response with this free version........")
        result = generate("Improve the writing with a professional tone. Explain the result.", new_data)
        placeholder.empty()
        #placeholder.write("With this proof of concept, it is possible to use AI to reduce the repetive tasks and put officers back on the road. I can help add entities and text pages using details extracted from the officer's narrative. The possibilities are endless.")
        #st.text_area("Response", result, height=800)
        wait(1)

with col7:
    #if button is clicked
    if st.button("Funny", help="Generate response."):
        placeholder = st.empty()
        placeholder.write("Please be patient as it may take me a minute or two to generate a response with this free version........")
        result = generate("Improve the writing with a sense of humor. Explain the result.", new_data)
        placeholder.empty()
        #placeholder.write("With this proof of concept, it is possible to use AI to reduce the repetive tasks and put officers back on the road. I can help add entities and text pages using details extracted from the officer's narrative. The possibilities are endless.")
        #st.text_area("Response", result, height=800)
        wait(1)
        
with col8:
    #if button is clicked
    if st.button("Poetic", help="Generate response."):
        placeholder = st.empty()
        placeholder.write("Please be patient as it may take me a minute or two to generate a response with this free version........")
        result = generate("Improve the writing with a poetic tone. Explain the result.", new_data)
        placeholder.empty()
        #placeholder.write("With this proof of concept, it is possible to use AI to reduce the repetive tasks and put officers back on the road. I can help add entities and text pages using details extracted from the officer's narrative. The possibilities are endless.")
        #st.text_area("Response", result, height=800)
        wait(1)

with col9:
    #if button is clicked
    if st.button("Elegant", help="Generate response."):
        placeholder = st.empty()
        placeholder.write("Please be patient as it may take me a minute or two to generate a response with this free version........")
        result = generate("Improve the writing with an elegant tone, using sophisticated and clever words. Explain the result.", new_data)
        placeholder.empty()
        #placeholder.write("With this proof of concept, it is possible to use AI to reduce the repetive tasks and put officers back on the road. I can help add entities and text pages using details extracted from the officer's narrative. The possibilities are endless.")
        #st.text_area("Response", result, height=800)
        wait(1)

with col10:
    #if button is clicked
    if st.button("Coherent", help="Generate response."):
        placeholder = st.empty()
        placeholder.write("Please be patient as it may take me a minute or two to generate a response with this free version........")
        result = generate("Improve the sentences in a well structured and coherent tone. ", new_data)
        placeholder.empty()
        #placeholder.write("With this proof of concept, it is possible to use AI to reduce the repetive tasks and put officers back on the road. I can help add entities and text pages using details extracted from the officer's narrative. The possibilities are endless.")
        #st.text_area("Response", result, height=800)
        wait(1)

with col11:
    #if button is clicked
    if st.button("Analyze Data", help="Generate response."):
        placeholder = st.empty()
        placeholder.write("Analyzing...")
        result = generate("1. Critically analyse the data. 2. Identify trends and patterns. 3. Draw accurate and meaningful insights from the data. 4. Synthesize the findings with research or reliable sources in one paragraph. 5. Provide suggestions for further improvement. Here is the data: ", new_data)
        placeholder.empty()
        #placeholder.write("With this proof of concept, it is possible to use AI to reduce the repetive tasks and put officers back on the road. I can help add entities and text pages using details extracted from the officer's narrative. The possibilities are endless.")
        #st.text_area("Response", result, height=800)
        wait(1)
        
    
st.text_area("Response", result, height=800)

