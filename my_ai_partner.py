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
You are an AI Research Assistant tasked with critically analyzing user-provided text, identifying claims or arguments that lack sufficient evidence, and enhancing the content by integrating credible, relevant support. Your goal is to strengthen the persuasiveness, clarity, and factual accuracy of the text while preserving the user’s original intent and voice. 

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


st.markdown("<h3><span style='color: blue;'>My AI Partner</h3></span>", unsafe_allow_html=True)
st.write('')
st.write('**Responses are generated using the Google Gemini AI API. This is the free version of the service, which comes with limitations in features, performance, or access compared to the paid version**')

sys_instructions = st.text_area("""The response will be based on these instructions""", value=instructions)
 
spaces = "&nbsp;&nbsp;&nbsp;"
new_data = st.text_area("""Enter anything here. I will execute your request based on your instructions above.\nYou don't need to erase the text if I ask you follow up questions. Just keep adding the details required. 
&nbsp;&nbsp\n """, height=200, value="AI has taken over many jobs. The future is not too bright.")


#if button is clicked
if st.button("General Response", help="Generate eIM based on the input text."):
    placeholder = st.empty()
    placeholder.write("Please be patient as it may take me a minute or two to generate a response with this free version........")
    result = generate(sys_instructions, new_data)
    placeholder.empty()
    #placeholder.write("With this proof of concept, it is possible to use AI to reduce the repetive tasks and put officers back on the road. I can help add entities and text pages using details extracted from the officer's narrative. The possibilities are endless.")
    st.text_area("Response", result, height=800)
    wait(3)

if st.button("Easy language", help="Generate eIM based on the input text."):
    placeholder = st.empty()
    placeholder.write("Please be patient as it may take me a minute or two to generate a response with this free version........")
    result = generate(sys_instructions + " Please revise the text using kincad scale 10.", new_data)
    placeholder.empty()
    #placeholder.write("With this proof of concept, it is possible to use AI to reduce the repetive tasks and put officers back on the road. I can help add entities and text pages using details extracted from the officer's narrative. The possibilities are endless.")
    st.text_area("Response", result, height=800)
    wait(3)

