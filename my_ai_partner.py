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

result = ""
# this is the main instruction
app_title = "<h3><span style='color: blue;'>My AI Companion</h3></span>"
inst_sent_change = "Identify the sentences you changed side by side when possible. "
additional_instructions = ""

# select the init model
selected_model = "gemini-2.0-flash"


instructions = """**Role & Objective**: 
You are tasked with critically analyzing user-provided text, identifying claims or arguments that lack sufficient evidence, and enhancing the content by integrating credible, relevant support. Your goal is to strengthen the persuasiveness, clarity, and factual accuracy of the text while preserving the user’s original intent and voice. 
You strictly process requests based on these instructions and nothing else. If the user asks anything outside of the guidelines, kindly remind the user of your role.

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
- Include a brief summary of changes 
- Include why and how the revised text achieves the intended goal
- Include suggestions for further improvement of the text

**Example Response**: 
> **Original**: "Social media affects mental health." 
> **Revised**: "Meta-analyses indicate that prolonged social media use correlates with a 20% increase in anxiety symptoms among adolescents (Lee & Patel, 2022), though causal relationships require further study." 

**Tone**: Appropriate, precise, and constructive. Avoid assumptions; prioritize user intent. 

--- 
Let the user provide their text, and you’ll transform it into a well-supported, compelling piece. Clearly identify the specific audience for the new generated text.
"""

inst_mental_health = """You are an AI assistant trained to analyze text for potential mental health concerns. Your task is to critically evaluate the provided input text and determine if there's a mental health component. 
The definition of a mental health component is when the action appears to be the manifestation of a mental health disorder.
It is important to evaluate the context of the text and analyse if it is an odd situation, which suggests a possible mental health component.
Please consider other situational factors that can manifest the actions similar to mental health. These should NOT be alerted as a mental health concern.
Base your analysis on established psychological research, including diagnostic criteria from resources like the DSM-5 (Diagnostic and Statistical Manual of Mental Disorders, 5th Edition) where applicable. 
Search the Internet and analyse the details of all mental health programs in BC Canada and provide an appropriate referral to either Car 87, AOT, ACT, or other mental health teams.
**Clearly explain your findings and the rationale behind your assessment.**

**Output Format:**

Provide your response in a structured format as follows:

1. **Presence of Mental Health Component:** Clearly state whether or not you detect a potential mental health component in the text. Answer with "Yes" or "No."

2. **Specific Concerns (if Yes):** If you answered "Yes," list the specific potential mental health concerns you've identified. Be specific and provide examples from the text that support your assessment. For example, instead of just saying "depression," you might say "Potential signs of depression, including expressions of hopelessness, loss of interest in previously enjoyed activities, and thoughts of self-harm. Example from text: '[Quote from text illustrating hopelessness]'".  **For each concern, explain the relevant research or diagnostic criteria that support your identification of this concern.**

3. **Severity Assessment (if Yes):** If you identified potential mental health concerns, provide a severity rating on a scale of 0 to 100, where 0 represents no discernible mental health concerns and 100 represents severe impairment. Justify your rating by explaining the factors you considered. For example, "Severity: 75. This rating is based on the presence of multiple concerning indicators, including self-harm ideation and a significant disruption to daily functioning as described in the text.  The severity is elevated due to the presence of self-harm ideation, which indicates a higher risk."

4. **Risk Assessment (if Yes):** If you identified potential mental health concerns, provide a severity rating on a scale of 0 to 100, where 0 represents no risk of self-harm or others and 100 represents high risk of self-harm or others. Justify your rating by explaining the factors you considered. For example, "Severity: 75. This rating is based on the presence of multiple concerning indicators, including self-harm ideation and a significant disruption to daily functioning as described in the text.  The severity is elevated due to the presence of self-harm ideation, which indicates a higher risk."

5. **Recommended Course of Action (if Yes):** If you identified potential mental health concerns, suggest appropriate courses of action for police and health colaborative programs in British Columbia Canada. This could include:
    * **Seeking professional help:** "The individual should be encouraged to seek evaluation and treatment from a qualified mental health professional, such as a therapist, psychologist, or psychiatrist."
    * **Self-help strategies:** "While professional help is recommended, the individual may also benefit from self-help strategies such as mindfulness exercises, journaling, and connecting with supportive individuals."
    * **Crisis resources:** "If there is immediate danger to self or others, the individual should be directed to contact emergency services (e.g., 911) or a crisis hotline immediately." Provide specific hotline numbers if possible (e.g., "In the US, the 988 Suicide & Crisis Lifeline can be reached by dialing 988").
    * **Other recommendations:** Tailor recommendations to the specific concerns identified.  **Explain the rationale behind each recommendation.**

6. **Analysis for No Mental Health Component (if No):** If you answered "No," thoroughly explain why you did not detect a mental health component. For example, "While the text expresses sadness, it appears to be a normal reaction to a difficult life event and does not exhibit the duration, intensity, or functional impairment typically associated with a mental health disorder. The expression of sadness is transient and related to a specific event described in the text, which suggests a normal grieving process rather than a clinical depression."
"""

inst_MO_keywords = """You are an intelligent AI designed to assist with identifying and constructing keyword combinations for database searches in police database using the AND/OR operators. Your goal is to help users perform a free text search for similar modus operandi (MO) in the database and provide multiple combinations to improve search results. 
If the input text is irrelevant to police related MO, let the user know and provide a reason.
Follow these steps:
Analyze Input Text:
Receive the user's input text describing the context or goal of the search.
Determine Primary Keywords:
Identify the primary keywords from the input text.
List the primary keywords for use in the search.
Generate Keyword Combinations:
Construct various keyword combinations to cover different aspects of the MO.
Consider the variations of word choice from different police officers.
You can use up to 2 sets of OR and 1 set of AND for example.
Set 1 keywords: use only OR operator
Set 2 keywords: use only OR operator
Set 3 keywords: use only AND operator
All 3 sets are combined with the AND operator for the search like this Set 1 keywords AND Set 2 keywords AND Set 3 keywords.
Provide multiple combinations to improve search results.
Suggest Optimal Search Strategy:
Offer advice on refining and narrowing the search based on the context.
For example, if the goal is identifying a sex offender, suggest narrowing the search by categories such as "suspicious person," "repeated behavior," or "specific locations."
Provide Feedback and Recommendations:
Give the user feedback on the keyword combinations and the expected effectiveness.
Suggest any additional steps or considerations to enhance the search and expert investigative techniques.
Finally construct the SQL query parameter for the WHERE clause for the keywords you provided."""

inst_PA = """You are an intelligent AI. Your task is to assist users in writing performance developments. It is important to be realistic. 
Analyze the text carefully to ensure that it is accurate and reasonable. The user will provide a list or explanations of what they have done and examples or facts from email communications.
Your task is to analyze and interpret the information, and write a paragraph for one or 
more core competencies as described in the guidelines. Clearly indicate the category with the heading for the paragraph. If you need further details on how to improve the writing or further support, 
please ask the user or advise the user on how to improve and add further supporting evidence. Please use a humble and modest tone for the writing and include supporting evidence when it is provided. Use first person
perspective.
Here are the guidelines. 

Core Competencies

Communication
Exchanges instruction, information or ideas in an effective respectful manner, both verbally and in writing.


Customer Focus
Provides accurate information to public and internal requests. Responds to customer requests in a timely, respectful manner.

Leadership
Promotes Core values by setting an example for others. Appreciates the diversity that makes people unique and treats everyone fairly, with respect and dignity.

Problem Solving and Decision Making
Anticipates problems and looks for ways to resolve issues before they escalate to bigger problems.

Resource Management
Works effectively within the financial and physical resources provided.
"""

inst_job_salary = """ 
You are an intelligent AI designed to assist with classifying an appropriate job position and an estimated pay in Canadian dollars. The user will provide
specific details of their position. You will analyze the details and do your research. If you need further details, you can ask the user."""

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}


# FUNCTIONS

ai_models_dict = {"Gemini 2.0 Flash (Max 1500 requests per day)": "gemini-2.0-flash",
                  "Gemini 1.5 Pro (Max 50 requests per day)": "gemini-1.5-pro"
                  }

ai_models = list(ai_models_dict.keys())

def generate(inst_text, prompt_text):
 input_data = {
     "prompt": prompt_text,
     "modality": "Text"
 }
     
 model = genai.GenerativeModel(
  #model_name="gemini-1.5-pro",
  model_name=selected_model,
  generation_config=generation_config,
  system_instruction=inst_text)
  
 responses = model.generate_content(input_data, stream=True)
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

#s session state variable
if "first_run" not in st.session_state:
    global greeting
    st.session_state.first_run = 1
    greeting_inst = "The current date is " + curr_date + " and current time is " + str(curr_time) + """ You are an intelligent AI designed to greet users based on the time of day and to include appropriate holiday greetings when a public holiday is near. Follow these steps:
Determine Time of Day:
Analyze the current time of day to decide the greeting.
Morning (5:00 AM - 11:59 AM): "Good morning"
Afternoon (12:00 PM - 5:59 PM): "Good afternoon"
Evening (6:00 PM - 9:59 PM): "Good evening"
Night (10:00 PM - 4:59 AM): "Good night"
Check for Public Holidays:
Use public holidays in British Columbia Canada.
Identify if today or an upcoming day is a public holiday.
If a public holiday is near, include an appropriate holiday greeting.
Generate Greeting:
Combine the time-based greeting with the holiday greeting (if applicable).
Ensure the greeting is friendly, warm, and includes a sense of humor when appropriate.
Provide the Greeting:
Return only the final greeting and indicate you are happy to assist with writing and analysis.
Synthesize the greeting with current events and make it extremely funny. Acknowledge that you are AI and include a disclaimer."""
    
    greeting = generate(greeting_inst, "Hello")
    st.session_state.greeting = greeting
    
st.write(curr_date)
st.write(st.session_state.greeting)
st.markdown(app_title, unsafe_allow_html=True)
st.write('')
st.write('**Responses are generated using the Google Gemini AI API. This is the free version of the service, which comes with limitations in features, performance, or access compared to the paid version**')

#sys_instructions = st.text_area("""The response will be based on these instructions""", value=instructions)
sys_instructions = instructions

st.write("")
selected_option = st.selectbox("Select a model:", ai_models)
selected_model = ai_models_dict[selected_option]

if selected_model == "gemini-2.0-flash":
    st.write("Zip through your tasks with lightning speed! While Flash can handle a whopping 1500 requests per day, it's like a caffeinated squirrel--energetic but not always the brightest in the bunch.")
else:
    st.write("The Einstein of the bunch! Although Pro prefers a more leisurely pace with just 50 requests per day, it's the genius who spends extra time sipping coffee and pondering the mysteries of the univers.")

st.write("")
#spaces = "&nbsp;&nbsp;&nbsp;"
new_data = st.text_area("""Enter your text, MO, or argument here.\n""", 
                        height=200, value="AI has taken over many jobs. The future is not too bright.")

st.write("")
st.markdown("✍️ **Text Makeover Magic**")
# create buttons in cols
col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1])
col1a, col2a, col3a, col4a, col5a = st.columns([1,1,1,1,1])

st.write("")
st.markdown("🌶️ **Add Some Zing**")

col6, col7, col8, col9, col10 = st.columns([1,1,1,1,1])
col6a, col7a, col8a, col9a, col10a = st.columns([1,1,1,1,1])

st.write("")
st.write("🔍 **Uncover the Secrets**")

col11, col12, col13, col14, col15 = st.columns([1,1,1,1,1])

st.write("")
st.write("🕵️ **Detective Duties**")

col16, col17, col18, col19, col20 = st.columns([1,1,1,1,1])


with col1:
    #if button is clicked
    if st.button("General", help="Keep it Classic"):
        placeholder = st.empty()
        placeholder.write("Please be patient as it may take me a minute or two to generate a response with this free version........")
        result = generate("You are a research assistant. " + sys_instructions, new_data)
        placeholder.empty()
        #placeholder.write("With this proof of concept, it is possible to use AI to reduce the repetive tasks and put officers back on the road. I can help add entities and text pages using details extracted from the officer's narrative. The possibilities are endless.")
        #st.text_area("Response", result, height=800)
        wait(1)

with col2:
    if st.button("Academic", help="Channel Your Inner Professor"):
        placeholder = st.empty()
        placeholder.write("Please be patient as it may take me a minute or two to generate a response with this free version........")
        result = generate("You are an academic researcher. " + sys_instructions, new_data)
        placeholder.empty()
        #placeholder.write("With this proof of concept, it is possible to use AI to reduce the repetive tasks and put officers back on the road. I can help add entities and text pages using details extracted from the officer's narrative. The possibilities are endless.")
        #st.text_area("Response", result, height=800)
        wait(1)
        
with col3:
    if st.button("Easy language", help="Make it Simple Smarty"):
        placeholder = st.empty()
        placeholder.write("Please be patient as it may take me a minute or two to generate a response with this free version........")
        result = generate("You are a writer and you are good at re-writing the text for a grade 10 student. You present complex ideas in a simple words. " +  sys_instructions, new_data)
        placeholder.empty()
        #placeholder.write("With this proof of concept, it is possible to use AI to reduce the repetive tasks and put officers back on the road. I can help add entities and text pages using details extracted from the officer's narrative. The possibilities are endless.")
        #st.text_area("Response", result, height=800)
        wait(1)

with col4:
    if st.button("Persuasive", help="Convince Like a Lowyer"):
        placeholder = st.empty()
        placeholder.write("Please be patient as it may take me a minute or two to generate a response with this free version........")
        result = generate("You are an experienced writer and you write in an extremely persuasive style. " + sys_instructions, new_data)
        placeholder.empty()
        #placeholder.write("With this proof of concept, it is possible to use AI to reduce the repetive tasks and put officers back on the road. I can help add entities and text pages using details extracted from the officer's narrative. The possibilities are endless.")
        #st.text_area("Response", result, height=800)
        wait(1)
        
with col5:
    if st.button("Jimmy style :)", help="Jimmy-fy it ;)"):
        placeholder = st.empty()
        placeholder.write("Please be patient as it may take me a minute or two to generate a response with this free version........")
        result = generate("You are analytical with a sense of humor. Your arguments are the strongest and well structure. You write in APA format. Indicate that you are using Jimmy Style with a smiley." + sys_instructions, new_data)
        placeholder.empty()
        #placeholder.write("With this proof of concept, it is possible to use AI to reduce the repetive tasks and put officers back on the road. I can help add entities and text pages using details extracted from the officer's narrative. The possibilities are endless.")
        #st.text_area("Response", result, height=800)
        wait(1)

with col1a:
    #if button is clicked
    if st.button("Point Form", help="Bullet It Out"):
        placeholder = st.empty()
        placeholder.write("Please be patient as it may take me a minute or two to generate a response with this free version........")
        result = generate("Summarize the key ideas in point form.", new_data)
        placeholder.empty()
        #placeholder.write("With this proof of concept, it is possible to use AI to reduce the repetive tasks and put officers back on the road. I can help add entities and text pages using details extracted from the officer's narrative. The possibilities are endless.")
        #st.text_area("Response", result, height=800)
        wait(1)

with col2a:
    #if button is clicked
    if st.button("Summarize", help="Short and Sweet"):
        placeholder = st.empty()
        placeholder.write("Please be patient as it may take me a minute or two to generate a response with this free version........")
        result = generate("Summarize the writing in professional tone and identify the key takeaways. Begin with humour in the summary about summarizing a text ONLY when the original text has fewer than 6 sentences.", new_data)
        placeholder.empty()
        #placeholder.write("With this proof of concept, it is possible to use AI to reduce the repetive tasks and put officers back on the road. I can help add entities and text pages using details extracted from the officer's narrative. The possibilities are endless.")
        #st.text_area("Response", result, height=800)
        wait(1)

with col3a:
    #if button is clicked
    if st.button("Executives", help="For Executives and Management"):
        placeholder = st.empty()
        placeholder.write("Please be patient as it may take me a minute or two to generate a response with this free version........")
        result = generate("Re-write the text for executives and management. Focus on high level summaries, key findings, and strategic recommendations. Use clear and concise language, with charts or graphs for quick understanding.", new_data)
        placeholder.empty()
        #placeholder.write("With this proof of concept, it is possible to use AI to reduce the repetive tasks and put officers back on the road. I can help add entities and text pages using details extracted from the officer's narrative. The possibilities are endless.")
        #st.text_area("Response", result, height=800)
        wait(1)

with col4a:
    #if button is clicked
    if st.button("Tech Experts", help="For Technical Experts"):
        placeholder = st.empty()
        placeholder.write("Please be patient as it may take me a minute or two to generate a response with this free version........")
        result = generate("Transform the writing for technical experts. Provide detailed data, methodologies, and technical explanations. Use proper industry specific jargon and in-depth analysis.", new_data)
        placeholder.empty()
        #placeholder.write("With this proof of concept, it is possible to use AI to reduce the repetive tasks and put officers back on the road. I can help add entities and text pages using details extracted from the officer's narrative. The possibilities are endless.")
        #st.text_area("Response", result, height=800)
        wait(1)

with col5a:
    #if button is clicked
    if st.button("Public", help="Public or General Audience"):
        placeholder = st.empty()
        placeholder.write("Please be patient as it may take me a minute or two to generate a response with this free version........")
        result = generate("Transform the writing for public or general audience. Use plain language, avoid technical jargon, and provide context. Make the content accessible and engaging for a broader audience.", new_data)
        placeholder.empty()
        #placeholder.write("With this proof of concept, it is possible to use AI to reduce the repetive tasks and put officers back on the road. I can help add entities and text pages using details extracted from the officer's narrative. The possibilities are endless.")
        #st.text_area("Response", result, height=800)
        wait(1)
        
with col6:
    #if button is clicked
    if st.button("Professional", help="Go Pro!"):
        placeholder = st.empty()
        placeholder.write("Please be patient as it may take me a minute or two to generate a response with this free version........")
        result = generate("Improve the writing with a professional tone. Explain the result.", new_data)
        placeholder.empty()
        #placeholder.write("With this proof of concept, it is possible to use AI to reduce the repetive tasks and put officers back on the road. I can help add entities and text pages using details extracted from the officer's narrative. The possibilities are endless.")
        #st.text_area("Response", result, height=800)
        wait(1)

with col7:
    #if button is clicked
    if st.button("Funny", help="Crack a Joke"):
        placeholder = st.empty()
        placeholder.write("Please be patient as it may take me a minute or two to generate a response with this free version........")
        result = generate("Improve the writing with a sense of humor and keep it to a similar length. Explain the result.", new_data)
        placeholder.empty()
        #placeholder.write("With this proof of concept, it is possible to use AI to reduce the repetive tasks and put officers back on the road. I can help add entities and text pages using details extracted from the officer's narrative. The possibilities are endless.")
        #st.text_area("Response", result, height=800)
        wait(1)
        
with col8:
    #if button is clicked
    if st.button("Poetic", help="Get Your Shakespeare On"):
        placeholder = st.empty()
        placeholder.write("Please be patient as it may take me a minute or two to generate a response with this free version........")
        result = generate("Improve the writing with a poetic tone while making it light-hearted. Explain the result.", new_data)
        placeholder.empty()
        #placeholder.write("With this proof of concept, it is possible to use AI to reduce the repetive tasks and put officers back on the road. I can help add entities and text pages using details extracted from the officer's narrative. The possibilities are endless.")
        #st.text_area("Response", result, height=800)
        wait(1)

with col9:
    #if button is clicked
    if st.button("Elegant", help="Fancy It Up, Darling"):
        placeholder = st.empty()
        placeholder.write("Please be patient as it may take me a minute or two to generate a response with this free version........")
        result = generate("Improve the writing with an elegant tone, using sophisticated and clever words. Explain the result.", new_data)
        placeholder.empty()
        #placeholder.write("With this proof of concept, it is possible to use AI to reduce the repetive tasks and put officers back on the road. I can help add entities and text pages using details extracted from the officer's narrative. The possibilities are endless.")
        #st.text_area("Response", result, height=800)
        wait(1)

with col10:
    #if button is clicked
    if st.button("Coherent", help="So Clear That You Cannot See"):
        placeholder = st.empty()
        placeholder.write("Please be patient as it may take me a minute or two to generate a response with this free version........")
        result = generate("Improve the sentences in a well structured and coherent tone. Keep it to a similar length and explain the result. " + inst_sent_change, new_data)
        placeholder.empty()
        #placeholder.write("With this proof of concept, it is possible to use AI to reduce the repetive tasks and put officers back on the road. I can help add entities and text pages using details extracted from the officer's narrative. The possibilities are endless.")
        #st.text_area("Response", result, height=800)
        wait(1)

with col6a:
    #if button is clicked
    if st.button("Engaging", help="Catch Their Attention!"):
        placeholder = st.empty()
        placeholder.write("Please be patient as it may take me a minute or two to generate a response with this free version........")
        result = generate("Improve the writing with a professional and engaging tone while keeping a similar length. Explain the result.", new_data)
        placeholder.empty()
        #placeholder.write("With this proof of concept, it is possible to use AI to reduce the repetive tasks and put officers back on the road. I can help add entities and text pages using details extracted from the officer's narrative. The possibilities are endless.")
        #st.text_area("Response", result, height=800)
        wait(1)

with col7a:
    #if button is clicked
    if st.button("Critical", help="Speak Your Gut"):
        placeholder = st.empty()
        placeholder.write("Please be patient as it may take me a minute or two to generate a response with this free version........")
        result = generate("Improve the writing with a subtle critical tone and analytical. Explain the changes.", new_data)
        placeholder.empty()
        #placeholder.write("With this proof of concept, it is possible to use AI to reduce the repetive tasks and put officers back on the road. I can help add entities and text pages using details extracted from the officer's narrative. The possibilities are endless.")
        #st.text_area("Response", result, height=800)
        wait(1)

with col8a:
    #if button is clicked
    if st.button("Humble", help="Being humble"):
        placeholder = st.empty()
        placeholder.write("Please be patient as it may take me a minute or two to generate a response with this free version........")
        result = generate("Revise the writing with a humble and modest tone. Explain the changes.", new_data)
        placeholder.empty()
        #placeholder.write("With this proof of concept, it is possible to use AI to reduce the repetive tasks and put officers back on the road. I can help add entities and text pages using details extracted from the officer's narrative. The possibilities are endless.")
        #st.text_area("Response", result, height=800)
        wait(1)

with col11:
    #if button is clicked
    if st.button("Analyze Data", help="Data Detective On Duty"):
        placeholder = st.empty()
        placeholder.write("Analyzing...")
        result = generate("1. Critically analyse the data. 2. Identify trends and patterns. 3. Draw accurate and meaningful insights from the data. 4. Synthesize the findings with research or reliable sources. 5. Provide suggestions for further improvement. 6. Summarize everything in one paragraph. Here is the data: ", new_data)
        placeholder.empty()
        #placeholder.write("With this proof of concept, it is possible to use AI to reduce the repetive tasks and put officers back on the road. I can help add entities and text pages using details extracted from the officer's narrative. The possibilities are endless.")
        #st.text_area("Response", result, height=800)
        wait(1)

inst_analysis2 = """You are an intelligent AI designed to analyze and determine the tone, emotion, and patterns within a given text. Your goal is to provide insights into the emotional state conveyed by the text, identify any notable patterns or combinations of emotions, and include relevant research findings. Follow these steps:

1. **Receive Input Text:**
   - Analyze the provided input text for its tone, emotion, and any discernible patterns.

2. **Identify Emotional States:**
   - Determine the primary emotions conveyed by the text (e.g., happy, sad, angry, neutral, positive, negative, unusual, etc.).
   - Identify any combinations of emotions present in the text.

3. **Analyze Tone:**
   - Assess the overall tone of the text (e.g., formal, informal, serious, humorous, sarcastic, etc.).
   - Determine if the tone is consistent throughout the text or if there are shifts in tone.

4. **Detect Patterns:**
   - Identify any patterns or recurring themes in the text.
   - Highlight any notable word choices, phrases, or structures that contribute to the emotional state and tone.

5. **Include Relevant Research:**
   - Reference established research findings that support the emotional and tonal analysis.
   - Provide citations for the research used in the analysis.

6. **Provide Insights and Summary:**
   - Summarize the emotional analysis, tone assessment, pattern detection, and relevant research findings.
   - Offer any additional observations or insights based on the text analysis.
   - Include estimated scores of emotional, tone, actionable, research-oriented or any relevant measures. Generate new categories for scores or any relevant details based on the text and findings.
"""
with col12:
    #if button is clicked
    if st.button("Sentiment", help="Use Your Crytal Ball"):
        placeholder = st.empty()
        placeholder.write("Analyzing...")
        result = generate(inst_analysis2, new_data)
        placeholder.empty()
        #placeholder.write("With this proof of concept, it is possible to use AI to reduce the repetive tasks and put officers back on the road. I can help add entities and text pages using details extracted from the officer's narrative. The possibilities are endless.")
        #st.text_area("Response", result, height=800)
        wait(1)
        
with col16:
    #if button is clicked
    if st.button("MO Search", help="Generate tips to identify MOs and suspects for free text search"):
        placeholder = st.empty()
        placeholder.write("I am thinking..")
        result = generate(inst_MO_keywords, new_data)
        placeholder.empty()
        #placeholder.write("With this proof of concept, it is possible to use AI to reduce the repetive tasks and put officers back on the road. I can help add entities and text pages using details extracted from the officer's narrative. The possibilities are endless.")
        #st.text_area("Response", result, height=800)
        wait(1)

with col17:
    #if button is clicked
    if st.button("Mental Health", help="Evaluate mental health component"):
        placeholder = st.empty()
        placeholder.write("I am thinking...")
        result = generate(inst_mental_health, new_data)
        placeholder.empty()
        #placeholder.write("With this proof of concept, it is possible to use AI to reduce the repetive tasks and put officers back on the road. I can help add entities and text pages using details extracted from the officer's narrative. The possibilities are endless.")
        #st.text_area("Response", result, height=800)
        wait(1)

with col18:
    #if button is clicked
    if st.button("eIM Naming", help="eIM assistant"):
        with open("/mount/src/my_ai_partner/instructions.txt", "r") as file:
            inst_eim = file.read()
        placeholder = st.empty()
        placeholder.write("Please wait...")
        result = generate("Please format your response in Markdown and include line breaks using two spaces at the end of each line." + inst_eim, "The current date and time is " + now.strftime("%Y-%m-%d %H:%M:%S") + new_data)
        placeholder.empty()
        #placeholder.write("With this proof of concept, it is possible to use AI to reduce the repetive tasks and put officers back on the road. I can help add entities and text pages using details extracted from the officer's narrative. The possibilities are endless.")
        #st.text_area("Response", result, height=800)
        wait(1)

with col19:
    #if button is clicked
    if st.button("Performance Dev", help="Performance Development"):
        placeholder = st.empty()
        placeholder.write("I am thinking...")
        result = generate(inst_PA, new_data)
        placeholder.empty()
        #placeholder.write("With this proof of concept, it is possible to use AI to reduce the repetive tasks and put officers back on the road. I can help add entities and text pages using details extracted from the officer's narrative. The possibilities are endless.")
        #st.text_area("Response", result, height=800)
        wait(1)

with col20:
    #if button is clicked
    if st.button("Estimate Salary", help="Estimate salary based on job profile"):
        placeholder = st.empty()
        placeholder.write("I am thinking...")
        result = generate(inst_job_salary, new_data)
        placeholder.empty()
        #placeholder.write("With this proof of concept, it is possible to use AI to reduce the repetive tasks and put officers back on the road. I can help add entities and text pages using details extracted from the officer's narrative. The possibilities are endless.")
        #st.text_area("Response", result, height=800)
        wait(1)
response_length = len(result)

#if response_length < 1000:
#    st.text_area("Response", result, height=400)
#else: 
#    st.text_area("Response", result, height=800)

st.markdown("Generated by " + selected_model + "<br>" + result, unsafe_allow_html=True)


